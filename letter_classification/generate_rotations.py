import cv2
import numpy as np
import joblib
import json

# Load KNN model and label map
model = joblib.load("hsv_knn_model.joblib")
with open("hsv_label_map.json", "r") as f:
    label_map = {int(k): v for k, v in json.load(f).items()}
with open("scrambled_cube.json", "r") as f:
    scrambled_cube = json.load(f)

# Grid parameters
GRID_SIZE = 3
BOX_SIZE = 40
MARGIN = 8  # avoid sticker edges

def rotate_face(face, k):
    """Rotate 3x3 face 90° clockwise k times"""
    return np.rot90(np.array(face), k=-k).tolist()

def define_all_rotated():
    rotated_faces = {}

    for face_label, grid in scrambled_cube.items():
        for i in range(4):  # 0 to 3 rotations
            key = f"{face_label}{i+1}"
            rotated_faces[key] = rotate_face(grid, i)

    with open("scrambled_rotations.json", "w") as f:
        json.dump(rotated_faces, f, indent=2)
    print("✅ Saved all rotated faces to scrambled_rotations.json")

# Run immediately
define_all_rotated()
