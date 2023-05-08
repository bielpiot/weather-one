import os
import pulumi
import pulumi_gcp as gcp
import pulumi_docker as docker
from pulumi_docker import DockerBuild
from pulumi import Config, ResourceOptions


# Part 0: Initials, common resources
config = Config()
project = gcp.organizations.get_project().project_id
org = pulumi.get_organization()

PATH_TO_FUNCTIONS_SOURCE_CODE = "./get_data"
PATH_TO_DASH_APP = "./dash_app"
FAILSAFE_DATA_PATH = "./failsafe_data/failsafe_data.csv"

# list of api services that has to be enabled
services_apis = [
    "cloudbuild.googleapis.com",
    "cloudfunctions.googleapis.com",
    "run.googleapis.com",
    "storage.googleapis.com",
    "containerregistry.googleapis.com",
    "cloudscheduler.googleapis.com",
]

# enable/prepare api services
apis = {
    f"{project}-{service_api}": gcp.projects.Service(
        f"{project}-{service_api}",
        disable_dependent_services=True,
        project=project,
        service=service_api,
    )
    for service_api in services_apis
}

# Service account to run operations
service_acc = gcp.serviceaccount.Account(
    "serviceAccount",
    account_id="weather-one-service-acc",
    display_name="Service account for Weather One",
)

# create data buckets: one for functions code, second for downloaded data
data_bucket = gcp.storage.Bucket("data_storage", location="EUROPE-CENTRAL2")
repo_bucket = gcp.storage.Bucket("code_storage", location="EUROPE-CENTRAL2")

# Part I: get_data utilizing Cloud function (request API -> store .csv @ bucket)
# Zip function code into archive, as required by Cloud Function service
assets = {}
for file in os.listdir(PATH_TO_FUNCTIONS_SOURCE_CODE):
    location = os.path.join(PATH_TO_FUNCTIONS_SOURCE_CODE, file)
    asset = pulumi.FileAsset(path=location)
    assets[file] = asset

archive = pulumi.AssetArchive(assets=assets)

# Build Cloud Storage object containing function's source code
source_archive_object = gcp.storage.BucketObject(
    "get-data-func-object",
    name="func",
    bucket=repo_bucket.name,
    source=archive,
)

# Environmental values for Cloud Function
func_config_values = {"BUCKET_NAME": data_bucket.name}

# Function creation
data_update_function = gcp.cloudfunctions.Function(
    "weather-one-function",
    description="Function that gets data from API and loading it into bucket (.csv)",
    runtime="python311",
    available_memory_mb=128,
    source_archive_bucket=repo_bucket.name,
    source_archive_object=source_archive_object.name,
    entry_point="save_astrometeo_data_to_bucket",
    trigger_http=True,
    environment_variables=func_config_values,
    region="europe-central2",
    project=project,
    opts=ResourceOptions(
        depends_on=[
            apis[f"{project}-cloudfunctions.googleapis.com"],
            apis[f"{project}-cloudbuild.googleapis.com"],
        ]
    ),
)

# Part II : Dash_app frontend, utilizing Cloud Run (read data -> build app)
# failsafe data csv upload to data bucket
failsafe_data_object = gcp.storage.BucketObject(
    "failsafe-data-csv",
    name="failsafe_data.csv",
    bucket=data_bucket.name,
    source=pulumi.FileAsset(FAILSAFE_DATA_PATH),
)

# create a private GCR repo, get info
registry = gcp.container.Registry(
    "weather-one-registry",
    location="EU",
    project=project,
    opts=ResourceOptions(
        depends_on=[apis[f"{project}-containerregistry.googleapis.com"]]
    ),
)
registry_url = registry.id.apply(
    lambda _: gcp.container.get_registry_repository().repository_url
)
image_name = registry_url.apply(lambda url: f"{url}/weather-one-image:latest")


# build image and push to gcr repository
weather_one_dash_image = docker.Image(
    name="weather-one-image",
    build=DockerBuild(context="./dash_app"),
    image_name=image_name,
    # registry=docker.ImageRegistry(server=registry_url)
)

cloud_run = gcp.cloudrun.Service(
    "weather-one-dash",
    location=Config("gcp").require("region"),
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[
                gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                    image=weather_one_dash_image.image_name,
                    envs=[
                        gcp.cloudrun.ServiceTemplateSpecContainerEnvArgs(
                            name="BUCKET_NAME", value=data_bucket.name
                        )
                    ],
                )
            ]
        )
    ),
    opts=ResourceOptions(
        depends_on=[
            apis[f"{project}-run.googleapis.com"],
            weather_one_dash_image,
            failsafe_data_object,
        ]
    ),
)

# Part III: Cloud Scheduler responsible for triggering get_data function

gcp_scheduler = gcp.cloudscheduler.Job(
    "job",
    description="func job @ schedule",
    schedule="0 * * * *",
    time_zone="Etc/UTC",
    attempt_deadline="320s",
    http_target=gcp.cloudscheduler.JobHttpTargetArgs(
        uri=data_update_function.https_trigger_url,
        oidc_token=gcp.cloudscheduler.JobHttpTargetOidcTokenArgs(
            service_account_email=service_acc.email,
        ),
    ),
    opts=ResourceOptions(depends_on=[apis[f"{project}-cloudscheduler.googleapis.com"]]),
)


# Part IV: IAM
storage_manager = gcp.storage.BucketIAMMember(
    "manager",
    bucket=repo_bucket.name,
    role="roles/storage.admin",
    member=service_acc.email.apply(lambda sa_email: f"serviceAccount:{sa_email}"),
)

func_invoker = gcp.cloudfunctions.FunctionIamMember(
    "invoker",
    project=data_update_function.project,
    region=data_update_function.region,
    cloud_function=data_update_function.name,
    role="roles/cloudfunctions.invoker",
    member=service_acc.email.apply(lambda sa_email: f"serviceAccount:{sa_email}"),
)

cloudrun_user = gcp.cloudrun.IamMember(
    "viewer",
    location=cloud_run.location,
    service=cloud_run.name,
    role="roles/run.invoker",
    member="allUsers",
)

pulumi.export("full_image_name", weather_one_dash_image.image_name)
pulumi.export("cloud_run_url", cloud_run.statuses[0].url)
