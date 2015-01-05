import itertools, os

WORD_FOLDER = "word_folder"
WORD_FILES = os.listdir(WORD_FOLDER)
nFiles = len(WORD_FILES)
print("Importing " + str(nFiles) + " text files")
full_paths = [os.path.join(os.getcwd(),WORD_FOLDER,file) for file in WORD_FILES]

words = set()
for WORD_FILE in full_paths:
    f = open(WORD_FILE,"r")
    words_ = set(f.read().rsplit())
    words = set.union(words,words_)

QUIT = False

def points(word):
    current_values = VALUES.copy()
    total = 0
    for letter in word:
        total += find_max(letter, current_values)
    return total

def find_max(letter, current_values):
    result = 0
    for (current_letter,current_value) in current_values:
        if (letter == current_letter):
            if current_value > result:
                result = current_value
    if result > 0:
        current_values.remove([letter,result])
    return result

def letters_and_values(user_input):
    vals = []
    for pair in zip(user_input, user_input[1:]+"1"):
        if pair[0].isalpha() and pair[1].isdigit():
            vals.append([pair[0],int(pair[1])])
        elif pair[0].isalpha()and not pair[1].isdigit():
            vals.append([pair[0],1])
    letters = ""
    for (letter,value) in vals:
        letters+=letter
    return (letters, vals)

while True:
    correct_input = False
    while not correct_input:
        user_input = input("Given letters and values: ")
        given_letters, VALUES = letters_and_values(user_input)
        
        if given_letters.lower() == "quit":
            print("Anagram Solver: stopping...")
            correct_input = True
            QUIT = True
 
        elif len(given_letters) > 9 or len(given_letters) < 1:
            print("From 1 to 9 letters!")
            
        else:
            correct_input = True
            
    if QUIT:
        break
    solutions = {}
    
    for nLetters in range(1,len(given_letters)+1):
        nCombinations = itertools.permutations(given_letters,nLetters)
        for new_word_tuple in nCombinations:
            new_word = ''.join(new_word_tuple)
            if (new_word in words) and (new_word not in solutions):
                solutions[new_word] = points(new_word)
                
    solns_by_points = sorted(solutions,key=solutions.get,reverse=True)
    for soln in solns_by_points[:5]:
        print(soln,points(soln)) #prints 5 best solutions and their point vals
