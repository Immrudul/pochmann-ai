import cv2
import numpy as np
import joblib
import json
import os

# Load KNN model and label map
base_dir = os.path.join(os.path.dirname(__file__), "..", "colour_classification")
model_path = os.path.join(base_dir, "hsv_knn_model.joblib")
label_map_path = os.path.join(base_dir, "hsv_label_map.json")

# Load model and label map from colour_classification
model = joblib.load(model_path)
with open(label_map_path, "r") as f:
    label_map = {int(k): v for k, v in json.load(f).items()}

# Load scrambled_rotations.json from current directory
with open("scrambled_rotations.json", "r") as f:
    rotated_faces = json.load(f)

# Load mapping.json (letter mappings for each face orientation)
with open("mapping.json", "r") as f:
    letter_map = json.load(f)

# Grid parameters
GRID_SIZE = 3
BOX_SIZE = 40
MARGIN = 8  # avoid sticker edges

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

def compare_with_rotations(predicted_grid):
    max_match = 0
    best_match = None

    for face, rotation in rotated_faces.items():
        match_count = sum(
            predicted_grid[i][j] == rotation[i][j]
            for i in range(3) for j in range(3)
        )
        if match_count > max_match:
            max_match = match_count
            best_match = face

    return best_match if max_match >= 6 else None, max_match

def overlay_letters(frame, start_x, start_y, letters):
    """Overlay top, right, bottom, left edge letters on the grid."""
    positions = {
        "top":    (0, 1),
        "right":  (1, 2),
        "bottom": (2, 1),
        "left":   (1, 0)
    }

    for label, pos in zip(letters, ["top", "right", "bottom", "left"]):
        i, j = positions[pos]
        x = start_x + j * BOX_SIZE + 10
        y = start_y + i * BOX_SIZE + 30
        cv2.putText(frame, label, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# Start camera
cap = cv2.VideoCapture(1)
print("🎥 Press SPACE to predict 3x3 grid. ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

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

        best_match, match_count = compare_with_rotations(predictions)
        if best_match:
            print(f"✅ Detected orientation: {best_match} ({match_count}/9 match)")
            if best_match in letter_map:
                letters = letter_map[best_match]  # List of 4 letters
                overlay_letters(display, start_x, start_y, letters)
                # Show overlay immediately
                cv2.imshow("KNN 3x3 Predictor", display)
                cv2.waitKey(3500)  # Wait 1 second to see the letters
            else:
                print(f"⚠️ No letter mapping found for {best_match}")
        else:
            print("❌ 6/9 not confirmed, please try again.")

cap.release()
cv2.destroyAllWindows()
