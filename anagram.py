import itertools, os, sys

WORD_FOLDER = "word_folder" # Folder name where .txt files should be kept
N_SOLUTIONS = 5 # How many best solutions to print.

def create_word_set():
    word_file_names = os.listdir(WORD_FOLDER)
    
    word_files = [os.path.join(os.getcwd(),WORD_FOLDER,file_name) for file_name in word_file_names]
    
    word_set = set()
    for word_file in word_files:
        if word_file.endswith(".txt"):
            f = open(word_file,"r")
            new_words = set(f.read().rsplit())
            word_set = word_set | new_words
    if len(word_set) == 0:
        print(".txt files should be added to /%s directory" % (WORD_FOLDER))
        sys.exit()
    print("Imported %s word(s) from %s files" % (len(word_set),len(word_files)))
    return word_set

def evaluate_word(word): #, free_values):
    word_value = 0
    free_values = VALUES.copy()
    #print (free_values)
    for letter in word:
        word_value += evaluate_letter(letter, free_values)
    return word_value

def evaluate_letter(letter, free_values):
    value = 0
    for (free_letter,free_value) in free_values:
        if (letter == free_letter):
            if free_value > value:
                value = free_value
    if value > 0:
        free_values.remove([letter,value])
    return value

def letters_and_values(user_input):
    vals = list()
    letters = str()
    user_input += "1"   #For being able to use zip() and not ignore the
                        #last symbol in user_input in case it is a letter.
    #Turns user input into a list (for example: [['a',1],['b',2],...]).
    for (fst,snd) in zip(user_input, user_input[1:]):
        if fst.isalpha():
            letters+=fst
            if snd.isdigit():
                vals.append([fst,int(snd)])
            else:
                vals.append([fst,1])
    return (letters, vals)

def wait_for_input():
    global VALUES
    correct_input = False
    while not correct_input:
        user_input = input("Given letters and values: ")
        letters, VALUES = letters_and_values(user_input)
        if letters.lower() == "quit":
            print("Anagramino: stopping...")
            sys.exit()
        if (1 <= len(letters) <= 9):
            correct_input = True
        else:
            print("Enter 1-9 letters!")
    return letters

def solve(letters):
    solutions = dict()
    for nLetters in range(1,len(letters)+1):
        combinations = itertools.permutations(letters,nLetters)
        for new_word_tuple in combinations:
            new_word = ''.join(new_word_tuple)
            if (new_word in words) and (new_word not in solutions):
                solutions[new_word] = evaluate_word(new_word)
    return solutions

def print_best_solutions(solutions):
    solutions_by_points = sorted(solutions,key=solutions.get,reverse=True)
    for solution in solutions_by_points[:N_SOLUTIONS]:
        print(solution,evaluate_word(solution))

####MAIN PROGRAM####        
words = create_word_set()
while True:
    letters = wait_for_input()
    solutions = solve(letters)
    print_best_solutions(solutions) #prints N_SOLUTIONS best solutions and their point values
