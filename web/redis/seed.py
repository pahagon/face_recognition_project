import os
import glob
import redis
import numpy as np
import face_recognition
from pathlib import Path

redis_host = os.getenv('FC_REDIS_HOST')
redis_port = os.getenv('FC_REDIS_PORT')
redis_password = os.getenv('FC_REDIS_PASSWORD')

# conecta ao Redis local (com RediSearch)
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True,
    password=redis_password,
)

for f in glob.glob(os.path.join("photos/", "*.jpg")):
    image = face_recognition.load_image_file(f)
    face_encoding = face_recognition.face_encodings(image)[0]
    face_encoding_float32 = np.array(face_encoding, dtype=np.float32)
    redis_client.hset(
        Path(f).stem,
        mapping={"embedding": face_encoding_float32.tobytes()}
    )
