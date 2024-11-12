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
