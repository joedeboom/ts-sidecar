# ts-sidecar

**ts-sidecar** is a utility for generating a Docker Compose file and required directory structure to add a containerized application to your Tailscale tailnet. By containerizing the sidecar, you can serve HTTPS to your devices within the tailnet, adding an extra layer of security and flexibility.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Additional Setup](#additional-setup)
- [Generated Files and Directories](#generated-files-and-directories)

---

## Overview

This tool creates a new Tailscale sidecar container file structure that contains:

- A Docker Compose file which defines two services:
  - A Tailscale container (`<SERVICE_NAME>-ts`) to manage networking.
  - A framework of the user-defined service container (`<SERVICE_NAME>`) whose network is defined to use Tailscale sidecar's service, making your container accessible to your tailnet.
  
- A service configuration file (`service.json`) which sets up  proxy rules for the Tailscale sidecar to serve HTTPS to the container's internal port. 


---

## Prerequisites

- Python 3.x installed.
- Docker installed.

### The script takes 4 arguments
- The **name** of the service you wish to add to your tailnet.
- An **authentication key** to add a node to your tailnet.
- The **internal port** the container is expecting to be served HTTPS to.
- The **path** to your docker directory

---

## Usage

1. Open your terminal.
2. Clone the project directory:
    ```sh
    git clone https://github.com/joedeboom/ts-sidecar.git
    cd ts-sidecar
    ```
3. Run the script with the required parameters:
```
    ```sh
    python3 generate_sidecar.py --name SERVICE_NAME --port PORT --docker-dir PATH_TO_DIR --auth-key TAILSCALE_AUTH_KEY
    ```
```

Replace `SERVICE_NAME` with the name of the service/node to be added to your tailnet and `PORT` with your service's internal port for HTTPS redirection. Replace `PATH_TO_DIR` with the path to your docker folder. Replace `TAILSCALE_AUTH_KEY` with an authentication key frojm github. 

---

## Additional Setup

1. **Tailscale Authentication**:  
    Once the containers are up and your sidecar has been authenticated, you can remove or comment out the authentication key line from the docker compose file.
   
2. **Service Customization**:   
   Edit your service container settings in the Docker Compose file to specify the appropriate image details, volumes, and environment variables as needed. DO NOT specify any ports in the docker compose. The internal port is specified in the generated service.json file for the tailscale sidecar to serve HTTPS to.

3. **Launch Containers**
    Launch the docker stack. In the service's directory:
    ```
    docker compose up -d
    ```

---

## Generated Files and Directories

When you run the script, the following structure will be created in your Docker directory (e.g. `/home/joe/docker`):

```
/home/joe/docker/SERVICE_NAME/
├── docker-compose.yml        # Docker Compose file to launch the sidecar and service
└── tailscale
    ├── ts-state              # Directory for Tailscale state persistence
    └── config
        └── service.json      # JSON file with proxy configuration for HTTPS
```

- The [`generate_docker_compose`](generate_sidecar.py#L8) function generates the Docker Compose file.
- The [`generate_service_json`](generate_sidecar.py#L50) function generates the `service.json`.

---

## Roadmap
- Have auth key as command line argument.
- Have path to docker folder as command line argument.
- 