FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y \
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
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY face_recognition/ /app/face_recognition/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
