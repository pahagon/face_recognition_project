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
    query_vector = face_encoding_float32.tobytes()
    query_params = {"vec_param": query_vector}
    ret = redis_client.execute_command(
        "FT.SEARCH", "idx:embeddings",
        "*=>[KNN 4 @embedding $vec_param AS vector_score]",
        "PARAMS", "2", "vec_param", query_vector,
        "RETURN", "1", "vector_score",
        "SORTBY", "vector_score",
        "DIALECT", "2"
    )
    print(ret)
