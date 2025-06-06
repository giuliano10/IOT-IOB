import cv2
import numpy as np

def calcular_brilho(frame):
    # Converte para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Retorna a média de brilho
    return np.mean(gray)

# Abrir a câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera")
    exit()

print("Monitorando brilho... Pressione 'q' para sair")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o frame")
        break

    brilho = calcular_brilho(frame)
    print(f"Brilho atual: {brilho:.2f}")

    # Mostra o frame
    cv2.imshow('Camera', frame)

    # Verifica se a luz apagou (limite ajustável, ex: 10)
    if brilho < 15:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("Alerta", "Luz apagada detectada!", duration=5)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
