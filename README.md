# ts-sidecar
Creates a new tailscale sidecar container directory structure to serve https to your tailnet. 

Set the path to the docker directory in the main function. Then call the function with 
```
python3 generate_sidecar.py --name SERVICE_NAME --port PORT
```

# Additional Setup
After the docker compose file is generated, you must enter a tailscale authentication key to add the sidecar to your tailnet. After the container is launched for the first time and authenticated, you can remove the key and comment out the line.

You will also need to enter details for the container you wish to set up regarding including the image details, volumes, and environment variables. 