APP_IMAGE_NAME = face-recognition-webcam-web
.PHONY: help build clean run-local stop-local run-local-web-server run-local-redis run-local-redis-create-schema run-local-redis-seeds run-local-redis-check run-helm-install-bitmami run-helm-install-redis

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker image with application
	docker build -t $(APP_IMAGE_NAME):latest .

clean: ## Cleans docker volumes and images
	@echo "Cleaning up Docker volumes and images..."
	docker rmi -f $(APP_IMAGE_NAME):latest

run-local: ## Run App using Docker image and host code and photo dir
	docker run --name fc-webapp -it --rm \
		-v $(PWD)/../face_recognition:/app/face_recognition \
		-v $(PWD)/main.py:/app/main.py \
		-e FC_REDIS_HOST=$(shell docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' fc-redis) \
		-e FC_REDIS_PORT=6379 \
		-e FC_REDIS_CLUSTER=false \
		-p 5000:5000 \
		$(APP_IMAGE_NAME)

stop-local: ## Stops and removes container
	@echo "Stopping and removing containers..."
	docker stop $(APP_IMAGE_NAME)
	docker rm $(APP_IMAGE_NAME)

run-local-web-server: ## Starts a development web server
	cd assets && python3 -m http.server

run-local-redis: ## Starts a development redis server
	docker run --name fc-redis -d -p 6379:6379 redis/redis-stack-server:latest

run-local-redis-create-schema: ## Create schema in redis
	docker run -it --rm \
		-v $(PWD)/redis/schema.py:/app/main.py \
		$(APP_IMAGE_NAME)

run-local-redis-seeds: ## Insert face embeddings into redis
	docker run -it --rm \
		-v $(PWD)/../face_recognition:/app/face_recognition \
		-v $(PWD)/../photos:/app/photos \
		-v $(PWD)/redis/seed.py:/app/main.py \
		$(APP_IMAGE_NAME)

run-local-redis-check: ## Check if face embeddings are in redis
	docker run -it --rm \
		-v $(PWD)/../face_recognition:/app/face_recognition \
		-v $(PWD)/../photos:/app/photos \
		-v $(PWD)/redis/check.py:/app/main.py \
		$(APP_IMAGE_NAME)

run-helm-install-bitmami: ## Install helm
	helm repo add bitnami https://charts.bitnami.com/bitnami

run-helm-install-redis: ## Starts a redis server in minikube
	helm install fr-redis bitnami/redis -f $(PWD)/k8s/redis/values.yml

run-helm-uninstall-redis: ## Uninstall redis server in minikube
	helm uninstall fr-redis

export-redis-password: ## Export redis password
	@echo "export REDIS_PASSWORD=$(shell kubectl get secret --namespace default fr-redis -o jsonpath="{.data.redis-password}" | base64 --decode)"

RANDOM ?= `head -128 /dev/urandom | cksum | cut -d ' ' -f1`
create-redis-client-pod: ## Create redis client pod
	kubectl run --namespace default fr-redis-client-$(RANDOM) --rm --tty -i --restart='Never' --env REDIS_PASSWORD=$(shell kubectl get secret --namespace default fr-redis -o jsonpath="{.data.redis-password}" | base64 --decode) --image docker.io/bitnami/redis:6.0.9-debian-10-r0 -- bash

connect-redis-client-pod: export-redis-password create-redis-client-pod ## Connect to redis client pod
	kubectl exec --tty -i fr-redis-client-$(RANDOM) --namespace default -- bash
