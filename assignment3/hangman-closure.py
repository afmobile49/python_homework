# Task 4


def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        letter = letter.lower()

        if letter not in guesses:
            guesses.append(letter)

        displayed_word = "".join(
            character
            if character.lower() in guesses
            else "_"
            for character in secret_word
        )

        print(displayed_word)

        return all(
            character.lower() in guesses
            for character in secret_word
        )

    return hangman_closure


if __name__ == "__main__":
    secret_word = input("Enter the secret word: ").strip()

    while not secret_word:
        print("The secret word cannot be empty.")
        secret_word = input("Enter the secret word: ").strip()

    game = make_hangman(secret_word)

    print("_" * len(secret_word))

    word_guessed = False

    while not word_guessed:
        guess = input("Guess a letter: ").strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one letter.")
            continue

        word_guessed = game(guess)

    print(f"You guessed the word: {secret_word}")