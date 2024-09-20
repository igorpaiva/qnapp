import tkinter as tk
from tkinter import messagebox
import json
import os

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        
        self.create_menu()

    def create_menu(self):
        """Sets up the main menu with Play, Create Deck, and Quit options."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title label
        title_label = tk.Label(self.root, text="Question & Answer Game", font=("Arial", 24))
        title_label.pack(pady=20)

        # Play button (can be implemented later)
        play_button = tk.Button(self.root, text="Play", font=("Arial", 14), command=self.play_game)
        play_button.pack(pady=10)

        # Create Deck button (open the QnApp)
        create_deck_button = tk.Button(self.root, text="Create Deck", font=("Arial", 14), command=self.open_deck_creator)
        create_deck_button.pack(pady=10)

        # Quit button
        quit_button = tk.Button(self.root, text="Quit", font=("Arial", 14), command=self.root.quit)
        quit_button.pack(pady=10)

    def play_game(self):
        """Placeholder for the game itself"""
        messagebox.showinfo("Play", "Game not implemented yet!")

    def open_deck_creator(self):
        """Opens the deck creator interface"""
        QnApp(self.root)

class QnApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Deck")

        # TODO: let the user choose the file name
        self.file_name = "qna.json"

        # Initialize the ID based on existing data
        self.question_id = self.get_next_question_id()
        self.answers = []

        # Create the UI
        self.create_ui()

    def create_ui(self):
        """Sets up the UI elements, used for initial setup and after resetting."""
        # Clear any existing UI elements
        for widget in self.root.winfo_children():
            widget.destroy()

        self.row = 0

        # Back to Menu button
        back_button = tk.Button(self.root, text="Back to Menu", command=self.back_to_menu)
        back_button.grid(row=self.row, column=0)

        self.increment_row()

        # Question entry
        self.question_label = tk.Label(self.root, text="Question:")
        self.question_label.grid(row=self.row, column=0)

        self.question_entry = tk.Entry(self.root, width=50)
        self.question_entry.grid(row=self.row, column=1)

        self.increment_row()

        # Answers frame
        self.answers_frame = tk.Frame(self.root)
        self.answers_frame.grid(row=self.row, column=0, columnspan=2)

        self.increment_row()

        # + Button to add more answers
        self.add_answer_button = tk.Button(self.root, text="+", command=self.add_answer_field)
        self.add_answer_button.grid(row=self.row, column=1, sticky='e')

        self.increment_row()

        # Save button
        self.save_button = tk.Button(self.root, text="Save", command=self.save_data)
        self.save_button.grid(row=self.row, column=1, sticky='e')

        self.increment_row()

        # Initialize with one answer field
        self.answers.clear()
        self.add_answer_field()

    def increment_row(self):
        self.row += 1

    def get_next_question_id(self):
        """Returns the next available question ID by checking existing data in the JSON file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
            if data:
                max_id = max(entry["id"] for entry in data)
                return max_id + 1
        return 1

    def add_answer_field(self):
        answer_label = tk.Label(self.answers_frame, text=f"Answer {len(self.answers) + 1}:")
        answer_label.grid(row=len(self.answers), column=0)

        answer_entry = tk.Entry(self.answers_frame, width=50)
        answer_entry.grid(row=len(self.answers), column=1)
        self.answers.append(answer_entry)

    def save_data(self):
        """Saves the question and answers to a .json file"""

        # TODO: maybe move to a validate card function later?
        # TODO: check if the card already exists
        # Does not let the user create a card with an empty question
        question = self.question_entry.get()
        if not question:
            messagebox.showwarning("Input Error", "Please enter a question.")
            return

        # Does not let the user create a card with no answers
        answers = [answer.get() for answer in self.answers if answer.get()]
        if not answers:
            messagebox.showwarning("Input Error", "Please provide at least one answer.")
            return

        # Load existing data or create new data structure
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
        else:
            data = []

        # Add new question-answer entry
        qna_entry = {
            "id": self.question_id,
            "question": question,
            "answers": answers
        }
        data.append(qna_entry)

        # Save to JSON file
        with open(self.file_name, "w") as f:
            json.dump(data, f, indent=4)

        self.question_id += 1
        messagebox.showinfo("Success", "Data saved successfully!")
        self.create_ui()

    def back_to_menu(self):
        """Go back to the main menu."""
        MainMenu(self.root)