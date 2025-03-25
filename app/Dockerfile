FROM face-recognition-base:latest

RUN apt-get update && \
    apt-get install -y \
    python3-opencv \
    libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
