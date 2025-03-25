import os
import glob
import redis
import numpy as np
import face_recognition
from pathlib import Path

r = redis.Redis(host='172.17.0.1', port=6379, decode_responses=True)

for f in glob.glob(os.path.join("photos/", "*.jpg")):
    image = face_recognition.load_image_file(f)
    face_encoding = face_recognition.face_encodings(image)[0]
    face_encoding_float32 = np.array(face_encoding, dtype=np.float32)
    r.hset(Path(f).stem, mapping={"embedding": face_encoding_float32.tobytes()})
