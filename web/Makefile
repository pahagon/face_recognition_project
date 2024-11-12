APP_IMAGE_NAME = face-recognition-webcam-web
.PHONY: help build run-dev dev-web-server

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image with application
	@cp -r $(shell pwd)/../face_recognition $(shell pwd)/.
	docker build -t $(APP_IMAGE_NAME):latest .
	@rm -r $(shell pwd)/face_recognition

run-dev: ## Run App using Docker image and host code and photo dir
	docker run -it --rm \
		-v $(PWD)/../face_recognition:/app/face_recognition \
		-v $(PWD)/../photos:/app/photos \
		-v $(PWD)/main.py:/app/main.py \
		-p 5000:5000 \
		$(APP_IMAGE_NAME)

dev-web-server: ## Starts a development web server
	cd assets && python3 -m http.server
