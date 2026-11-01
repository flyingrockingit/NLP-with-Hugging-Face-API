PETS = ["hamster", "rabbit", "parrot", "goldfish", "turtle", "puppy", "kitten", "guinea pig"]
MAX_FIXES = 2

TEST_SEARCHES = [
    ("hamstr", "hamster"),
    ("rabit", "rabbit"),
    ("parott", "parrot"),
    ("gold fish", "goldfish"),
    ("puppee", "puppy"),
    ("pig", "guinea pig"),
]

def edit_distance(a, b):
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        table[i][0] = i
    for j in range(len(b) + 1):
        table[0][j] = j
    # YOUR CODE HERE
    # Loop over i from 1 to len(a) and j from 1 to len(b).
    # The cost of changing a letter is 0 if a[i - 1] == b[j - 1], otherwise 1.
    # table[i][j] is the smallest of: the cell above + 1, the cell to the left + 1,
    # and the cell diagonally up-left + the cost.
    return 0

print("PART 1: Edit distance")
print(edit_distance("cat", "cut"), edit_distance("rabit", "rabbit"))

# ---------- PART 2: find the closest pet ----------
def closest(search):
    # YOUR CODE HERE
    # Make a list of (edit_distance(search, pet), pet) for every pet in PETS,
    # sort the list, and return its first item.
    return (0, "")

print("\nPART 2: Closest pet")
print(closest("parott"))

def did_you_mean(search):
    # YOUR CODE HERE
    # Get the closest pet. Return its name if its distance is at most MAX_FIXES,
    # otherwise return "no match".
    return "no match"

print("\nPART 3: Did you mean?")
print(did_you_mean("hamstr"), "|", did_you_mean("elephant"))

print("\nPART 4: Test all searches")
mistakes = 0
# YOUR CODE HERE
# For each (search, wanted) pair: get the answer from did_you_mean, add 1 to mistakes
# if it is not the wanted one, and print the answer and the search on one line.
# After the loop, print: Mistakes: <number> out of <total>
