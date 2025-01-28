import os
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import Button, Label, Entry
import platform
import stat

# Function to get the current script directory
def get_script_directory():
    return os.path.dirname(os.path.realpath(__file__))

# Function to get the hidden file path based on the operating system
def get_hidden_file_path():
    system = platform.system().lower()

    # Get the hidden folder location based on the operating system
    if system == "windows":
        # Windows AppData path
        hidden_folder = os.path.join(os.environ['APPDATA'], 'HitarthCoin')
    else:
        # For macOS and Linux, use the home directory and make it hidden
        hidden_folder = os.path.join(os.path.expanduser("~"), ".HitarthCoin")

    # Ensure the hidden folder exists
    if not os.path.exists(hidden_folder):
        os.makedirs(hidden_folder)

    return os.path.join(hidden_folder, "user_data.json")

# Function to ensure the JSON file is writable
def make_writable(filepath):
    """Ensure the file is writable by removing the read-only attribute."""
    if os.path.exists(filepath):
        os.chmod(filepath, stat.S_IWRITE)

# Function to handle mining logic and file saving
def start_mining(name_entry, root, coin_label, start_button):
    # Get user name from the input field
    user_name = name_entry.get()

    # Check if the name is empty
    if not user_name:
        messagebox.showerror("Input Error", "Please enter your name")
        return

    # Get the path of the hidden user data file
    user_data_path = get_hidden_file_path()

    # Ensure the JSON file is writable
    make_writable(user_data_path)

    # Try reading the existing data from the file
    try:
        with open(user_data_path, "r") as file:
            user_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}

    # Check if the user already has an entry in the data
    if user_name not in user_data:
        user_data[user_name] = {"coins": 0}

    # Function to update coins and show message
    def update_coins():
        user_data[user_name]["coins"] += 1
        with open(user_data_path, "w") as file:
            json.dump(user_data, file)
        
        # Update the coin label
        coin_label.config(text=f"{user_name} has {user_data[user_name]['coins']} HitarthCoins!")
        
        # Display a message in the main window instead of a pop-up
        earned_label.config(text="+1 HitarthCoin Earned!", fg="green")
        
        # Hide the message after 3 seconds
        root.after(3000, lambda: earned_label.config(text=""))

        # Schedule next coin update in 1 minute
        root.after(60000, update_coins)  # Update every minute

    # Make the Start Mining button disappear after the first click
    start_button.pack_forget()

    # Start the mining process
    update_coins()

# Set up the Tkinter interface
root = tk.Tk()
root.title("HitarthCoin Mining")

# Set the window size
root.geometry("400x300")  # Increased window size for better visibility

# Prompt for the user's name
label = Label(root, text="Enter your name:")
label.pack(pady=10)

name_entry = Entry(root)
name_entry.pack(pady=10)

# Label to display user's coin count
coin_label = Label(root, text="You have 0 HitarthCoins", font=("Arial", 12))
coin_label.pack(pady=20)

# Label to display the "+1 HitarthCoin Earned!" message
earned_label = Label(root, text="", font=("Arial", 12), fg="green")
earned_label.pack(pady=5)

# Button to start mining
start_button = Button(root, text="Start Mining", font=("Arial", 12), command=lambda: start_mining(name_entry, root, coin_label, start_button))
start_button.pack(pady=20)

root.mainloop()
