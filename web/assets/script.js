const video = document.getElementById("video");
const overlay = document.getElementById("overlay");
const context = overlay.getContext("2d");

let detection = null;
let recognizedName = null;

function startVideo() {
    navigator.mediaDevices
        .getUserMedia({ video: {} })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((err) => console.error("Erro ao acessar a webcam:", err));
}

function loadModels() {
    const MODEL_URL = "https://cdn.jsdelivr.net/npm/@vladmandic/face-api@1.0.2/model/";
    faceapi.nets.ssdMobilenetv1.loadFromUri(MODEL_URL);
    faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
    faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
    console.log("Modelos carregados com sucesso.");
}

async function getFaceEmbedding() {
    detection = await faceapi.detectSingleFace(video).withFaceLandmarks().withFaceDescriptor();
    if (detection) {
        currentEmbedding = Object.values(detection.descriptor);
        sendEmbedding(currentEmbedding);
    } else {
        recognizedName = null;
    }
}

async function sendEmbedding(embedding) {
    try {
        const response = await fetch("http://localhost:5000/embeddings", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(embedding)
        });
        const result = await response.json();
        recognizedName = result.name;
    } catch (error) {
        console.error("Erro ao enviar o embedding:", error);
    }
}

function drawOverlay() {
    context.clearRect(0, 0, overlay.width, overlay.height);
    if (detection && recognizedName) {
      /*
        const { x, y, width, height } = detection.detection.box;
        const adjustedX = x;
        const adjustedY = y;

        context.beginPath();
        context.rect(adjustedX, adjustedY, 50, 50);
        context.lineWidth = 3;
        context.strokeStyle = "red";
        context.stroke();
      */
        context.fillStyle = "red";
        context.font = "16px Arial";
        context.fillText(recognizedName, 15, 15);
    }
}

function init() {
  loadModels();
  startVideo();

  setInterval(getFaceEmbedding, 5000);
  setInterval(drawOverlay, 100);
}

init();
