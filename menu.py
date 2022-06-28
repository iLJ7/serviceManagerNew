from tkinter import *

root = Tk()
root.title("Menu test")

my_menu = Menu(root)
root.config(menu=my_menu)


select = PhotoImage(file='select.png')
file_menu = Menu(my_menu)
my_menu.add_cascade(image=select, menu=file_menu)

root.mainloop()