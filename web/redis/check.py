import os
import glob
import redis
import numpy as np
import face_recognition
from pathlib import Path

r = redis.Redis(host='172.17.0.1', port=6379, decode_responses=True)
base_query = "*=>[KNN 2 @embedding $vec_param AS vector_score]"

for f in glob.glob(os.path.join("photos/", "*.jpg")):
    image = face_recognition.load_image_file(f)
    face_encoding = face_recognition.face_encodings(image)[0]
    face_encoding_float32 = np.array(face_encoding, dtype=np.float32)
    query_vector = face_encoding_float32.tobytes()
    query_params = {"vec_param": query_vector}
    ret = r.execute_command(
        "FT.SEARCH", "idx:embeddings",
        base_query,
        "PARAMS", "2", "vec_param", query_vector,
        "RETURN", "1", "vector_score",
        "SORTBY", "vector_score",
        "DIALECT", "2"
    )
    print(ret)
