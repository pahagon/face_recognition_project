# Nome da imagem e variáveis de versão
APP_IMAGE_NAME = opencv-webcam-app
.PHONY: build-base-img build xhost run run-dev run-preprocess-photos stop clean

build-base-img:
	@echo "Building Base Docker image for application..."
	docker run --name opencv-webcam-base-tmp  python:3.10-slim \
    bash -c " apt-get update && \
    apt-get install -y python3-opencv \
    libgl1-mesa-glx \
    cmake \
    libboost-all-dev \
    build-essential \
    libopenblas-dev \
    libx11-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev && \
    rm -rf /var/lib/apt/lists/*" && \
	docker commit opencv-webcam-base-tmp opencv-webcam-base:latest && \
    docker rm opencv-webcam-base-tmp

# Alvo para construir a imagem da aplicação
build:
	@echo "Building Docker image for the application..."
	docker build -t $(APP_IMAGE_NAME):latest .

#Configurar Host para permiter acesso ao display X11
xhost:
	xhost +local:docker

run:
	docker run -it --rm --device=/dev/video0:/dev/video0  \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		$(APP_IMAGE_NAME)

run-dev:
	docker run -it --rm --device=/dev/video0:/dev/video0  \
		-e DISPLAY=$(DISPLAY) \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-v $(PWD)/face_recognition:/app/face_recognition \
		-v $(PWD)/photos:/app/photos \
		-v $(PWD)/main.py:/app/main.py \
		$(APP_IMAGE_NAME)

run-preprocess-photos:
		docker run -it --rm \
		-v $(PWD)/photos:/app/photos \
		-v $(PWD)/preprocess_photo.py:/app/preprocess_photo.py \
		$(APP_IMAGE_NAME) bash -c "python preprocess_photo.py"

# Alvo para parar e remover contêineres
stop:
	@echo "Stopping and removing containers..."
	docker stop $(APP_IMAGE_NAME)
	docker rm $(APP_IMAGE_NAME)

# Alvo para limpar os volumes de dados e as imagens
clean: stop
	@echo "Cleaning up Docker volumes and images..."
	docker rmi $(APP_IMAGE_NAME):latest
