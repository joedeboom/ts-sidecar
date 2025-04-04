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
  - A framework of the user-defined service container (`<SERVICE_NAME>`) that joins the Tailscale network via the Tailscale sidecar.
  
- A service configuration file (`service.json`) which sets up HTTPS and proxy rules for the Tailscale sidecar.

The workflow uses [generate_sidecar.py](generate_sidecar.py) to generate all necessary files and creates the proper folder structure in your Docker directory.

---

## Prerequisites

- Python 3.x installed.
- Docker installed.
- A working Tailscale setup.
- The path to your Docker directory correctly set inside the [generate_sidecar.py](generate_sidecar.py) file (currently set to `/home/joe/docker`).

---

## Usage

1. Open your terminal.
2. Clone the project directory:
    ```sh
    git clone https://github.com/joedeboom/ts-sidecar.git
    cd ts-sidecar
    ```
3. Update the `DOCKER_DIR` path at the top of generate_sidecar.py to point to the directory of your choice. By default it points to `/home/joe/docker`.
3. Run the script with the required parameters:
    ```sh
    python3 generate_sidecar.py --name SERVICE_NAME --port PORT
    ```
   Replace `SERVICE_NAME` with the name of the service/node to be added to your tailnet and `PORT` with your service's internal port for HTTPS redirection.

---

## Additional Setup

1. **Tailscale Authentication**:  
   After running the script, edit the generated Docker Compose file to include a Tailscale authentication key on the line indicated by `TS_AUTH_KEY=`. Once the containers are up and your sidecar has been authenticated, you can remove or comment out the authentication key line. 
   
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