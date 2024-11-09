# Nome da imagem e variáveis de versão
APP_IMAGE_NAME = opencv-webcam-app
.PHONY: xhost build run stop clean

# Alvo para construir a imagem da aplicação
build:
	@echo "Building Docker image for the application..."
	docker build -t $(APP_IMAGE_NAME):latest .

#Configurar Host para permiter acesso ao display X11
xhost:
	xhost +local:docker

# Instala as dependências e roda o script
run:
	docker run -it --rm --device=/dev/video0:/dev/video0  \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		$(APP_IMAGE_NAME)

run-without-img:
	docker run -it --rm --device=/dev/video0:/dev/video0  \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD)/main.py:/app/main.py \
		$(APP_IMAGE_NAME)

# Alvo para parar e remover contêineres
stop:
	@echo "Stopping and removing containers..."
	-docker stop $(APP_IMAGE_NAME)
	-docker rm $(APP_IMAGE_NAME)

# Alvo para limpar os volumes de dados e as imagens
clean: stop
	@echo "Cleaning up Docker volumes and images..."
	-docker rmi $(APP_IMAGE_NAME):latest
