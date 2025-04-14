# -*- coding: utf-8 -*-
"""
Simple Command-Line Typing Speed Test Game in Python.
"""

import time
import random
import sys # Used for flushing output

# --- Configuration ---
# List of sentences to type. Add more or load from a file for variety!
SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump!",
    "Programming is fun and rewarding.",
    "Practice makes perfect when learning to type faster.",
    "Keep calm and code on, diligently and patiently.",
    "Python is a versatile and widely-used programming language.",
    "Hello World is often the first program written by beginners.",
    "GitHub is a popular platform for version control and collaboration.",
    "Never stop learning new skills and expanding your horizons.",
    "The journey of a thousand miles begins with a single step.",
    "Computers are incredibly fast, accurate, and stupid.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "Ask not what your country can do for you; ask what you can do for your country."
]

# --- Helper Functions ---

def get_sentence():
    """Selects a random sentence from the list."""
    return random.choice(SENTENCES)

def calculate_results(start_time, end_time, user_input, target_sentence):
    """
    Calculates time elapsed, WPM (Words Per Minute), and accuracy.

    Args:
        start_time (float): The timestamp when typing started.
        end_time (float): The timestamp when typing ended.
        user_input (str): The text typed by the user.
        target_sentence (str): The sentence the user was supposed to type.

    Returns:
        tuple: Contains time_elapsed (float), wpm (int), accuracy (float).
    """
    time_elapsed = end_time - start_time
    # Prevent division by zero if time is too short or zero
    if time_elapsed <= 0:
        time_elapsed = 0.01 # Assign a very small duration

    # Calculate Accuracy
    correct_chars = 0
    # Iterate up to the length of the SHORTER string to avoid index errors
    # or up to the target length if user typed more
    comparison_length = min(len(user_input), len(target_sentence))

    for i in range(comparison_length):
        if user_input[i] == target_sentence[i]:
            correct_chars += 1

    # Accuracy based on the target sentence length
    accuracy = (correct_chars / len(target_sentence)) * 100 if len(target_sentence) > 0 else 0

    # Calculate WPM (Words Per Minute)
    # A standard "word" in typing tests is often considered 5 characters (including spaces)
    # We base WPM on the number of characters the user actually typed.
    typed_chars = len(user_input)
    words_typed = typed_chars / 5.0
    time_in_minutes = time_elapsed / 60.0
    wpm = int(words_typed / time_in_minutes) if time_in_minutes > 0 else 0

    return time_elapsed, wpm, accuracy

def display_feedback(time_taken, wpm, accuracy, user_input, target_sentence):
    """Prints the results and feedback to the user."""
    print("\n----- Results -----")
    print(f"Time taken: {time_taken:.2f} seconds")
    print(f"Your speed: {wpm} WPM")
    print(f"Accuracy:   {accuracy:.2f}%")

    # Optional: Show detailed comparison if accuracy isn't 100%
    if accuracy < 100:
        print("\n----- Comparison -----")
        print(f"Target:   '{target_sentence}'")
        print(f"You typed: '{user_input}'")
        # You could add more detailed error highlighting here if desired
    print("--------------------\n")


# --- Game Logic ---

def play_round(round_number):
    """Plays a single round of the typing game."""
    target_sentence = get_sentence()

    print(f"\n--- Round {round_number} ---")
    print("Prepare to type:")
    print(f"'{target_sentence}'")
    print("-" * (len(target_sentence) + 2)) # Dynamic separator length

    # Give user a moment and prompt to start
    input("Press Enter when you are ready to start typing...")
    print("Starting now!") # Indicate the timer has started
    time.sleep(0.5) # Brief pause

    # Clear the input prompt line (works better in some terminals)
    # print("\033[F\033[K", end="") # ANSI escape code: Move cursor up, clear line
    # print("Start typing here:") # Re-print prompt without the 'Press Enter...' message

    start_time = time.time() # Start timer *after* user presses Enter

    # Get user input - use print without newline and flush to keep prompt clean
    print("Type here > ", end="")
    sys.stdout.flush() # Ensure the prompt appears immediately
    user_input = input()

    end_time = time.time()   # Stop timer immediately after input is submitted

    # Calculate and display results
    time_taken, wpm, accuracy = calculate_results(start_time, end_time, user_input, target_sentence)
    display_feedback(time_taken, wpm, accuracy, user_input, target_sentence)

def main():
    """Main function to run the typing game loop."""
    print("=============================================")
    print(" Welcome to the Simple Python Typing Tester! ")
    print("=============================================")
    print("Instructions: Type the sentence shown as")
    print("              accurately and quickly as possible.")
    print("              Press Enter after typing.")

    round_count = 0
    while True:
        round_count += 1
        play_round(round_count)

        # Ask to play again
        while True:
            play_again = input("Do you want to play another round? (y/n): ").lower().strip()
            if play_again in ['y', 'n']:
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if play_again == 'n':
            break

    print("\nThanks for playing! Practice regularly to improve your speed.")
    print("=============================================")

# --- Run the game ---
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user. Goodbye!")
