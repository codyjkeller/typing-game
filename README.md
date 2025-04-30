# main.py
import tkinter as tk
from tkinter import messagebox
import random
import time

# --- Constants ---
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
GAME_DURATION_SECONDS = 60
WORD_FILE = "words.txt" # Expects a file with one word per line

# --- Load Words ---
try:
    with open(WORD_FILE, "r") as f:
        words = [word.strip().lower() for word in f.readlines() if word.strip()]
    if not words:
        words = ["programming", "coding", "algorithm", "systems", "python", "software", "developer", "keyboard", "practice", "typing"] # Fallback words
except FileNotFoundError:
    print(f"Warning: '{WORD_FILE}' not found. Using default word list.")
    words = ["programming", "coding", "algorithm", "systems", "python", "software", "developer", "keyboard", "practice", "typing"]

# --- Game Class ---
class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False) # Prevent resizing

        self.words_to_type =
        self.current_word_index = 0
        self.typed_text = ""
        self.correct_chars = 0
        self.total_chars = 0
        self.start_time = 0
        self.time_left = GAME_DURATION_SECONDS
        self.timer_running = False
        self.timer_id = None

        # --- UI Elements ---
        self.instructions_label = tk.Label(root, text=f"Type the words below. You have {GAME_DURATION_SECONDS} seconds.", font=("Helvetica", 14))
        self.instructions_label.pack(pady=20)

        self.word_display_label = tk.Label(root, text="", font=("Courier New", 18), wraplength=WINDOW_WIDTH - 50, justify="center", height=5)
        self.word_display_label.pack(pady=10)

        self.entry_var = tk.StringVar()
        self.typing_entry = tk.Entry(root, textvariable=self.entry_var, font=("Helvetica", 16), width=50)
        self.typing_entry.pack(pady=10)
        self.typing_entry.bind("<KeyRelease>", self.check_input) # Use KeyRelease to get final value after key press
        self.typing_entry.focus_set() # Set focus to entry widget

        self.timer_label = tk.Label(root, text=f"Time Left: {self.time_left}s", font=("Helvetica", 14))
        self.timer_label.pack(pady=10)

        self.results_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.results_label.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart Test", font=("Helvetica", 14), command=self.reset_game, state=tk.DISABLED)
        self.restart_button.pack(pady=20)

        # --- Start Game ---
        self.reset_game()

    def generate_words(self):
        """Generates a list of words for the current test."""
        # Estimate words needed based on average speed (e.g., 50 WPM) + buffer
        estimated_words = int((50 * (GAME_DURATION_SECONDS / 60)) * 2.5)
        self.words_to_type = random.sample(words, min(len(words), estimated_words))

    def update_word_display(self):
        """Updates the label showing words to type."""
        display_text = " ".join(self.words_to_type)
        self.word_display_label.config(text=display_text)
        # Highlight the current word (simple approach: just show all)
        # More complex: Could use Text widget for highlighting

    def reset_game(self):
        """Resets the game to the initial state."""
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.current_word_index = 0
        self.typed_text = ""
        self.correct_chars = 0
        self.total_chars = 0
        self.start_time = 0
        self.time_left = GAME_DURATION_SECONDS

        self.generate_words()
        self.update_word_display()

        self.entry_var.set("")
        self.typing_entry.config(state=tk.NORMAL)
        self.typing_entry.focus_set()

        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        self.results_label.config(text="")
        self.restart_button.config(state=tk.DISABLED)
        self.instructions_label.config(text=f"Type the words below. You have {GAME_DURATION_SECONDS} seconds. Start typing to begin.")


    def start_timer(self):
        """Starts the game timer."""
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.instructions_label.config(text="Go!")
            self.update_timer()

    def update_timer(self):
        """Updates the timer label and checks for game end."""
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.time_left = max(0, GAME_DURATION_SECONDS - int(elapsed_time))
            self.timer_label.config(text=f"Time Left: {self.time_left}s")

            if self.time_left > 0:
                self.timer_id = self.root.after(1000, self.update_timer) # Schedule next update
            else:
                self.end_game()

    def check_input(self, event):
        """Checks the user's input as they type."""
        if not self.timer_running and self.time_left > 0:
            self.start_timer()

        if not self.timer_running: # Don't process input if timer hasn't started or has ended
            return

        current_input = self.entry_var.get()
        target_words_str = " ".join(self.words_to_type)

        # Simple comparison: check typed text against the beginning of the target string
        self.total_chars = len(current_input)
        self.correct_chars = 0
        for i, char in enumerate(current_input):
            if i < len(target_words_str) and char == target_words_str[i]:
                self.correct_chars += 1
            else:
                # Optional: Add visual feedback for errors (e.g., change text color)
                pass

        # Check if the user typed a space, indicating word completion (basic check)
        if event.keysym == "space":
             # This simple version doesn't advance word by word,
             # it just lets user type freely into the target string.
             # A more complex version would track word boundaries.
             pass


    def end_game(self):
        """Ends the game and displays results."""
        self.timer_running = False
        self.typing_entry.config(state=tk.DISABLED) # Disable further typing
        self.restart_button.config(state=tk.NORMAL)

        # Calculate WPM (based on 5 chars per word)
        gross_wpm = int(((self.total_chars / 5) / (GAME_DURATION_SECONDS / 60))) if self.total_chars > 0 else 0

        # Calculate Accuracy
        accuracy = int((self.correct_chars / self.total_chars) * 100) if self.total_chars > 0 else 0

        # Calculate Net WPM (Adjusted for accuracy) - Optional
        # net_wpm = int(gross_wpm * (accuracy / 100))

        result_text = f"Time's Up!\nGross WPM: {gross_wpm}\nAccuracy: {accuracy}%"
        self.results_label.config(text=result_text)
        messagebox.showinfo("Results", result_text)


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    game = TypingSpeedTest(root)
    root.mainloop()
