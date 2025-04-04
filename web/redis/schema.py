import os
import redis
import numpy as np

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
redis_client.execute_command(
    "FT.CREATE", "idx:embeddings",
    "ON", "HASH",
    "SCHEMA",
    "embedding", "VECTOR", "FLAT", "6",  # FLAT é o método de indexação
    "TYPE", "FLOAT32",
    "DIM", 128,
    "DISTANCE_METRIC", "COSINE"
)
