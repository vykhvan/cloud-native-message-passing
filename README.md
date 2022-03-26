# UdaConnect

## Technologies
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver.
* [gPRC](https://grpc.io/) - A high performance, open source universal RPC framework.
* [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM.
* [PostgreSQL](https://www.postgresql.org/) - Relational database.
* [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries.
* [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments.
* [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems.
* [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster.
* [Helm](https://helm.sh/) - The package manager for Kubernetes.
* [Apache Kafka](https://kafka.apache.org/) - Open-source distributed event streaming platform.

## Running the app

The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites

* Install Docker
* Set up a DockerHub account
* Set up kubectl
* Install VirtualBox with at least version 6.0
* Install Vagrant with at least version 2.0
* Install Helm

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

### Initialize K3s
In this project's root, run `vagrant up`.
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

### Set up `kubectl`
After `vagrant up` is done, you will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
You will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. You should see output similar to the one that I've shown below. Note that the output below is just for your reference: every configuration is unique and you should _NOT_ copy the output I have below.

Copy the contents from the output issued from your own command into your clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and you will find yourself back in your computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output here.

Afterwards, you can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### Install Apache Kafka
`helm repo add bitnami https://charts.bitnami.com/bitnami`

`helm install kafka bitnami/kafka`

### Deployment Steps
1. `kubectl apply -f deployment/db-persons-configmap.yaml` - Set up environment variables for the persons database.
2. `kubectl apply -f deployment/db-locations-configmap.yaml` - Set up environment variables for the locations database.
3. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods.
4. `kubectl apply -f deployment/postgres-persons-deployment.yaml` - Set up a Postgres database for persons service.
5. `kubectl apply -f deployment/postgres-locations-deployment.yaml` - Set up a Postgres database for locations service.
6. `kubectl apply -f deployment/persons-api-deployment.yaml` - Set up the service and deployment for Persons API.
7. `kubectl apply -f deployment/connections-api-configmap.yaml` - Set up environment variables for the Connections API.
8. `kubectl apply -f deployment/connections-api-deployment.yaml` - Set up the service and deployment for Connections API.
9. `kubectl apply -f deployment/kafka-configmap.yaml` - Set up environment variables for Kafka.
10. `kubectl apply -f deployment/locations-producer-deployment.yaml` - Set up service and deployment for Locations API.
11. `kubectl apply -f deployment/locations-consumer-deployment.yaml` - Set up deployment for kafka consumer.
12. `kubectl apply -f deployment/udaconnect-app-deployment.yaml` - Set up the service and deployment for front-end.

### Seed the Database

1. `sh scripts/run_db_persons_command.sh <POD_NAME>`
2. `sh scripts/run_db_locations_command.sh <POD_NAME>`

### Verifying it Works
Once the project is up and running, you should be able to see 3 deployments and 3 services in Kubernetes: kubectl get pods and kubectl get services - should both return udaconnect-app, udaconnect-api, and postgres

Services:

* http://localhost:30000/ - Frontend ReactJS Application.
* http://localhost:30001/ - Locations Service API.
* http://localhost:30002/ - Persons Service API.
* http://localhost:30003/ - Connections Service API.