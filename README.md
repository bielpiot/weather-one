# Weather-one

Pulumi-deployed Dash-based simple weather application running on Google Cloud Platform

## Overview
![Weather-one diagram](https://github.com/bielpiot/weather-one/blob/master/diagram.png)

Weather-one is an example of automized application build & deployment into cloud environment using IaC approach. Goal of the project was to build backend utilizing several GCP services along with frontend running in some python-based technology. I settled at dash as I had no closer familiarity with it beforehand and it seemed to be a remarkable data-visualisation tool.

Weather-one utilizes:
Dash-plotly - data visualization
Docker - Dash-plotly app containerization
GCP cloud run - Hosting containerized app along with using storage bucket as docker volume
GCP storage - storing app data & function code data
GCP cloud functions - running a function pulling data from API service ([7timer](http://www.7timer.info/doc.php)) to storage
GCP scheduler - triggering function periodically (Currently it is set to refresh data every 1 hour)


## Instalation & deployment
# Prerequisites:
1. [GCP account](https://console.cloud.google.com/getting-started)
2. [Pulumi CLI](https://www.pulumi.com/docs/get-started/install/)
3. [Pulumi-GCP configuration](https://www.pulumi.com/docs/intro/cloud-providers/gcp/setup/)
4. [Docker](https://docs.docker.com/install/)
5. [Pulumi-Docker configuration](https://www.pulumi.com/registry/packages/docker/installation-configuration/)
6. [Configure docker-gcp.io communication using `gcloud auth configure-docker`](https://cloud.google.com/sdk/gcloud/reference/auth/configure-docker)

# Run
1. Create a new stack:

    ```bash
    pulumi stack init <stack name>
    ```

2. Configure GCP project and region:

    ```bash
    pulumi config set gcp:project <projectname>
    pulumi config set gcp:region <region>
    ```

    Depending on your environment, you might also want to set docker:host in your config, refer to point 5.

    ```bash
    pulumi config set docker:host <host>
    ```

3. Run `pulumi up` to preview and deploy changes:

    ```bash
    $ pulumi up
    Previewing changes:
    ...
    Performing changes:
    ...
    Outputs:
    - cloud_run_url  : "https:// ..."
    ...
    Resources:
        + 21 created
    Duration: 3m21s
    ```

You can get link of your app by calling 'pulumi stack output cloud_run_url'. Below you can see a showcase of application:
![](https://github.com/bielpiot/weather-one/blob/master/weather-one.gif)

You can also check app running [here](https://weather-one-dash-0738b6d-nsh4gb4fvq-lm.a.run.app)

4. Cleanup

    ```
    $ pulumi destroy
    ...
    $ pulumi stack rm dev
    ...
    ```

## Notes

If you did not have API service for cloud functions enabled in your project prior to deploying pulumi stack you may get error associated with Cloud Function deployment. In such case you simply need to wait a couple of minutes (for google API service to process) and run 'pulumi up' again - stack will get updated.

## Potential further upgrades/changes

- attaching detailed description for measures values
- adding icons rendered when certain pattern of measure values occurs (eg. good weather for astronomical observations given seeing < x, transparency < y etc.)
- enabling parametrization (eg. adding/removing locations) throuh ENV values
- visual upgrades (app is pretty basic currently)
- adding more tests and CI/CD pipeline if new functionalities were to be added

## License

Copyright (c) Piotr Bielecki

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.