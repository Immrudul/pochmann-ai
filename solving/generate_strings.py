import json
import os

# Load scrambled_cube.json from one folder up in 'letter_classification'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "..", "letter_classification", "scrambled_cube.json")

with open(JSON_PATH, "r") as f:
    cube = json.load(f)

solved = ["B", "M"]
order = []
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"]

edge_letters = {
    "WB": "A",
    "WR": "B",
    "WG": "C",
    "WO": "D",

    "OW": "E",
    "OG": "F",
    "OY": "G",
    "OB": "H",

    "GW": "I",
    "GR": "J",
    "GY": "K",
    "GO": "L",

    "RW": "M",
    "RB": "N",
    "RY": "O",
    "RG": "P",
    
    "BW": "Q",
    "BO": "R",
    "BY": "S",
    "BR": "T",

    "YG": "U",
    "YR": "V",
    "YB": "W",
    "YO": "X",
}

locations = {
    "A": cube["U"][0][1],
    "B": cube["U"][1][2],
    "C": cube["U"][2][1],
    "D": cube["U"][1][0],

    "E": cube["L"][0][1],
    "F": cube["L"][1][2],
    "G": cube["L"][2][1],
    "H": cube["L"][1][0],

    "I": cube["F"][0][1],
    "J": cube["F"][1][2],
    "K": cube["F"][2][1],
    "L": cube["F"][1][0],

    "M": cube["R"][0][1],
    "N": cube["R"][1][2],
    "O": cube["R"][2][1],
    "P": cube["R"][1][0],

    "Q": cube["B"][0][1],
    "R": cube["B"][1][2],
    "S": cube["B"][2][1],
    "T": cube["B"][1][0],

    "U": cube["D"][0][1],
    "V": cube["D"][1][2],
    "W": cube["D"][2][1],
    "X": cube["D"][1][0]
}

def find_already_solved(cube, locations):
    if locations["A"] == "W" and locations["Q"] == "B":
        solved.append("A")
        solved.append("Q")
    if locations["B"] == "W" and locations["M"] == "R":
        solved.append("B")
        solved.append("M")
    if locations["C"] == "W" and locations["I"] == "G":
        solved.append("C")
        solved.append("I")
    if locations["D"] == "W" and locations["E"] == "O":
        solved.append("D")
        solved.append("E")

    if locations["U"] == "Y" and locations["K"] == "G":
        solved.append("U")
        solved.append("K")
    if locations["V"] == "Y" and locations["O"] == "R":
        solved.append("V")
        solved.append("O")
    if locations["W"] == "Y" and locations["S"] == "B":
        solved.append("W")
        solved.append("S")
    if locations["X"] == "Y" and locations["G"] == "O":
        solved.append("X")
        solved.append("G")

    if locations["L"] == "G" and locations["F"] == "O":
        solved.append("L")
        solved.append("F")
    
    if locations["J"] == "G" and locations["P"] == "R":
        solved.append("J")
        solved.append("P")

    if locations["T"] == "B" and locations["N"] == "R":
        solved.append("T")
        solved.append("N")

    if locations["R"] == "B" and locations["H"] == "O":
        solved.append("R")
        solved.append("H")

find_already_solved(cube, locations)
# print("already solved: ", solved)

correspondence = {
    "A": "Q", "Q": "A",
    "B": "M", "M": "B",
    "C": "I", "I": "C",
    "D": "E", "E": "D",
    "U": "K", "K": "U",
    "V": "O", "O": "V", 
    "W": "S", "S": "W",
    "X": "G", "G": "X",
    "L": "F", "F": "L",
    "J": "P", "P": "J",
    "T": "N", "N": "T",
    "R": "H", "H": "R"
}


c1 = locations["B"]
c2 = locations["M"]
piece = c1 + c2
letter = edge_letters[piece]
marked = None

count = 0

flag = True
tempflag = False

buffer_found_edge = False

while flag:

    if len(set(solved)) == 24:
        flag = False
        break

    if letter == marked:
        order.append(letter)
        solved.append(letter)
        solved.append(correspondence[letter])
        marked = None
        for i in letters:
            # print("checking: ", i)
            if (i not in solved) and (i != "M") and (i != "B"):
                letter = i
                # print("chose: ", letter)
                tempflag=True
                break

    if (letter == "B" or letter == "M") or (letter in order):
        # print('buffer found')
        buffer_found_edge = True
        for i in letters:
            # print("checking: ", i)
            if (i not in solved) and (i != "M") and (i != "B"):
                letter = i
                # print("chose: ", letter)
                tempflag=True
                break

    order.append(letter)
    solved.append(letter)
    solved.append(correspondence[letter])
    if tempflag:
        marked = correspondence[letter]
        solved.remove(correspondence[letter])
        tempflag=False
    c1 = locations[letter]
    c2 = locations[correspondence[letter]]
    piece = c1 + c2
    letter = edge_letters[piece]
    # print(letter)
    # count += 1
    # if count == 10:
    #     flag = False

order.pop()
if not buffer_found_edge:
    order.append(letter)

edge_order = order
print("Edge order: ", edge_order)


# ---------------------------------------------------------- Corner Pieces Below ----------------------------------------------------------


even_or_odd = len(order) % 2


solved = ["A", "E", "R"]
order = []

if even_or_odd == 1:
    
    temp = cube["U"][0][2]
    cube["U"][0][2] = cube["U"][2][2]
    cube["U"][2][2] = temp

    temp = cube["F"][0][2]
    cube["F"][0][2] = cube["R"][0][2]
    cube["R"][0][2] = temp

    temp = cube["R"][0][0]
    cube["R"][0][0] = cube["B"][0][0]
    cube["B"][0][0] = temp
    
    
corner_letters = {
    "WOB": "A",
    "WBR": "B",
    "WRG": "C",
    "WGO": "D",

    "OBW": "E",
    "OWG": "F",
    "OGY": "G",
    "OYB": "H",

    "GOW": "I",
    "GWR": "J",
    "GRY": "K",
    "GYO": "L",

    "RGW": "M",
    "RWB": "N",
    "RBY": "O",
    "RYG": "P",

    "BRW": "Q",
    "BWO": "R",
    "BOY": "S",
    "BYR": "T",

    "YOG": "U",
    "YGR": "V",
    "YRB": "W",
    "YBO": "X",
}


locations = {

    "A": cube["U"][0][0],
    "B": cube["U"][0][2],
    "C": cube["U"][2][2],
    "D": cube["U"][2][0],

    "E": cube["L"][0][0],
    "F": cube["L"][0][2],
    "G": cube["L"][2][2],
    "H": cube["L"][2][0],

    "I": cube["F"][0][0],
    "J": cube["F"][0][2],
    "K": cube["F"][2][2],
    "L": cube["F"][2][0],

    "M": cube["R"][0][0],
    "N": cube["R"][0][2],
    "O": cube["R"][2][2],
    "P": cube["R"][2][0],

    "Q": cube["B"][0][0],
    "R": cube["B"][0][2],
    "S": cube["B"][2][2],
    "T": cube["B"][2][0],

    "U": cube["D"][0][0],
    "V": cube["D"][0][2],
    "W": cube["D"][2][2],
    "X": cube["D"][2][0],
}


def find_already_solved_corners(cube, locations):
    if locations["A"] == "W" and locations["E"] == "O" and locations["R"] == "B":
        solved.append("A")
        solved.append("E")
        solved.append("R")
    if locations["B"] == "W" and locations["Q"] == "B" and locations["N"] == "R":
        solved.append("B")
        solved.append("Q")
        solved.append("N")
    if locations["C"] == "W" and locations["J"] == "G" and locations["M"] == "R":
        solved.append("C")
        solved.append("J")
        solved.append("M")
    if locations["D"] == "W" and locations["I"] == "G" and locations["F"] == "O":
        solved.append("D")
        solved.append("I")
        solved.append("F")
    
    if locations["U"] == "Y" and locations["G"] == "O" and locations["L"] == "G":
        solved.append("U")
        solved.append("G")
        solved.append("L")
    if locations["V"] == "Y" and locations["K"] == "G" and locations["P"] == "R":
        solved.append("V")
        solved.append("K")
        solved.append("P")
    if locations["W"] == "Y" and locations["O"] == "R" and locations["T"] == "B":
        solved.append("W")
        solved.append("O")
        solved.append("T")
    if locations["X"] == "Y" and locations["S"] == "B" and locations["H"] == "O":
        solved.append("X")
        solved.append("S")
        solved.append("H")

find_already_solved_corners(cube, locations)

correspondence = {
    "A": ["E", "R"], "E": ["A", "R"], "R": ["A", "E"],
    "B": ["Q", "N"], "Q": ["B", "N"], "N": ["B", "Q"],
    "C": ["J", "M"], "J": ["C", "M"], "M": ["C", "J"],
    "D": ["I", "F"], "I": ["D", "F"], "F": ["D", "I"],
    "U": ["G", "L"], "G": ["U", "L"], "L": ["U", "G"],
    "V": ["K", "P"], "K": ["V", "P"], "P": ["V", "K"],
    "W": ["O", "T"], "O": ["W", "T"], "T": ["W", "O"],
    "X": ["S", "H"], "S": ["X", "H"], "H": ["X", "S"]
}

c1 = locations["E"]
c2 = locations["R"] 
c3 = locations["A"]
piece = c1 + c2 + c3
letter = corner_letters[piece]
marked = None
buffer_found = False

# print(piece)
# print(letter)

count = 0

flag = True
tempflag = False

while flag:
    if len(set(solved)) == 24:
        flag = False
        break

    if letter == marked:
        order.append(letter)
        solved.append(letter)
        solved.extend(correspondence[letter])
        marked = None
        for i in letters:
            if (i not in solved) and (i != "A") and (i != "E") and (i != "R"):
                letter = i
                # print("chose: ", letter)
                tempflag = True
                break

    if (letter == "A") or (letter == "E") or (letter == "R") or (letter in order):
        print("buffer found")
        buffer_found = True
        for i in letters:
            if (i not in solved) and (i != "A") and (i != "E") and (i != "R"):
                letter = i
                # print("chose: ", letter)
                tempflag = True
                break


    order.append(letter)
    solved.append(letter)
    solved.extend(correspondence[letter])
    if tempflag:
        marked = correspondence[letter][0]  # Mark the first corresponding piece
        # print("marked: ", marked)
        solved.remove(correspondence[letter][0])
        tempflag = False


    # print("this is the letter: ", letter)
    c1 = locations[letter]
    c2 = locations[correspondence[letter][0]]
    c3 = locations[correspondence[letter][1]]
    piece = c1 + c2 + c3
    
    # Check if the piece exists, if not try swapping c2 and c3
    if piece not in corner_letters:
        piece = c1 + c3 + c2
    #     print("swapped piece: ", c1, c3, c2)
    # print("this is the piece: ", piece)
    letter = corner_letters[piece]
    # print(letter)
    # print(piece)
    # count += 1
    # if count == 6:
    #     flag = False


if not buffer_found:
    order.append(letter)

corner_order = order
print("Corner order: ", corner_order)


# ANS = U. N, M, S, P, O, E

output_data = {
    "edge_order": edge_order,
    "corner_order": corner_order
}

OUTPUT_PATH = os.path.join(BASE_DIR, "cube_solution_order.json")
with open(OUTPUT_PATH, "w") as f:
    json.dump(output_data, f, indent=4)

print(f"\nExported to {OUTPUT_PATH}")