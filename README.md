Simple Python Typing Speed Test
A basic desktop application built with Python and Tkinter to test your typing speed and accuracy.

Features
Displays random words from a list (words.txt).
Timed test duration (default: 60 seconds).
Calculates Gross Words Per Minute (WPM) based on characters typed (standard 5 chars/word).
Calculates typing accuracy percentage.
Simple graphical user interface using Tkinter.
Restart functionality.
Requirements
Python 3.x
Tkinter (usually included with Python standard installations)
Installation and Usage
**Clone the repository:**bash git clone <your-repository-url> cd simple-typing-test
(Optional but Recommended) Create and activate a virtual environment:
Bash

# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
Ensure words.txt is present: The game reads words from words.txt in the same directory. You can customize this file with your own word list (one word per line).
Run the game:
Bash

python main.py
Start typing in the input field when ready. The timer begins as soon as you press the first key.
