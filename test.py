from tkinter import *
from tkinter import ttk
from ctypes import windll
from turtle import bgcolor

from main import main
windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title('Learn To Code at Codemy.com')
root.state('zoomed')
# Create A Main Frame
main_frame = Frame(root)
main_frame.pack()

# Create A Canvas
my_canvas = Canvas(main_frame, height=1080, width=1920)
my_canvas.pack()

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
# my_scrollbar.place(x=1780, y=0, height=300)

# Configure The Canvasy
my_canvas.configure(yscrollcommand=my_scrollbar.set)

my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

def _on_mouse_wheel(event):
    my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
    
my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

# Create ANOTHER Frame INSIDE the Canvas
second_frame = Frame(my_canvas, height=1080, width=1920, bg='white')
second_frame.pack()
# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

posY=0
altura = 0

buttons = []

select = PhotoImage(file='select.png')
selectButton = Label(second_frame, image=select, height=280, bg='white')
selectButton.image = select

click_btn1 = PhotoImage(file="151-kk-142.png")
button1 = Button(second_frame, bg='white', image=click_btn1, height=300, width=1920, borderwidth = 0, command=lambda: up_frame("151-kk-142"))
button1.image = click_btn1 # keep a reference!

click_btn2 = PhotoImage(file="181-wx-2860.png")
button2 = Button(second_frame, bg='white', image=click_btn2, height=300, width=1920, borderwidth = 0, command=lambda: up_frame("181-wx-2860"))
button2.image = click_btn2

click_btn3 = PhotoImage(file="171-kk-7900.png")
button3 = Button(second_frame, bg='white', image=click_btn3, height=300, width=1920, borderwidth = 0, command=lambda: up_frame("171-kk-7900"))
button3.image = click_btn3

buttons.append(selectButton)
buttons.append(button1)
buttons.append(button2)
buttons.append(button3)

for button in buttons:
    button.pack()

root.mainloop()
