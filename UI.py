import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import math
import time
import training

def add_message():
    button.config(state=tk.NORMAL)
    entry.config(state=tk.NORMAL)

    message = entry.get()
    # Print the message to the Python console
    #print("HUMANO DICE: " + message)
    entry.delete(0, tk.END)  # Clear the input field
    bg_color = "lightgreen"
    alignment = tk.E  # Align to the east (right)
    button.config(state=tk.DISABLED)
    entry.config(state=tk.DISABLED)

    # Create a new frame for the message and add it to the scrollable window
    frame = tk.Frame(scrollable_frame, bg=bg_color)
    frame.grid(row=len(message_frames), column=0, sticky=tk.E if alignment == tk.E else tk.W, padx=10, pady=5)

    # Create a label within the frame to display the message
    label = tk.Label(frame, text=message, anchor=tk.E if alignment == tk.E else tk.W, bg=bg_color, wraplength=600)
    label.pack(side=tk.RIGHT if alignment == tk.E else tk.LEFT, padx=10, pady=5)

    message_frames.append(frame)



    # Configure the scrollable frame to expand vertically and display each message below the previous one
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)
    reply = training.reply(message)
    reply_message(reply)

def reply_message(msg):
    bg_color = "lightblue"
    alignment = tk.W  # Align to the west (left)
    frame = tk.Frame(scrollable_frame, bg=bg_color)
    frame.grid(row=len(message_frames), column=0, sticky=tk.E if alignment == tk.E else tk.W, padx=10, pady=5)

    label = tk.Label(frame, anchor=tk.E if alignment == tk.E else tk.W, bg=bg_color, wraplength=600)
    label.pack(side=tk.RIGHT if alignment == tk.E else tk.LEFT, padx=10, pady=5)

    if msg == "Muchas gracias, nos vemos!" or msg == "Excelente, hemos encontrado un trabajo que se adjusta a tus preferencias. Muchas gracias" \
                         " por participar de este proceso junto a Chaty. Nos vemos":
        cerrar_ventana()
        return
    message_frames.append(frame)

    button.config(state=tk.DISABLED)
    entry.config(state=tk.DISABLED)


    for i, char in enumerate(msg):
        label.config(text=msg[:i+1])  # Update the label with each letter
        root.update()  # Update the GUI
        time.sleep(0.02)  # Add a delay to control the speed of printing

    button.config(state=tk.NORMAL)
    entry.config(state=tk.NORMAL)

    # Configure the scrollable frame to expand vertically and display each message below the previous one
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(1.0)



def center_window(window, width_ratio, height_ratio):
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()
    desired_width = math.floor(window_width * width_ratio)
    desired_height = math.floor(window_height * height_ratio)
    offset_x = math.floor((window_width - desired_width) / 2)
    offset_y = math.floor((window_height - desired_height) / 2)
    window.geometry(f"{desired_width}x{desired_height}+{offset_x}+{offset_y}")
    return desired_width, desired_height

def cerrar_ventana():
    msg = "Gracias por utilizar Chaty! Espero haberte ayudado. Nos vemos la proxima!"
    reply_message(msg)
    msg = "Cerrando la aplicacion en 3... 2... 1..."
    reply_message(msg)
    time.sleep(2)
    root.destroy()

root = tk.Tk()
root.title("Chaty v4")
root.protocol("WM_DELETE_WINDOW", cerrar_ventana)


# Center the window and set its size to occupy 3/4 of the screen
window_width, window_height = center_window(root, 0.64, 0.75)

# Set custom font size for the labels
font = tkFont.Font(size=10)

# Create a scrollable window
canvas = tk.Canvas(root)
canvas.grid(row=0, column=0, sticky=tk.NSEW)

scrollbar = ttk.Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky=tk.NS)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

scrollable_frame = tk.Frame(canvas)
scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Add an initial message box aligned to the left
initial_frame = tk.Frame(scrollable_frame, bg="lightblue")
initial_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

initial_label = tk.Label(initial_frame, text="Hola, en que puedo ayudarte? Soy Chaty, tu asistente inteligente. Comencemos con las preguntas. Dime que quieres saber y te respondo.", anchor=tk.W, bg="lightblue", font=font)
initial_label.pack(side=tk.LEFT, padx=10, pady=5)

message_frames = [initial_frame]

# Calculate the desired width of the Entry field based on the screen width
entry_width = window_width - 40  # Subtracting the padding and margins

# Add an input field in the second row
entry = tk.Entry(root, font=font, width=entry_width)
entry.grid(row=1, column=0, padx=10, pady=5)
entry.focus_set()  # Set focus to the Entry field

# Add the "Enviar" button in the third row
button = tk.Button(root, text="Enviar", command=add_message)
button.grid(row=2, column=0, padx=10, pady=5)

# Bind the Enter key press event to the add_message function
entry.bind("<Return>", lambda event: add_message())

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
scrollable_frame.grid_rowconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(0, weight=1)

root.mainloop()