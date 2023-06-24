import tkinter as tk
from tkinter.font import Font


def resize_canvas(event):
    global square_size, font
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Clear the canvas
    canvas.delete(tk.ALL)

    # Calculate the square size
    padding = 10
    max_message_length = max(len(message) for message, _ in messages)
    square_size = (min(canvas_width, canvas_height) - padding * (len(messages) + 1)) // max_message_length

    for i, (message, color) in enumerate(messages):
        square_x1 = padding
        square_y1 = padding + i * (square_size + padding)

        # Calculate the width based on the length of the message
        square_x2 = square_x1 + len(message) * square_size

        square_y2 = square_y1 + square_size

        # Determine the anchor point based on message index
        anchor = tk.W if i % 2 == 0 else tk.E  # Align even entries to the left, odd entries to the right

        # Calculate the x-coordinate for the square based on the anchor
        square_x1 = padding if anchor == tk.W else canvas_width - padding - len(message) * square_size

        # Create the rectangle
        canvas.create_rectangle(square_x1, square_y1, square_x2, square_y2, outline="black", fill=color)

        # Calculate the center position for the text
        text_x = square_x1 + len(message) * square_size // 2

        # Determine the anchor for text based on message index
        text_anchor = tk.W if anchor == tk.W else tk.E

        # Calculate the maximum font size that fits within the square
        max_font_size = 1
        font = Font(family="Arial", size=max_font_size)
        while font.measure(message) < square_size and max_font_size < square_size:
            max_font_size += 1
            font.configure(size=max_font_size)

        # Create the text with the appropriate font size
        canvas.create_text(text_x, square_y1, text=message, font=font, anchor=text_anchor)

    # Update the scrollable region
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    # Scroll to the bottom
    canvas.yview_moveto(1.0)


def add_update_square():
    global messages
    message = entry.get()
    if len(messages) % 2 == 0:
        color = "lightblue"  # Blue background for even messages
    else:
        color = "lightgreen"  # Green background for odd messages
    messages.append((message, color))
    entry.delete(0, tk.END)
    resize_canvas(tk.Event())


# Create a tkinter window
window = tk.Tk()

window.geometry("530x600")  # Set the window size

# Set the window title
window.title("Scrollable Squares")

# Create a scrollbar
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a canvas widget
canvas = tk.Canvas(window, yscrollcommand=scrollbar.set)
canvas.pack(fill=tk.BOTH, expand=True)

# Configure the scrollbar
scrollbar.config(command=canvas.yview)

# Bind the <Configure> event to the resize_canvas function
canvas.bind("<Configure>", resize_canvas)

# Create a frame to hold the canvas contents
frame = tk.Frame(canvas)
frame.pack()

# Initialize the list of messages and colors
messages = [("Hola, en que te puedo ayudar?", "lightblue")]
colors = ["lightblue", "lightgreen", "lightpink", "lightyellow"]

# Define the font
font = Font(family="Arial", size=14)

# Create an entry widget to input a new message
entry = tk.Entry(window, font=font)
entry.pack(side=tk.BOTTOM, padx=10, pady=10)

# Create an "Add/Update" button
add_update_button = tk.Button(window, text="Add/Update", command=add_update_square)
add_update_button.pack(side=tk.BOTTOM, padx=10, pady=10)

# Draw the initial squares and messages
padding = 10
square_size = 0  # Initialize square_size
resize_canvas(tk.Event())

# Start the tkinter event loop
window.mainloop()
