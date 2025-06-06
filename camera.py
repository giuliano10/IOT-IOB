import cv2
import numpy as np
import mediapipe as mp
from win10toast import ToastNotifier


def calcular_brilho(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

# Inicializa o MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Inicializa a notificação
toaster = ToastNotifier()

# Abrir a câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera")
    exit()

print("Monitorando brilho e presença de rosto... Pressione 'q' para sair")

# Variável para evitar notificação contínua
luz_apagada = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o frame")
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image_rgb)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)

    brilho = calcular_brilho(frame)
    rosto_detectado = results.detections is not None
    print(f"Brilho atual: {brilho:.2f} | Rosto detectado: {'Sim' if rosto_detectado else 'Não'}")

    # Verifica se a luz acabou (brilho < limite) e notifica uma única vez
    if brilho < 15:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("Alerta", "Luz apagada detectada!", duration=5)

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
