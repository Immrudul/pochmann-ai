import cv2
import os
import numpy as np
from datetime import datetime

# Dataset folder
SAVE_DIR = "dataset"
os.makedirs(SAVE_DIR, exist_ok=True)
for label in ['W', 'Y', 'R', 'O', 'G', 'B']:
    os.makedirs(os.path.join(SAVE_DIR, label), exist_ok=True)

# Grid parameters
CROP_SIZE = 32
GRID_SIZE = 3
BOX_SIZE = 40  # For visualization

def draw_grid(frame):
    h, w, _ = frame.shape
    start_x = w // 2 - BOX_SIZE * GRID_SIZE // 2
    start_y = h // 2 - BOX_SIZE * GRID_SIZE // 2
    for i in range(GRID_SIZE + 1):
        # Vertical lines
        cv2.line(frame, (start_x + i * BOX_SIZE, start_y),
                 (start_x + i * BOX_SIZE, start_y + GRID_SIZE * BOX_SIZE), (0, 255, 0), 1)
        # Horizontal lines
        cv2.line(frame, (start_x, start_y + i * BOX_SIZE),
                 (start_x + GRID_SIZE * BOX_SIZE, start_y + i * BOX_SIZE), (0, 255, 0), 1)
    return start_x, start_y

def get_grid_crops(frame, start_x, start_y):
    crops = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = start_x + col * BOX_SIZE
            y = start_y + row * BOX_SIZE
            crop = frame[y:y+BOX_SIZE, x:x+BOX_SIZE]
            crop = cv2.resize(crop, (CROP_SIZE, CROP_SIZE))
            crops.append(crop)
    return crops

cap = cv2.VideoCapture(1)
print("Press W/Y/R/O/G/B to label all 9 stickers currently in view.")
print("Press ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for user-friendly display
    frame = cv2.flip(frame, 1)
    display_frame = frame.copy()

    start_x, start_y = draw_grid(display_frame)
    cv2.putText(display_frame, "Center cube face in grid & press key (W/Y/R/O/G/B)", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Label Cube Face", display_frame)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break

    if chr(key).upper() in ['W', 'Y', 'R', 'O', 'G', 'B']:
        label = chr(key).upper()
        crops = get_grid_crops(frame, start_x, start_y)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for i, crop in enumerate(crops):
            filename = os.path.join(SAVE_DIR, label, f"{label}_{timestamp}_{i}.png")
            cv2.imwrite(filename, crop)
        print(f"✅ Saved 9 images to '{label}/'")

cap.release()
cv2.destroyAllWindows()
