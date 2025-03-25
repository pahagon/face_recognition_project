import redis
import numpy as np

# conecta ao Redis local (com RediSearch)
r = redis.Redis(host='172.17.0.1', port=6379, decode_responses=True)

# cria índice no RediSearch
schema = {
    "embedding": {
        "type": "VECTOR",
        "TYPE": "FLOAT32",
        "DIM": 128,
        "DISTANCE_METRIC": "COSINE"
    }
}

# Comando FT.CREATE para RediSearch (exemplo)
r.execute_command(
    "FT.CREATE", "idx:embeddings",
    "ON", "HASH",
    "SCHEMA",
    "embedding", "VECTOR", "FLAT", "6",  # FLAT é o método de indexação
    "TYPE", "FLOAT32",
    "DIM", 128,
    "DISTANCE_METRIC", "COSINE"
)
