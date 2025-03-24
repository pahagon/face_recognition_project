import os
import glob
import json
import face_recognition
import numpy as np
from pathlib import Path
from wsgiref.simple_server import make_server

known_face_encodings = []
known_face_names = []
for f in glob.glob(os.path.join("photos/", "*.jpg")):
    image = face_recognition.load_image_file(f)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(Path(f).stem)

host = "0.0.0.0"
port = 5000

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

def query_embeddings(face_encoding):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)

    name = "Unknow"
    if matches[best_match_index]:
            name = known_face_names[best_match_index]

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
