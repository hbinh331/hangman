import random

def load_words_from_file(file_path="animals.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = [line.strip().upper() for line in file if line.strip()]
            return words if words else ["DOG", "CAT", "ELEPHANT"]
    except Exception:
        # Use reserved words in case of errors
        return ["DOG", "CAT", "ELEPHANT"]
    
class HangmanGame:
    def __init__(self, word_list=None, max_tries=6):
        if word_list is None:
            self.word_list = load_words_from_file("animals.txt")
        else:
            self.word_list = word_list

        self.max_tries = max_tries
        self.reset()

    def reset(self):
        self.secret_word = random.choice(self.word_list).upper()
        self.tries_left = self.max_tries
        self.guessed_letters = set()
        self.incorrect_guessed = []

    def guess(self, letter):
        letter = letter.upper()
        
        # Skip if already guessed
        if letter in self.guessed_letters:
            return "ALREADY_GUESSED"

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            return "CORRECT"
        else:
            self.tries_left -= 1
            self.incorrect_guessed.append(letter)
            return "INCORRECT"

    def get_display_word(self):
        # return correctly guessed letters and leftover '_'
        return " ".join([ltr if ltr in self.guessed_letters else "_" for ltr in self.secret_word])

    def is_won(self):
        return all(letter in self.guessed_letters for letter in self.secret_word)

    def is_lost(self):
        return self.tries_left <= 0

if __name__ == "__main__":
    game = HangmanGame()
    
    while True:
        print("\n" + "=" * 40)
        print(f"Secret Word: {game.get_display_word()}")
        print(f"Tries Left: {game.tries_left}")
        print(f"Wrong Guesses: {', '.join(game.incorrect_guessed)}")
        print("=" * 40)

        # Get user input
        user_input = input("Enter a letter (or 'quit' to quit): ").strip().upper()

        if user_input == 'QUIT':
            print("Game exited!")
            break

        if len(user_input) != 1 or not user_input.isalpha():
            print(">> Please enter a single letter!")
            continue

        # Process the guess
        result = game.guess(user_input)

        if result == "ALREADY_GUESSED":
            print(f">> You already guessed '{user_input}'!")
        elif result == "CORRECT":
            print(f">> Correct! '{user_input}' is in the word.")
        elif result == "INCORRECT":
            print(f">> Wrong! '{user_input}' is not in the word.")

        # Check Win condition
        if game.is_won():
            print("\n" + "*" * 40)
            print(f"YOU WON! The secret word was: {game.secret_word}")
            print("*" * 40)
            play_again = input("Do you want to play again? (Y/N): ").strip().upper()
            if play_again == 'Y':
                game.reset()
            else:
                break

        # Check Lose condition
        elif game.is_lost():
            print("\n" + "X" * 40)
            print(f"YOU LOST! The secret word was: {game.secret_word}")
            print("X" * 40)
            play_again = input("Do you want to play again? (Y/N): ").strip().upper()
            if play_again == 'Y':
                game.reset()
            else:
                break