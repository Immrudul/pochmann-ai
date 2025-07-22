cube = {
    "F": [
        ["G", "Y", "R"],
        ["G", "G", "W"],
        ["B", "O", "Y"]
    ],
    "R": [
        ["W", "R", "O"],
        ["B", "R", "B"],
        ["R", "G", "O"]
    ],
    "L": [
        ["Y", "G", "O"],
        ["Y", "O", "O"],
        ["Y", "O", "W"]
    ],
    "B": [
        ["B", "R", "O"],
        ["R", "B", "B"],
        ["B", "O", "R"]
    ],
    "U": [
        ["G", "W", "Y"],
        ["W", "W", "Y"],
        ["W", "G", "G"]
    ],
    "D": [
        ["R", "W", "B"],
        ["B", "Y", "R"],
        ["G", "Y", "W"]
    ]
}

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

find_already_solved(cube)
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


# Initialize with buffer piece
c1 = locations["B"]
c2 = locations["M"]
piece = c1 + c2
letter = edge_letters[piece]
marked = None

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
        solved.append(correspondence[letter])
        marked = None
        for i in letters:
            # print("checking: ", i)
            if (i not in solved) and (i != "M") and (i != "B"):
                letter = i
                print("chose: ", letter)
                tempflag=True
                break

    if (letter == "B" or letter == "M") or (letter in order):
        print('buffer found')
        for i in letters:
            # print("checking: ", i)
            if (i not in solved) and (i != "M") and (i != "B"):
                letter = i
                print("chose: ", letter)
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
print(order)
# print(solved)