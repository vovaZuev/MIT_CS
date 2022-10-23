# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for char in secret_word:
        if char not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = ""
    
    for char in secret_word:
        if char in letters_guessed:
            result += char
        else:
            result += "_ "
    return result


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    new_list = ""
    
    for char in string.ascii_lowercase:
        if char not in letters_guessed:
            new_list += char
    return new_list
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    def get_score(secret_word, remaining_guesses):
        unique_letters_list = []
        for char in secret_word:
            if char not in unique_letters_list:
                unique_letters_list.append(char)
        return remaining_guesses * len(unique_letters_list)
        
    game_is_over = False
    letters_guessed = []
    num_guesses = 6
    num_warnings = 3
    vowels = ['a','e','i','o','u']
    dashes = "------------------------"
    print("Welcome to the game Hangman!")
    print("I am thinking of a secret word that is", len(secret_word),"letters long.")
    print("You have", num_warnings,"warnings left.")
    while not game_is_over:
        print(dashes)
        print("You have", num_guesses,"guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        
        user_input = input("Please guess a letter: ")
        if str.isalpha(user_input) and len(user_input) == 1:
            user_input = str.lower(user_input)
            if user_input in secret_word:
                if user_input in letters_guessed:
                    num_warnings -= 1
                    if num_warnings < 0:
                        num_guesses -= 1
                        num_warnings = 3
                        print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
                    else:
                        print("Oops! You've already guessed that letter. You now have", num_warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                else:
                    letters_guessed.append(user_input)
                    print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
                    if is_word_guessed(secret_word, letters_guessed):
                        game_is_over = True
                        print(dashes)
                        print("Congratulations, you won!")
                        print("Your total score for this game is:", get_score(secret_word, num_guesses))
                        
            else:
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                if user_input in vowels:
                    num_guesses -= 2
                else:
                    num_guesses -= 1
                if num_guesses <= 0:
                    game_is_over = True
                    print(dashes)
                    print("Sorry, you ran out of guesses. The word was", secret_word)
                
        else:
            num_warnings -= 1
            if num_warnings < 0:
                num_guesses -= 1
                num_warnings = 3
                print("Oops! That is not a valid letter. You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! That is not a valid letter. You have", num_warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
            
    

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_stripped = my_word.replace(" ", "")
    opened_letters = []
    
    for char in my_word_stripped:
        if char != "_":
            opened_letters.append(char)
    
    if len(other_word) == len(my_word_stripped):
        for i in range(len(other_word)):
            if my_word_stripped[i] == "_":
                if other_word[i] in opened_letters:
                    return False
                else:
                    continue
            else:
                if my_word_stripped[i] != other_word[i]:
                    return False
        return True
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = ""
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches += word + " "
    
    if len(matches) > 0:
        print(matches)
    else:
        print("No matches found.")
    return None


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    def get_score(secret_word, remaining_guesses):
        unique_letters_list = []
        for char in secret_word:
            if char not in unique_letters_list:
                unique_letters_list.append(char)
        return remaining_guesses * len(unique_letters_list)
        
    game_is_over = False
    letters_guessed = []
    num_guesses = 6
    num_warnings = 3
    vowels = ['a','e','i','o','u']
    dashes = "------------------------"
    print("Welcome to the game Hangman!")
    print("I am thinking of a secret word that is", len(secret_word),"letters long.")
    print("You have", num_warnings,"warnings left.")
    while not game_is_over:
        print(dashes)
        print("You have", num_guesses,"guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        
        user_input = input("Please guess a letter: ")
        if str.isalpha(user_input) and len(user_input) == 1:
            user_input = str.lower(user_input)
            if user_input in secret_word:
                if user_input in letters_guessed:
                    num_warnings -= 1
                    if num_warnings < 0:
                        num_guesses -= 1
                        num_warnings = 3
                        print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
                    else:
                        print("Oops! You've already guessed that letter. You now have", num_warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                else:
                    letters_guessed.append(user_input)
                    print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
                    if is_word_guessed(secret_word, letters_guessed):
                        game_is_over = True
                        print(dashes)
                        print("Congratulations, you won!")
                        print("Your total score for this game is:", get_score(secret_word, num_guesses))
            else:
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                if user_input in vowels:
                    num_guesses -= 2
                else:
                    num_guesses -= 1
                if num_guesses <= 0:
                    game_is_over = True
                    print(dashes)
                    print("Sorry, you ran out of guesses. The word was", secret_word)
        elif user_input == "*":
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))        
        else:
            num_warnings -= 1
            if num_warnings < 0:
                num_guesses -= 1
                num_warnings = 3
                print("Oops! That is not a valid letter. You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! That is not a valid letter. You have", num_warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
#     # pass

#     # To test part 2, comment out the pass line above and
#     # uncomment the following two lines.
    
#     secret_word = choose_word(wordlist)
#     hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
