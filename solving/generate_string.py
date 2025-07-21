cube = {
    "F": [
        ["B", "B", "W"],
        ["R", "G", "R"],
        ["G", "G", "W"]
    ],
    "R": [
        ["O", "W", "G"],
        ["Y", "R", "W"],
        ["O", "W", "Y"]
    ],
    "L": [
        ["W", "W", "O"],
        ["R", "O", "G"],
        ["G", "G", "O"]
    ],
    "B": [
        ["Y", "O", "B"],
        ["G", "B", "B"],
        ["R", "B", "R"]
    ],
    "U": [
        ["R", "Y", "R"],
        ["R", "W", "B"],
        ["Y", "Y", "G"]
    ],
    "D": [
        ["Y", "O", "B"],
        ["Y", "Y", "O"],
        ["W", "O", "B"]
    ]
}

solved = {}

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

def find_already_solved(cube):
    if cube["U"][0][1] == "W" and cube["B"][0][1] == "B":
        solved.append("A")
        solved.append("Q")
    if cube["U"][1][2] == "W" and cube["R"][0][1] == "R":
        solved.append("B")
        solved.append("M")
    if cube["U"][2][1] == "W" and cube["F"][0][1] == "G":
        solved.append("C")
        solved.append("I")
    if cube["U"][1][0] == "W" and cube["L"][0][1] == "O":
        solved.append("D")
        solved.append("E")

    if cube["D"][0][1] == "Y" and cube["F"][2][1] == "G":
        solved.append("U")
        solved.append("K")
    if cube["D"][1][2] == "Y" and cube["R"][2][1] == "R":
        solved.append("V")
        solved.append("O")
    if cube["D"][2][1] == "Y" and cube["B"][2][1] == "B":
        solved.append("W")
        solved.append("S")
    if cube["D"][1][0] == "Y" and cube["L"][2][1] == "O":
        solved.append("X")
        solved.append("G")

    if cube["F"][1][0] == "G" and cube["L"][1][2] == "O":
        solved.append("L")
        solved.append("F")
    
    if cube["F"][1][2] == "G" and cube["R"][1][0] == "R":
        solved.append("J")
        solved.append("P")

    if cube["B"][1][0] == "B" and cube["R"][1][2] == "R":
        solved.append("T")
        solved.append("N")

    if cube["B"][1][2] == "B" and cube["L"][1][0] == "O":
        solved.append("R")
        solved.append("H")




def generate_string(cube):
    if (cube["U"][1][2] == "R" and cube["R"][0][1] == "W") or (cube["U"][1][2] == "W" and cube["R"][0][1] == "R"):
        print('buffer piece found')
    else:
        print('no buffer piece found')


generate_string(cube)
