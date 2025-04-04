# ts-sidecar
Creates a new tailscale sidecar container directory structure to serve https to your tailnet. 

Set the path to the docker directory in the main function. Then call the function with 
```
python3 generate_sidecar.py --name SERVICE_NAME --port PORT
```

# NOTE
The service you deploy must use the ts-sidecar's network:
```
SERVICE_NAME:
    network_mode: "service:SERVICE_NAME-ts"