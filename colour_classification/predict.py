import cv2
import numpy as np
import joblib
import json

model = joblib.load("hsv_knn_model.joblib")
with open("hsv_label_map.json", "r") as f:
    label_map = json.load(f)
label_map = {int(k): v for k, v in label_map.items()}  # keys as ints

BOX_SIZE = 40

cap = cv2.VideoCapture(1)
print("🎥 Press SPACE to predict center sticker color. ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    display = frame.copy()

    h, w, _ = frame.shape
    cx, cy = w // 2, h // 2
    top_left = (cx - BOX_SIZE // 2, cy - BOX_SIZE // 2)
    bottom_right = (cx + BOX_SIZE // 2, cy + BOX_SIZE // 2)
    cv2.rectangle(display, top_left, bottom_right, (0, 255, 0), 2)

    cv2.imshow("KNN Color Predictor", display)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

    if key == 32:  # SPACE
        crop = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        avg_hsv = np.mean(hsv.reshape(-1, 3), axis=0).reshape(1, -1)

        prediction = model.predict(avg_hsv)
        predicted_label = label_map[prediction[0]]

        print(f"🎯 Predicted color: {predicted_label}")

cap.release()
cv2.destroyAllWindows()
