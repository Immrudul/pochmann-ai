import json
import os

# Get base directory of the current file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the JSON file located one directory up, inside "solving"
SOLUTION_JSON_PATH = os.path.join(BASE_DIR, "..", "solving", "cube_solution_order.json")

# Load the JSON file
with open(SOLUTION_JSON_PATH, "r") as f:
    solution_data = json.load(f)

# Extract the orders as lists
edge_order = solution_data.get("edge_order", [])
corner_order = solution_data.get("corner_order", [])

edge_moves = {
    "A": ["l2", "D'", "L2"],
    "C": ["l2", "D", "L2"],
    "D": [],
    "E": ["L", "dw'", "L"],
    "F": ["dw'", "L"],
    "G": ["L'", "dw'", "L"],
    "H": ["dw", "L'"],
    "I": ["l", "D'", "L2"],
    "J": ["dw2", "L"],
    "K": ["l", "D", "L2"],
    "L": ["L'"],
    "N": ["dw", "L"],
    "O": ["D2", "L'", "dw'", "L"],
    "P": ["dw'", "L'"],
    "Q": ["l'", "D", "L2"],
    "R": ["L"],
    "S": ["l'", "D'", "L2"],
    "T": ["dw2", "L'"],
    "U": ["D'", "L2"],
    "V": ["D2", "L2"],
    "W": ["D", "L2"],
    "X": ["L2"],
}

edge_moves_reversed = {
    "A": ["L2", "D", "l2"],
    "C": ["L2", "D'", "l2"],
    "D": [],
    "E": ["L'", "dw", "L'"],
    "F": ["L'", "dw"],
    "G": ["L'", "dw", "L"],
    "H": ["L", "dw'"],
    "I": ["L2", "D", "l'"],
    "J": ["L'", "dw2"],
    "K": ["L2", "D'", "l'"],
    "L": ["L"],
    "N": ["L'", "dw'"],
    "O": ["L'", "dw", "L", "D2"],
    "P": ["L", "dw"],
    "Q": ["L2", "D'", "l"],
    "R": ["L'"],
    "S": ["L2", "D", "l"],
    "T": ["L", "dw2"],
    "U": ["L2", "D"],
    "V": ["L2", "D2"],
    "W": ["L2", "D'"],
    "X": ["L2"],
}

corner_moves = {
    "B": ["R2"],
    "C": ["F2", "D"],
    "D": ["F2"],
    "F": ["F'", "D"],
    "G": ["F'"],
    "H": ["D'", "R"],
    "I": ["F", "R'"],
    "J": ["R'"],
    "K": ["F'", "R'"],
    "L": ["F2", "R'"],
    "M": ["F"],
    "N": ["R'", "F"],
    "O": ["R2", "F"],
    "P": ["R", "F"],
    "Q": ["R", "D'"],
    "S": ["D", "F'"],
    "T": ["R"],
    "U": ["D"],
    "V": [],
    "W": ["D'"],
    "X": ["D2"],
}


corner_moves_reversed = {
    "B": ["R2"],
    "C": ["D'", "F2"],
    "D": ["F2"],
    "F": ["D'", "F"],
    "G": ["F"],
    "H": ["R'", "D"],
    "I": ["R", "F'"],
    "J": ["R"],
    "K": ["R", "F"],
    "L": ["R", "F2"],
    "M": ["F'"],
    "N": ["F'", "R"],
    "O": ["F'", "R2"],
    "P": ["F'", "R'"],
    "Q": ["D", "R'"],
    "S": ["F", "D'"],
    "T": ["R'"],
    "U": ["D'"],
    "V": [],
    "W": ["D"],
    "X": ["D2"],
}


print("Edge order: ", edge_order)
print("Corner order: ", corner_order)

