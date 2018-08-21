"""
-------------------------------------------------------
finalwordblizy.py
A two player game that allows players
to guess a word based on a clue (the category) that
is being provided.

-------------------------------------------------------
"""

from random import randint
import random
import sys


show = []
vowels = ['a', 'e', 'i', 'o', 'u']
guessed = []

'''
Codes loadPuzzles and getRandomPuzzle copied from file provided by the Professor
loadPuzzles is used to read the file and separate the category (which is the clue) 
from the secret word. getRandomPuzzles allows us to randomize
the list within the file
'''


def loadPuzzles(filename='wordblitzclues.txt'):
    fileClues = open(filename, 'r')
    lisClues = []
    for line in fileClues:
        lisClues.append(line.rstrip())
    fileClues.close()
    return lisClues


def getRandomPuzzle(puzzleLis):
    randomIndex = random.randint(0, len(puzzleLis) - 1)
    puzzle = puzzleLis[randomIndex].split('\t')
    for extraTab in puzzle:
        if extraTab == '':
            puzzle.remove('')
    puzzleClue = puzzle[0]
    secretWord = puzzle[1]
    return puzzleClue, secretWord


'''
The start function collects information on the players,
it will only proceed with the game if there are two players
global variables used because player1 and player2 are accessed
multiple times by different functions
'''


def start():
    global player1
    global player2

    userselect = str(input("Are 2 players playing the game (Yes/No): "))
    if userselect == "No" or userselect == "no":
        game = str(input("Sorry, two players are needed to play this game"))
        startnow = False
    elif userselect == "Yes" or userselect == "yes":
        player1 = str(input("Enter the name of player one: "))
        player2 = str(input("Enter the name of player two: "))
        startnow = True
        puzzle(startnow)
    else:
        print("Sorry, that does not seem like one of the options.")


"""
through the puzzle function the game begins
"""


def puzzle(startnow):
    global secret
    puzzleLis = loadPuzzles()
    puzzleClue, secretWord = getRandomPuzzle(
        puzzleLis)
    clue = puzzleClue
    secret = secretWord
    secret = secret.lower()
    if startnow == True:
        main_function(secretWord, clue)


"""
the main function is the most important function in the code,
hence the 'main' function, it takes into account all of the conditions
that were provided such as the ability to spin, buy a vowel, solve for
the secret word and quit the game
"""


def main_function(secretWord, clue):
    global guess

    player1_ta = 0
    player1_ga = 0
    player2_ta = 0
    player2_ga = 0

    vowels = ['a', 'e', 'i', 'o', 'u']

    print("\n")
    print("Hello! Welcome to WordBlitz")
    print("\nCategory:" + clue)
    print("Guessed Letters: " + str(guessed))
    print(len(secretWord) * (" _ "))

    new_answer = (len(secretWord) * (" _ "))

    answer = list(secretWord)
    show.extend(answer)
    for i in range(len(show)):
        show[i] = "_"

    full = []
    full.extend(answer)

    active_game = True
    while active_game:

        p1_turn = True

        while p1_turn and full:

            print("\nHello " + str(player1))

            print("\nCategory:" + clue)
            print("Guessed Letters: " + str(guessed))
            print(new_answer)

            print(player1 + "'s turn account:" +
                  str(player1_ta) + " dollars.", end="       ")
            print(player2 + "'s turn account:" +
                  str(player2_ta) + " dollars.")
            print(player1 + "'s game account:" +
                  str(player1_ga) + " dollars.", end="       ")
            print(player2 + "'s game account:" +
                  str(player2_ga) + " dollars.")

            userselect = input(
                '''\n| 1: spin the wheel 
                   \n| 2: buy a vowel 
                   \n| 3: solve 
                   \n| 4: quit 
                   \n which option would you like to choose: ''')

            if userselect == "1":
                number = spin()
                print("Your number is: " + str(number))

                if number == 0:
                    print(
                        "The number you receive is 0. Unfortunately, you lose your money")
                    player1_ta = 0
                    p1_turn = False

                elif number == 21:
                    print(
                        "The number you receive is 21, unfortunately your turn is over.")
                    player1_ga = player1_ga + player1_ta
                    p1_turn = False

                else:
                    guess = input(
                        "What is your consonant would you like to guess: ")

                    while guess.lower() in vowels:
                        guess = input("Please choose a consonant: ")

                    guessed.append(guess)

                    startnow = guessing()

                    if startnow == True:

                        print("Congratulations, you get another turn.")


# the for loop is used to remove dashes and update the player on the letters
# they guessed correctly.

                        for i in range(len(answer)):

                            if answer[i] == guess.lower():
                                show[i] = guess.lower()

                                full.remove(guess)
                        new_answer = (" ".join(show))

                        update = secret.lower().count(guess.lower())
                        player1_ta = player1_ta + (int(update) * number)
                        print("You earned: $" + str(player1_ta) + " this round")

                    else:
                        print("No, try again")
                        player1_ta = player1_ta - number
                        player1_ga = player1_ga + player1_ta
                        player1_ta = 0
                        p1_turn = False

            if userselect == "2":

                guess = input(
                    "Alright, which vowel would you like to choose: ")

                while guess.lower() not in vowels:
                    guess = input("Please enter a vowel [AEIOU]: ")
                guessed.append(guess)
                # subtracts $25 from the players' account if they choose to
                # guess a vowel
                player1_ta = player1_ta - 25
                print(
                    "Your account has been charged $25, your remaining balance is $ " + str(player1_ta))

                startnow = vowels()

                if startnow == True:

                    print("Congratulations")

                    for i in range(len(answer)):
                        if answer[i] == guess:
                            show[i] = guess

                            full.remove(guess)
                    new_answer = (" ".join(show))

                else:
                    print("Sorry that's not there")
                    player1_ga = player1_ga + player1_ta
                    player1_ta = 0
                    p1_turn = False

            if userselect == "3":
                attempt_solve = input("Guess:")

                if attempt_solve.lower() == secret.lower():

                    print("Impressive, you are correct!")

                    update_dashes = new_answer.count("_")
                    update_dashes = (5 * update_dashes)
                    player1_ga = player1_ga + player1_ta
                    player1_ga = player1_ga + (update_dashes)
                    print("You Win $ " + str(update_dashes))
                    winner(player2_ga, player1_ga)

                else:
                    print("Sorry, that doesn't seem right!")
                    player1_ga = player1_ga + player1_ta
                    player1_ta = 0
                    p1_turn = False

            if userselect == "4":
                exit_game()
# Same thing repeats from player 1, but this time for player 2
        p2_turn = True

        while p2_turn and full:

            print("\nHello " + str(player2) +
                  " which option would you like to choose: ")
            print("\nCategory:" + clue)
            print("Guessed Letters: " + str(guessed))
            print(new_answer)

            print("Hello " + str(player2) +
                  " which option would you like to choose: ")
            print(player1 + "'s turn account:" +
                  str(player1_ta) + " dollars.", end="       ")
            print(player2 + "'s turn account:" +
                  str(player2_ta) + " dollars.")
            print(player1 + "'s game account:" +
                  str(player1_ga) + " dollars.", end="       ")
            print(player2 + "'s game account:" +
                  str(player2_ga) + " dollars.")

            userselect = input(
                '''\n| 1: spin the wheel 
                   \n| 2: buy a vowel 
                   \n| 3: solve 
                   \n| 4: quit 
                 \n which option would you like to choose: ''')

            if userselect == "1":
                number = spin()
                print("The number you receive is: " + str(number))

                if number == 0:
                    print(
                        "The number you receive is 0. Unfortunately you lose your money.")
                    player2_ta = 0
                    p2_turn = False

                elif number == 21:
                    print(
                        "The number you receive is 21, unfortunately your turn is over.")
                    player2_ga = player2_ga + player2_ta
                    player2_ta = 0
                    p2_turn = False

                else:
                    guess = input("Which consonant would you like to choose: ")

                    while guess.lower() in vowels:
                        guess = input("Choose a consonant, please try again: ")
                    guessed.append(guess)
                    startnow = guessing()

                    if startnow == True:

                        print("Correct!")

                        for i in range(len(answer)):
                            if answer[i] == guess.lower():
                                show[i] = guess.lower()
                                full.remove(guess)
                        new_answer = (" ".join(show))

                        occur = secret.lower().count(guess.lower())
                        player2_ta = player2_ta + (int(occur) * number)

                        print("You won: $" + str(player2_ta) + " this round")

                    else:
                        print("Try Again")
                        player2_ta = player2_ta - number
                        player2_ta = player2_ta + player2_ga
                        player2_ta = 0
                        p2_turn = False

            if userselect == "2":

                guess = input("Which vowel would you like to choose: ")

                while guess.lower() not in vowels:
                    guess = input("Please enter a vowel [AEIOU]: ")

                player2_ta = player2_ta - 25
                print(
                    "Your account has been charged $25, your remaining balance is $" + str(player2_ta))

                guessed.append(guess)
                startnow = vowels()

                if startnow == True:

                    print("Congratulations!")

                    for i in range(len(answer)):
                        if answer[i] == guess:
                            show[i] = guess
                            full.remove(guess)
                    new_answer = (" ".join(show))

                else:
                    print("Sorry that's not there")
                    player2_ga = player2_ga + player2_ta
                    player2_ta = 0
                    p2_turn = False

            if userselect == "3":
                attempt_solve = input("Guess: ")

                if attempt_solve.lower() == secret.lower():
                    print("Impressive! You are Correct")
                    update_dashes = new_answer.count("_")
                    update_dashes = (5 * update_dashes)
                    player2_ga = player2_ga + player2_ta
                    player2_ga = player2_ga + (update_dashes)
                    print("Congrats! You won $" + str(update_dashes))
                    winner(player2_ga, player1_ga)

                else:
                    print("Please try again.")
                    player2_ga = player2_ga + player2_ta
                    player2_ta = 0
                    p2_turn = False

            if userselect == "4":
                exit_game()

        if not full:
            this = True

            while this == True:
                player1_ga = player1_ga + player1_ta
                player2_ga = player2_ga + player2_ta
                winner(player2_ga, player1_ga)


'''
Allows the player to exit the game if they wish to
'''


def exit_game():
    print("Hope you'll play again! ")
    sys.exit()


'''
the winner function helps determine the winner of the game
it declares a winner if either all of the letters were
guessed or if the secret word was guessed

'''


def winner(player2_ga, player1_ga):

    print("\nThe word was guessed!")
    print(player1 + "'s game account:" +
          str(player1_ga) + " dollars.", end="       ")
    print(player2 + "'s game account:" +
          str(player2_ga) + " dollars.")

    print("The word was: {}".format(secret))
    print("Since {} had ${} and {} had ${} in their accounts".format(
        player1, player1_ga, player2, (player2_ga)))
    if player2_ga > player1_ga:
        print("\nCool, " + player2 + " you win!")
        sys.exit()
    else:
        print("\nCool, " + player1 + " you win!")
        sys.exit()


'''
the spin function generates a random number for the program

'''


def spin():
    number = randint(0, 21)
    return number


'''
This function below helps determine if the consonant that the user
is guessing can be found in the secret word
'''


def guessing():
    if guess.lower() in secret.lower():
        startnow = True
    else:
        startnow = False
    return startnow


'''
this function determines if there are vowels in our secret word
and returns true if there are and false if there are not.  
hence, its checking for vowels
 
'''


def vowels():
    if guess.lower() in secret.lower():
        startnow = True
    else:
        startnow = False
    return startnow


'''
Used to start the game figured this out and the obtained the code for this part
through stackoverflow
'''

if __name__ == "__main__":
    start()
