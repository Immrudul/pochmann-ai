import cv2
import numpy as np
import joblib
import json

# Load model and label map
model = joblib.load("hsv_knn_model.joblib")
with open("hsv_label_map.json", "r") as f:
    label_map = json.load(f)
label_map = {int(k): v for k, v in label_map.items()}

# Grid parameters
GRID_SIZE = 3
BOX_SIZE = 40
MARGIN = 8  # for inner crop to avoid edges

def draw_grid(frame):
    h, w, _ = frame.shape
    start_x = w // 2 - BOX_SIZE * GRID_SIZE // 2
    start_y = h // 2 - BOX_SIZE * GRID_SIZE // 2
    for i in range(GRID_SIZE + 1):
        cv2.line(frame, (start_x + i * BOX_SIZE, start_y),
                 (start_x + i * BOX_SIZE, start_y + GRID_SIZE * BOX_SIZE), (0, 255, 0), 1)
        cv2.line(frame, (start_x, start_y + i * BOX_SIZE),
                 (start_x + GRID_SIZE * BOX_SIZE, start_y + i * BOX_SIZE), (0, 255, 0), 1)
    return start_x, start_y

def get_predictions(frame, start_x, start_y):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    predictions = []
    for row in range(GRID_SIZE):
        row_preds = []
        for col in range(GRID_SIZE):
            x = start_x + col * BOX_SIZE
            y = start_y + row * BOX_SIZE
            crop = hsv_frame[y+MARGIN:y+BOX_SIZE-MARGIN, x+MARGIN:x+BOX_SIZE-MARGIN]
            avg_hsv = np.mean(crop.reshape(-1, 3), axis=0).reshape(1, -1)
            pred = model.predict(avg_hsv)[0]
            row_preds.append(label_map[pred])
        predictions.append(row_preds)
    return predictions

# Start camera
cap = cv2.VideoCapture(1)
print("🎥 Press SPACE to predict 3x3 grid. ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    display = frame.copy()
    start_x, start_y = draw_grid(display)

    cv2.imshow("KNN 3x3 Predictor", display)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    if key == 32:  # SPACE
        predictions = get_predictions(frame, start_x, start_y)
        print("\n🎯 Predicted 3x3 Grid:")
        for row in predictions:
            print(" ".join(row))

cap.release()
cv2.destroyAllWindows()
