import random
import requests
import csv

hangman_steps = [
    """
    ------
    | |
    |
    |
    |
    |
    |
    |___
    """,
    """
    ------
    | |
    | O
    |
    |
    |
    |
    |___
    """,
    """
    ------
    | |
    | O
    | |
    |
    |
    |
    |___
    """,
    """
    ------
    | |
    | O
    | /|
    |
    |
    |
    |___
    """,
    """
    ------
    | |
    | O
    | /|\\
    |
    |
    |
    |___
    """,
    """
    ------
    | |
    | O
    | /|\\
    | /
    |
    |
    |___
    """,
    """
    ------
    | |
    | O
    | /|\\
    | / \\
    |
    |
    |___
    """
]


def game_setup():
    # secret_words = ["hi", "horse", "love", "coffee", "joke", "table", "Hanna", "Fikusz", "Muki", "sound"]
    while True:
        try:
            response = requests.get('https://random-word-api.herokuapp.com/word', timeout=5)
        except requests.exceptions.RequestException:
            with open('names.csv', newline='') as names_csv_file:
                csv_reader = csv.reader(names_csv_file)
                next(csv_reader)
                word = (random.choice([line[0] for line in csv_reader]))
                break
        else:
            letters = list(response.text)
            word = letters[2:len(letters) - 2]
            break

    word2 = list(word)
    for x in range(len(word)):
        word2[x] = '_'
    for x in range(len(word)):
        print("_", end="")
    return word, word2


def input_function():

    while True:
        letter = input("\nEnter a letter: ")
        if len(letter) == 1 and letter.isalpha() is True:
            return letter
        else:
            print("this is not a letter")
            continue


def correct_guess(letter, word, word2):
    for x in range(len(word)):
        if letter == word[x]:
            word2[x] = letter
    else:
        print(''.join(word2))
        return word2


def incorrect_guess(letter, word, attempt):
    if letter not in word:
        print(hangman_steps[7 - attempt])
        return True


def winning_function(word, word2):
    if ''.join(word2) == ''.join(word):
        print("You have won the game!")
        return True


def loosing_function(attempt):
    if attempt == 0:
        print("You have lost the game. You've been hanged!")
        return True


def game_over(word):
    print("The secret word is: ", ''.join(word))


def main():
    attempt = 7
    word, word2 = game_setup()
    while True:
        letter = input_function()
        word2 = correct_guess(letter, word, word2)
        if incorrect_guess(letter, word, attempt) is True:
            attempt = attempt - 1
        if winning_function(word, word2) is True:
            break
        elif loosing_function(attempt) is True:
            break

    game_over(word)


main()
