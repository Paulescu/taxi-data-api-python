<div align="center">
    <h1>Build and deploy a professional REST API</h1>
</div>

#### Table of contents
* [Our goal](#our-goal-)
* [How to run this thing locally?](#how-to-run-this-thing-locally)
* [How to deploy to Kubernetes?](#deployment-to-a-kubernetes-cluster)
* []()
* [Wanna learn more real-world ML?](#wanna-learn-more-real-world-ml)

## Our goal 🎯

Let’s build and deploys a production-ready REST API that can serve data on historical taxi rides in NYC.

The original data is stored in one-month parquet files [on this website](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), and our goal is to make it easily accessible to the WORLD through a REST API.


## How to run this thing locally

Git clone this repository, cd into the root directory of the project and then run the following commands using make.

1. Install [Python Poetry](https://python-poetry.org/docs/#installation) (if necessary)
and create an isolated virtual environmnet for development purposes.
    ```
    $ make install
    ```

2. Test, build and run the dockerized REST API with
    ```
    $ make all
    ```

3. Check the API is up and running locally, and that you can connect to it
    ```
    $ make health-check-local
    ```

4. Send a sample request to the local API
    ```
    $ make sample-request-local
    ```

Good job. The API is up and running locally.


## Deployment to a Kubernetes cluster
Let's now make it available to the whole world! Let's deploy it to a production Kubernetes cluster.

### Why Kubernetes?


### Why Gimlet?

### Manual deployment

### CI/CD -> Automatic testing and deployment with Github actions


## Wanna learn more real-world ML?

Join more than 19k builders to the [**Real-World ML Newsletter**](https://www.realworldml.net/subscribe). Every Saturday morning.

### [👉🏽 Click here to subscribe for FREE](https://www.realworldml.net/subscribe)

### [**👉🏽 My live courses on Real World ML**](https://www.realworldml.net/courses)


