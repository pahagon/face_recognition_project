# Usa uma imagem Python com base no Debian
FROM python:3.10-slim

# Instala as dependências necessárias para o OpenCV
RUN apt-get update && \
    apt-get install -y python3-opencv libgl1-mesa-glx  && \
    rm -rf /var/lib/apt/lists/*

# Instala o OpenCV para Python
RUN pip install opencv-python

# Copia o script Python para dentro do contêiner
WORKDIR /app
COPY main.py /app/

# Comando padrão para iniciar o script
CMD ["python", "main.py"]
