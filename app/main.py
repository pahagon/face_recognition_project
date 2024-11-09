import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a webcam")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar o quadro")
            break

        cv2.imshow("Feed da Webcam - Original", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
