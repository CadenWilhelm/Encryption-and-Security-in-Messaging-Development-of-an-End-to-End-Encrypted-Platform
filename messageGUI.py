# Caden Wilhelm
# Capstone Project: MessageAPP
# Project desciption: In modern technology, privacy is hard to come by and ensuring security and privacy of messages is a major concern. Traditional messaging platforms have become outdated and are susceptible to interception and eavesdropping. This poses a risk for unauthorized access, and data theft on a personal and organizational level. This project aims to discuss and research this topic, and gaining first-hand experience through development of a messaging platform featuring end-to-end encryption (E2EE) ensuring security from sender to recipient.
import tkinter as tk
from tkinter import Menu
import json

# Function to open a new chat window
def open_chat(name):
    chat_window = tk.Toplevel(root)
    chat_window.title(f"Chat with {name}")

    chat_display = tk.Text(chat_window, state=tk.DISABLED, wrap=tk.WORD)
    chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    message_entry = tk.Entry(chat_window)
    message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
    
    def send_message():
        message = message_entry.get()
        if message:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"You: {message}\n")
            chat_display.config(state=tk.DISABLED)
            message_entry.delete(0, tk.END)
            chat_display.see(tk.END)
            save_chat_history(name, message)
    
    send_button = tk.Button(chat_window, text="Send", command=send_message)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def clear_chat_history():
        filename = f"chat_history_{name}.txt"
        with open(filename, "w") as file:
            pass  # This will clear the file
        chat_display.config(state=tk.NORMAL)
        chat_display.delete(1.0, tk.END)  # Clear the Text widget
        chat_display.config(state=tk.DISABLED)
    
    clear_button = tk.Button(chat_window, text="Clear Chat", command=clear_chat_history)
    clear_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Function to save chat history for specific chat
    def save_chat_history(name, message):
        filename = f"chat_history_{name}.txt"
        with open(filename, "a") as file:
            file.write(f"You: {message}\n")
    
    # Function to load chat history for specific chat
    def load_chat_history(name):
        filename = f"chat_history_{name}.txt"
        try:
            with open(filename, "r") as file:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, file.read())
                chat_display.config(state=tk.DISABLED)
        except FileNotFoundError:
            pass

    # Load chat history for specific chat
    load_chat_history(name)

# Function to create a new contact
def create_contact():
    def save_contact():
        username = username_entry.get()
        contact_name = contact_name_entry.get()
        chats_list.append((username, contact_name))
        save_contacts_to_file()
        print("New Contact Created:")
        print("Username:", username)
        print("Contact Name:", contact_name)
        new_contact_window.destroy()
        update_chat_menu()
        open_chat(contact_name)  # Open chat with the newly added contact

    new_contact_window = tk.Toplevel(root)
    new_contact_window.title("Create New Contact")

    username_label = tk.Label(new_contact_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(new_contact_window)
    username_entry.pack()

    contact_name_label = tk.Label(new_contact_window, text="Contact Name:")
    contact_name_label.pack()
    contact_name_entry = tk.Entry(new_contact_window)
    contact_name_entry.pack()

    save_button = tk.Button(new_contact_window, text="Save", command=save_contact)
    save_button.pack()

def update_chat_menu():
    # Clear existing menu items
    chats_menu.delete(0, tk.END)
    # Adding dynamic chat menu options with commands
    for username, contact_name in chats_list:
        chats_menu.add_command(label=f"Chat with {contact_name}", command=lambda name=contact_name: open_chat(name))

def save_contacts_to_file():
    with open("contacts.json", "w") as file:
        json.dump(chats_list, file)

def load_contacts_from_file():
    try:
        with open("contacts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Create the main application window
root = tk.Tk()

# Set the title of the window
root.title("MessageAPP - E2EE")

# Load contacts from file
chats_list = load_contacts_from_file()

# Create and pack a label widget with a title
welcome_label = tk.Label(root, text="Click to Start a Chat!", font=("Helvetica", 22))
welcome_label.pack(pady=20)

# Create buttons for each contact
for _, contact_name in chats_list:
    contact_button = tk.Button(root, text=f" {contact_name} ", command=lambda name=contact_name: open_chat(name))
    contact_button.pack()

# Button to create a new contact
new_contact_button = tk.Button(root, text="Create a New Contact", command=create_contact)
new_contact_button.pack()

# Create a frame for the button and place it at the top right
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

stop_button = tk.Button(top_frame, text="Stop", width=10, command=root.destroy)
stop_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create a 'Chats' menu
chats_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Chats", menu=chats_menu)

# Update chat menu
update_chat_menu()

# Run the Tkinter main loop
root.mainloop()
