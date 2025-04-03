.ONESHELL:
IMAGE_NAME=face-recognition-base
.PHONY: build clean

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Builds base image from all projects of face-recognition
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):latest .

clean: ## Removes docker images
	@echo "Cleaning up Docker volumes and images..."
	docker rmi $(IMAGE_NAME):latest

intall-deps: ## Install dependencies
	@echo "Installing dependencies..."
	ansible-playbook --ask-become ansible/localhost.yml
