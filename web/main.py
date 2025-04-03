from redis.cluster import RedisCluster
import os
import json
import face_recognition
import numpy as np
from wsgiref.simple_server import make_server

host = os.getenv('FR_APP_HOST') or "0.0.0.0"
port = os.getenv('FR_APP_PORT') or 5000

redis_host = os.getenv('FR_REDIS_HOST') or "127.0.0.1"
redis_port = os.getenv('FR_REDIS_PORT') or 6379

allow_origins = [
    "http://{host}:{port}".format(host=host, port=port),
    "http://localhost:5000",
    "http://localhost:8000",
]

def middleware(app):
    def handle_with_without_cors(environ, start_response):
        response_headers = [("Access-Control-Allow-Headers", "Content-Type"),
                            ("Access-Control-Allow-Methods", "GET, POST")]

        origin = environ.get("HTTP_ORIGIN");
        if origin in allow_origins:
            response_headers.append(("Access-Control-Allow-Origin", "*"))

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            status = "200 OK"
            start_response(status, response_headers)
            return []

        def _start_response(status, headers, exec_info=None):
            headers.extend(response_headers)
            return start_response(status, headers, exec_info)

        return app(environ, _start_response)

    return handle_with_without_cors

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    if path == '/':
        return handle_index(environ, start_response)
    elif path == '/embeddings':
        return handle_embeddings(environ, start_response)

    return handle_notfound(environ, start_response)

def handle_notfound(environ, start_response):
    status = "404 Not Found"
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)

    return [b"Not Found"]

def handle_embeddings(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        post_body = environ['wsgi.input'].read(content_length)

        face_encoding = json.loads(post_body.decode("utf-8"))
        face_encoding = np.array(face_encoding)

        name = query_embeddings(face_encoding)

        status = "200 OK"
        headers = [("Content-type", "application/json")]
        start_response(status, headers)

        return [json.dumps({"name": name}).encode("utf-8")]

    status = "405 Method Not Allowed"
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)

    return [b"Method Not Allowed"]

foo = [{"name": redis_host, "port": redis_port}]
r = RedisCluster(startup_nodes=foo, decode_responses=True)
def query_embeddings(face_encoding):
    base_query = "*=>[KNN 2 @embedding $vec_param AS vector_score]"
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
    name = "Unknow"
    if ret[0] != 0 and float(ret[2][1]) > 0.02:
        name = ret[1]

    return name

def handle_index(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        status = "200 OK"
        headers = [("Content-type", "text/plain; charset=utf-8")]
        start_response(status, headers)

        return [b"OK"]

    status = "405 Method Not Allowed"
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)

    return [b"Method Not Allowed"]

app = middleware(application)
with make_server(host, port, app) as server:
    print(f"Server started at http://{host}:{port}")
    server.serve_forever()
