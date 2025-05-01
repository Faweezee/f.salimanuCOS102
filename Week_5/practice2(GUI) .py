import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk

#Handling button click event
def welcomeMessage(username) :
    #Create a Tkinter window
    window = tk.Toplevel(root)
    window.title("Admin Box")
    window.geometry("500x200")

    label1= tk.Label(window, text = f"Welcome {username}\n")
    label1.pack()
    label2 = tk.Label(window, text="This is a Python GUI with Tkinter")
    label2.pack()

    #run the Tkinter event loop
    root.mainloop()

def submit() :
    username = username_entry.get()
    password = password_entry.get()

    if username == "Mary" and password == "cos102" :
        welcomeMessage(username)
    else:
        msgbox.showerror("Login", "Invalid username or password")

# Create main window
root = tk.Tk()
root.title("Login Form")
root.geometry("500x200")


#Create username label and entry
username_label = tk.Label(root, text = "Username :")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

#Crete password label and entry
password_label = tk.Label(root, text = "Password :")
password_label.pack()
password_entry = tk.Entry(root)
password_entry.pack()

# Create submit button
submit_button = tk.Button(root, text = "Submit", command= submit)
submit_button.pack()

# Run the main event loop
root.mainloop()