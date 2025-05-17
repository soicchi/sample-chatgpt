build:
	docker build -t sample-chatgpt .

interactive_run:
	docker run -it --mount type=bind,source=.,target=/opt --env-file .env --rm sample-chatgpt bash
