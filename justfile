docker_run:
    docker run -it --rm --mount type=bind,src=.,dst=/opt --env-file .env sample-chatgpt /bin/bash
