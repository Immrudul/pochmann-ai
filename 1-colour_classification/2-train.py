import os
import cv2
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

dataset_dir = "./datasetnight"
output_model_path = "hsv_knn_model.joblib"
label_map_path = "hsv_label_map.json"

X = []  # HSV features
y = []  # Labels

label_map = {}  # e.g., 0 -> 'W'
label_counter = 0

for label_folder in sorted(os.listdir(dataset_dir)):
    folder_path = os.path.join(dataset_dir, label_folder)
    if not os.path.isdir(folder_path):
        continue

    # Assign integer class
    if label_folder not in label_map.values():
        label_map[label_counter] = label_folder
        label_id = label_counter
        label_counter += 1
    else:
        label_id = list(label_map.keys())[list(label_map.values()).index(label_folder)]

    for file in os.listdir(folder_path):
        path = os.path.join(folder_path, file)
        img = cv2.imread(path)
        if img is None:
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        avg_hsv = np.mean(hsv.reshape(-1, 3), axis=0)  # 1x3
        X.append(avg_hsv)
        y.append(label_id)

# Train model
X = np.array(X)
y = np.array(y)

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

# Save model and label map
joblib.dump(model, output_model_path)
with open(label_map_path, 'w') as f:
    json.dump(label_map, f)

print(f"✅ Model saved to {output_model_path}")
print(f"✅ Label map: {label_map}")
