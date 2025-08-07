import cv2
import numpy as np
import joblib
import json
import os

# === Load KNN model and label map ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "1-colour_classification", "hsv_knn_model.joblib")
LABEL_MAP_PATH = os.path.join(BASE_DIR, "..", "1-colour_classification", "hsv_label_map.json")

model = joblib.load(MODEL_PATH)
with open(LABEL_MAP_PATH, "r") as f:
    label_map = json.load(f)
label_map = {int(k): v for k, v in label_map.items()}

# === Grid settings ===
GRID_SIZE = 3
BOX_SIZE = 50
MARGIN = 8

face_order = [
    ("F", "Show GREEN center face with WHITE on top"),
    ("R", "Show RED center face with WHITE on top"),
    ("L", "Show ORANGE center face with WHITE on top"),
    ("B", "Show BLUE center face with WHITE on top"),
    ("U", "Show WHITE center face with GREEN on top"),
    ("D", "Show YELLOW center face with GREEN on top"),
]

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

def get_grid_predictions(frame, start_x, start_y):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    predictions = []
    for row in range(GRID_SIZE):
        row_colors = []
        for col in range(GRID_SIZE):
            x = start_x + col * BOX_SIZE
            y = start_y + row * BOX_SIZE
            crop = hsv_frame[y+MARGIN:y+BOX_SIZE-MARGIN, x+MARGIN:x+BOX_SIZE-MARGIN]
            avg_hsv = np.mean(crop.reshape(-1, 3), axis=0).reshape(1, -1)
            pred = model.predict(avg_hsv)[0]
            row_colors.append(label_map[pred])
        predictions.append(row_colors)
    return predictions

def print_2d_cube(cube_state):
    def row(face, r): return " ".join(cube_state[face][r])

    print("\n🧊 Final 2D Cube Mapping:\n")
    for r in range(3):
        print("      " + row("U", r))
    for r in range(3):
        print(row("L", r) + " " + row("F", r) + " " + row("R", r) + " " + row("B", r))
    for r in range(3):
        print("      " + row("D", r))
    print("\n✅ Mapping complete. Ready for algorithms.\n")

# === Camera & Main Capture Loop ===
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("❌ Failed to open camera.")
    exit()

cube_state = {}

for face_code, instruction in face_order:
    print(f"\n➡️  {instruction}")
    print("   Align the face in the 3x3 grid and press SPACE to capture.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame read failed.")
            break

        # frame = cv2.flip(frame, 1)
        display = frame.copy()
        start_x, start_y = draw_grid(display)

        cv2.putText(display, f"{instruction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(display, "Press SPACE to capture | ESC to exit", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.imshow("Rubik's Cube Mapper", display)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            print("❌ Exit requested.")
            cap.release()
            cv2.destroyAllWindows()
            exit()
        if key == 32:
            predictions = get_grid_predictions(frame, start_x, start_y)

            # Rotate WHITE face 180 degrees
            if face_code == "U":
                predictions = [row[::-1] for row in predictions[::-1]]

            cube_state[face_code] = predictions
            print(f"✅ Captured {face_code} face:")
            for row in predictions:
                print("   " + " ".join(row))
            break

cap.release()
cv2.destroyAllWindows()

# Print final cube state
print_2d_cube(cube_state)

# Assuming BASE_DIR and cube_state are already defined
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "scrambled_cube.json")

with open(output_path, "w") as f:
    json.dump(cube_state, f, indent=2)  # or use separators=(',', ':') for more compact
print(f"✅ Saved cube state to {output_path}")

# Generating rotations
def rotate_face(face, k):
    """Rotate 3x3 face 90° clockwise k times"""
    return np.rot90(np.array(face), k=-k).tolist()

def define_all_rotated():
    with open(output_path, "r") as f:
        scrambled_cube = json.load(f)

    rotated_faces = {}
    for face_label, grid in scrambled_cube.items():
        for i in range(4):  # 0 to 3 rotations
            key = f"{face_label}{i+1}"
            rotated_faces[key] = rotate_face(grid, i)

    output_rot_path = os.path.join(BASE_DIR, "scrambled_rotations.json")
    with open(output_rot_path, "w") as f:
        json.dump(rotated_faces, f, indent=2)
    print("✅ Saved all rotated faces to scrambled_rotations.json")

# Call after saving cube
define_all_rotated()