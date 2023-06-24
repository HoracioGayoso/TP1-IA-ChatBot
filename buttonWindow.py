# This will import all the widgets
# and modules which are available in
# tkinter and ttk module
from tkinter import *
from tkinter.ttk import *
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

# creates a Tk() object
master = Tk()

# sets the geometry of main
# root window
master.geometry("800x600")
center(master)


# function to open a new window
# on a button click
def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(master)

    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")

    # sets the geometry of toplevel
    newWindow.geometry("800x600")
    center(newWindow)


    # A Label widget to show in toplevel
    Label(newWindow,
          text="This is a new window").pack()


# label = Label(master,
#               text="This is the main window")
#
# label.pack(pady=10)

# a button widget which will open a
# new window on button click
# btn = Button(master,
#              text="Click to open a new window",
#              command=openNewWindow)
# btn.pack(pady=10)

# mainloop, runs infinitely

w = Canvas(master, width=250, height=200)
w.create_rectangle(0, 0, 200, 100, fill="blue", outline = 'blue')
message = "Hello, Square!"
w.create_text(100, 100, text=message, font=("Arial", 14), fill="black")
w.pack()
mainloop()