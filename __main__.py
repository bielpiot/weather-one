import pulumi
import pulumi_gcp as gcp
import pulumi_docker as docker
from pulumi_docker import DockerBuild
from pulumi import Output, Config
from pulumi_gcp.cloudrun import (
    ServiceTemplateMetadataArgs,
    ServiceTemplateSpecContainerEnvArgs,
)

config = Config()
project = pulumi.get_project()
org = pulumi.get_organization()

# list of api services that has to be enabled
services_apis = ['cloudfunctions.googleapis.com', 'run.googleapis.com', 'storage.googleapis.com', 'containerregistry.googleapis.com']

# enable/prepare api services
apis = [gcp.projects.Service(f'{project}-{service_api}',
                             disable_dependent_services=True,
                             project=project,
                             service=service_api)
        for service_api in services_apis]

# create a private GCR repo, get info
registry = gcp.container.Registry('weather-one-registry')
registry_url = registry.id.apply(lambda _: gcp.container.get_registry_repository().repository_url)
image_name = registry_url.apply(lambda url: f'{url}/dash-app:latest')
registry_info = None #standard gcp authentication used


# build image and push to gcr repository
weather_one_dash_image = docker.Image(
    build = DockerBuild(context='./dash-app'),
    image_name=image_name,
    registry=registry_info
)

weather_one_data_bucket = gcp.storage.Bucket()
weather_one_repo_bucket = gcp.storage.Bucket()

weather_one_sa = gcp.service_account.Account("serviceAccount",
                                              account_id="weather-one-service-acc",
                                              display_name="Service account for Weather One")

weather_one_function = gcp.cloudfunctions.Function("weather_one_function",
    description= 'Function responsible for getting weather data from API and loading it into bucket as csv',
    runtime='python310',
    available_memory_mb=128,
    source_archive_bucket=weather_one_data_bucket.name,
    source_archive_object=weather_one_repo_bucket.name,
    entry_point='load_astrometeo_data_to_bucket',
    environment_variables= {
        "BUCKET_NAME": weather_one_data_bucket.name
    }

)


gcp_scheduler = gcp.cloudscheduler.Job()

cloud_run = gcp.cloudrun.Service(
    "weather-one-dash",
    location=Config("gcp").require("region"),
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image= weather_one_dash_image.image_name,
                envs = {"BUCKET_NAME": weather_one_data_bucket.name})]
        )
))


# cloud_run = gcp.cloudrun.Service(
#     "default-service",
#     location=Config("gcp").require("region"),
#     template=gcp.cloudrun.ServiceTemplateArgs(
#         metadata=ServiceTemplateMetadataArgs(
#             annotations={
#                 "run.googleapis.com/cloudsql-instances": sql_instance.connection_name
#             }
#         ),
#         spec=gcp.cloudrun.ServiceTemplateSpecArgs(
#             containers=[
#                 gcp.cloudrun.ServiceTemplateSpecContainerArgs(
#                     image="gcr.io/cloudrun/hello",
#                     envs=[
#                         ServiceTemplateSpecContainerEnvArgs(
#                             name="DATABASE_URL",
#                             value=sql_instance_url,
#                         )
#                     ],
#                 )
#             ],
#         ),
#     ),
#     traffics=[
#         gcp.cloudrun.ServiceTrafficArgs(
#             latest_revision=True,
#             percent=100,
#         )
#     ],
# )

pulumi.export('full_image_name', weather_one_dash_image.image_name)
pulumi.export("cloud_run_url", cloud_run.statuses[0].url)