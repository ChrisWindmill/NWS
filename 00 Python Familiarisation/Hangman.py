import random

words = ["Networks", "Security", "Toast", "Cheese"]
hangman = ["Thing 1", "Thing 2", "Thing 3", "Thing 4", "Thing 5", "Done"]

player_guess = None
won = False
attempts = len(hangman) - 1
guessed_letters = []


chosen_word = random.choice(words).lower()

while attempts > 0 and not won:
    player_guess = None
    print(f"You have {attempts} guesses left before the game ends")
    for letter in chosen_word:
        if letter in guessed_letters:
            print(f" {letter}", end="")
        else:
            print(" - ", end="")
    print()

    while player_guess == None:
        try:
            player_guess = str(input("Please enter a letter: A-Z")).lower()
        except:
            print("An error occurred, that was not a string input")
        else:
            if not player_guess.isalpha():
                print("That was not a character")
                continue
            elif len(player_guess) > 1:
                print("You entered more than one character")
                continue
            elif player_guess in guessed_letters:
                print("You chose that one before, please be more careful")
                continue
            else:
                pass

    guessed_letters.append(player_guess)

    if player_guess in chosen_word:
        won = True
        for letter in chosen_word:
            if not letter in guessed_letters:
                won = False

        if won:
            print("Congratulations, you won")
    else:
        print("That was incorrect")
        attempts -= 1
        print(hangman[-attempts])
