import os
import sys
import argparse


DOCKER_DIR = "/home/joe/docker"


def generate_docker_compose(name, service_dir):
    """
    Generates a docker-compose.yml file with the specified configuration.
    """
    docker_compose_content = f"""services:

    {name}-ts:
        container_name: {name}-ts
        image: tailscale/tailscale:latest
        hostname: {name}
        cap_add:
            - NET_ADMIN
            - SYS_MODULE
        volumes:
            - /dev/net/tun:/dev/net/tun
            - {service_dir}/tailscale/ts-state:/var/lib/tailscale
            - {service_dir}/tailscale/config:/config
        environment:
            # https://github.com/tailscale/tailscale/issues/4913#issuecomment-1186402307
            # we have to tell the container to put the state in the same folder
            # that way the state is saved on the host and survives reboot of the container
            - TS_STATE_DIR=/var/lib/tailscale
            # this have to be used only on the first time
            # after that, the state is saved in /var/lib/tailscale and the next line can be commented out
            - TS_AUTH_KEY=
            - TS_SERVE_CONFIG=/config/service.json
        restart: unless-stopped

    {name}:
        image:
        container_name: {name}
        network_mode: "service:{name}-ts"
        environment:
            - TZ=America/Chicago
        depends_on:
            - {name}-ts
        restart: unless-stopped

    """
    docker_compose_filepath = os.path.join(service_dir, "docker-compose.yml")
    with open(docker_compose_filepath, "w") as f:
        f.write(docker_compose_content)
    print(f"Docker Compose file generated at {docker_compose_filepath}")

def generate_service_json(name, config_dir, port):
    service_json_content = f"""{{
    "TCP": {{
        "443": {{
            "HTTPS": true
        }}
    }},
    "Web": {{
        "${{TS_CERT_DOMAIN}}:443": {{
            "Handlers": {{
                "/": {{
                    "Proxy": "http://127.0.0.1:{port}"
                }}
            }}
        }}
    }},
    "AllowFunnel": {{
        "${{TS_CERT_DOMAIN}}:443": false
    }}
}}"""
    service_json_filepath = os.path.join(config_dir, "service.json")
    with open(service_json_filepath, "w") as f:
        f.write(service_json_content)
    print(f"Service JSON file generated at {service_json_filepath}")


if __name__ == "__main__":
    # Fetch service name from command line arguments
    parser = argparse.ArgumentParser(description="Generate a Docker Compose file for Tailscale.")
    parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Name of the Tailscale service.",
    )
    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="Port of the Tailscale service.",
    )
    # Parse args after all arguments have been added
    args = parser.parse_args()
    name = args.name
    port = args.port

    # Make folders for the service in the docker directory
    service_dir = os.path.join(DOCKER_DIR, name)
    tailscale_dir = os.path.join(service_dir, "tailscale")
    config_dir = os.path.join(tailscale_dir, "config")
    ts_state_dir = os.path.join(tailscale_dir, "ts-state")
    os.makedirs(service_dir, exist_ok=True)
    os.makedirs(tailscale_dir, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(ts_state_dir, exist_ok=True)

    # Create files
    generate_docker_compose(name, service_dir)
    generate_service_json(name, config_dir, port)

    print(f"Service {name} sidecar created successfully.")

