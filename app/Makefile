APP_IMAGE_NAME = face-recognition-webcam-app
.PHONY: build xhost run run-dev run-preprocess-photos stop clean

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image with application
	@cp -r $(shell pwd)/../face_recognition $(shell pwd)/.
	docker build -t $(APP_IMAGE_NAME):latest .
	@rm -r $(shell pwd)/face_recognition

xhost: ## Allow container connect on X11 host server
	xhost +local:docker

run: ## Run App from docker image
	docker run -it --rm --device=/dev/video0:/dev/video0  \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		$(APP_IMAGE_NAME)

run-dev: ## Run App using Docker image and host code and photo dir
	docker run -it --rm --device=/dev/video0:/dev/video0  \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD)/../face_recognition:/app/face_recognition \
		-v $(PWD)/../photos:/app/photos \
		-v $(PWD)/main.py:/app/main.py \
		$(APP_IMAGE_NAME)

run-preprocess-photos: ## Pre-process images from photos dir
		docker run -it --rm \
		-v $(PWD)/../photos:/app/photos \
		-v $(PWD)/preprocess_photo.py:/app/preprocess_photo.py \
		$(APP_IMAGE_NAME) bash -c "python preprocess_photo.py"

stop: ## Stops and removes container
	@echo "Stopping and removing containers..."
	docker stop $(APP_IMAGE_NAME)
	docker rm $(APP_IMAGE_NAME)

clean: stop ## Cleans docker volumes and images
	@echo "Cleaning up Docker volumes and images..."
	docker rmi $(APP_IMAGE_NAME):latest
