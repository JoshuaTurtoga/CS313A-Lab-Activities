import random
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

# Dictionary of words and their hints
WORDS = {
    "PYTHON": "A popular programming language named after a snake",
    "PROGRAMMING": "The art of telling a computer what to do",
    "COMPUTER": "An electronic device that processes data",
    "ALGORITHM": "A step-by-step procedure to solve a problem",
    "DATABASE": "A structured collection of data",
    "NETWORK": "A system of interconnected computers",
    "JAVASCRIPT": "A programming language for web browsers",
    "DEVELOPER": "Someone who creates software",
    "SOFTWARE": "Programs and other operating information",
    "HANGMAN": "The very game you're playing right now",
    "INTERFACE": "A point where two systems meet and interact",
    "VARIABLE": "A container for storing data values",
    "FUNCTION": "A reusable block of code",
    "KEYBOARD": "Device used to input text into a computer",
    "MONITOR": "A display screen for computers"
}

# Hangman ASCII art states
HANGMAN_STATES = [
    # State 0: Empty
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    # State 1: Head
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    # State 2: Head and torso
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    # State 3: Head, torso, and one arm
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    # State 4: Head, torso, and both arms
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    # State 5: Head, torso, both arms, and one leg
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    # State 6: Full hangman (game over)
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Display the main menu and get user choice."""
    while True:
        clear_screen()
        print(Fore.CYAN + "=== HANGMAN GAME ===" + Style.RESET_ALL)
        print("\n1. Start Game")
        print("2. Instructions")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice in ['1', '2', '3']:
            return choice
        print(Fore.RED + "\nInvalid choice! Press Enter to try again..." + Style.RESET_ALL)
        input()


def show_instructions():
    """Display game instructions."""
    clear_screen()
    print(Fore.CYAN + "=== INSTRUCTIONS ===" + Style.RESET_ALL)
    print("\n1. The computer will choose a random word")
    print("2. Try to guess the word one letter at a time")
    print("3. Each wrong guess adds a part to the hangman")
    print("4. You have 6 wrong guesses before the game is over")
    print("5. Duplicate guesses don't count against you")
    print("6. Press '1' during the game to get a hint (-30 points)")
    print(Fore.YELLOW + "\nPoints System:" + Style.RESET_ALL)
    print("• Correct guess: +10 points")
    print("• Wrong guess: -5 points")
    print("• Using a hint: -30 points")
    print("• Winning the game: +50 bonus points")
    print("\nPress Enter to return to main menu...")
    input()


def display_game_state(word, guessed_letters, wrong_attempts, score, hint_used=False):
    """Display the current state of the game."""
    clear_screen()

    # Display hangman
    print(HANGMAN_STATES[wrong_attempts])

    # Display word progress
    word_progress = ''
    for letter in word:
        if letter in guessed_letters:
            word_progress += Fore.GREEN + letter + Style.RESET_ALL + ' '
        else:
            word_progress += '_ '
    print("\nWord:", word_progress)

    # Always display hint if it has been used
    if hint_used:
        print(Fore.CYAN + "\nHint:", WORDS[word] + Style.RESET_ALL)

    # Display guessed letters
    print("\nGuessed letters:", ' '.join(sorted(guessed_letters)))
    print(Fore.YELLOW +
          f"\nRemaining attempts: {6 - wrong_attempts}" + Style.RESET_ALL)
    print(Fore.CYAN + f"Score: {score}" + Style.RESET_ALL)

    # Show different prompt based on hint status
    if hint_used:
        print("\nEnter a letter to guess:")
    else:
        print("\nEnter '1' for a hint (-30 points) or enter a letter to guess:")


def play_game():
    """Main game logic."""
    score = 0
    while True:
        # Select a random word from the dictionary
        word = random.choice(list(WORDS.keys()))
        guessed_letters = set()
        wrong_attempts = 0
        word_completed = False
        hint_used = False

        while wrong_attempts < 6 and not word_completed:
            display_game_state(word, guessed_letters,
                               wrong_attempts, score, hint_used)  # Show hint if it's been used

            # Get player's guess
            guess = input().upper().strip()

            # Check for hint request
            if guess == '1':
                if not hint_used:
                    if score >= 30:  # Check if player has enough points
                        print(Fore.YELLOW +
                              "\nUsing hint! -30 points" + Style.RESET_ALL)
                        hint_used = True
                        score -= 30  # Deduct points for using hint
                        print(Fore.CYAN + "HINT:",
                              WORDS[word] + Style.RESET_ALL)
                        input("\nPress Enter to continue...")
                        continue
                    else:
                        print(
                            Fore.RED + f"\nNot enough points! You need 30 points to use a hint. Current score: {score}" + Style.RESET_ALL)
                        input("Press Enter to continue...")
                        continue
                else:
                    print(
                        Fore.YELLOW + "\nHint already used! The hint is shown above." + Style.RESET_ALL)
                    input("Press Enter to continue...")
                    continue

            # Validate input
            if len(guess) != 1 or not guess.isalpha():
                print(Fore.RED + "\nPlease enter a single letter!" + Style.RESET_ALL)
                input("Press Enter to continue...")
                continue

            # Check if letter was already guessed
            if guess in guessed_letters:
                print(Fore.YELLOW +
                      "\nYou already guessed that letter!" + Style.RESET_ALL)
                input("Press Enter to continue...")
                continue

            guessed_letters.add(guess)

            # Check if guess is correct
            if guess in word:
                print(Fore.GREEN + "\nCorrect guess!" + Style.RESET_ALL)
                score += 10
            else:
                print(Fore.RED + "\nWrong guess!" + Style.RESET_ALL)
                wrong_attempts += 1
                # Deduct points for wrong guess, minimum 0
                score = max(0, score - 5)

            # Check if word is completed
            word_completed = all(letter in guessed_letters for letter in word)
            input("Press Enter to continue...")

        # Game over - display final state
        display_game_state(word, guessed_letters, wrong_attempts, score)

        if word_completed:
            print(Fore.GREEN + "\nCongratulations! You won!" + Style.RESET_ALL)
            print(f"Final Score: {score}")
            print(Fore.YELLOW + "Adding bonus points for winning: +50" + Style.RESET_ALL)
            score += 50  # Bonus points for winning
            print(f"Total Score: {score}")
        else:
            print(Fore.RED + "\nGame Over! The word was: " +
                  word + Style.RESET_ALL)

        # Ask to play again
        play_again = input(
            "\nDo you want to play again? (y/n): ").lower().strip()
        if play_again != 'y':
            break


def main():
    """Main program loop."""
    while True:
        choice = display_menu()

        if choice == '1':
            play_game()
        elif choice == '2':
            show_instructions()
        else:  # choice == '3'
            clear_screen()
            print(Fore.CYAN + "Thanks for playing Hangman! Goodbye!" + Style.RESET_ALL)
            break


if __name__ == "__main__":
    main()
