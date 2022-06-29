#!/usr/bin/env python3
import os
import tkinter as tk
from truckDB import truckDB
from tkinter import ttk
from datetime import datetime
from tkinter import *
from tkinter import font
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()
        
        self.configure(background='white')
        global allPages
        allPages = {}

        global truckdb
        truckdb = truckDB('trucks.db')
  
        #  Creating the home page.
        page_name = homePage.__name__
        frame = homePage(parent = container, controller = self) # Frame is an instance of each page class.
        frame.configure(bg='white')
        frame.grid(row=0, column=0, sticky = 'nsew')
        allPages[page_name] = frame

        # Creating the truck page
        page_name = truckPage.__name__
        frame = truckPage(parent = container, controller = self)
        frame.configure(bg='white')
        frame.grid(row=0, column=0, sticky='nsew')
        allPages[page_name] = frame

        # Creating the individual truck pages.
        trucks = truckdb.fetch()
        for i, truck in enumerate(trucks):
            page_name = trucks[i][0][:-4]
            frame = individualTruck(parent = container, controller = self, truck = truck)
            frame.configure(bg='white')
            frame.grid(row=0, column=0, sticky='nsew')
            allPages[page_name] = frame
    
        up_frame('homePage')

    global up_frame
    def up_frame(page_name):
        page = allPages[page_name]
        page.tkraise()

class homePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #self.controller.configure(background="white")
        #self.id = controller.id
        
        global homeController
        homeController = controller

        select = PhotoImage(file='select.png')
        selectButton = Label(self, image=select, height=280, borderwidth = 0, bg='white')
        selectButton.image = select
        selectButton.pack(padx=(10, 0))

        trucks= PhotoImage(file='trucks.png')
        trucksButton = Button(self, image=trucks, height=300, borderwidth = 0, bg='white', command=lambda: up_frame('truckPage'))
        trucksButton.image = trucks # keep a reference!
        trucksButton.pack()
        
        trailers = PhotoImage(file='trailers.png')
        trailersButton = Button(self, image=trailers, height=300, borderwidth = 0, bg='white', command=lambda: print("Trying to load trailers page.")) #self.controller.up_frame('trailersPage'))
        trailersButton.image = trailers
        trailersButton.pack()

class truckPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        container = Frame(self, bg='white')#, highlightbackground="yellow", highlightthickness=10)

        container.configure(height=1000, width=1920)

        container.pack_propagate(0)

        my_canvas = Canvas(container, bg='white')

        scrollbar = Scrollbar(container, orient="vertical", command=my_canvas.yview)
        scrollable_frame = Frame(my_canvas, bg='white')#, highlightbackground="blue", highlightthickness=10)

        scrollable_frame.bind(
        "<Configure>",
        lambda e: my_canvas.configure(
            scrollregion=my_canvas.bbox("all")
            )
        )

        my_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        my_canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill=BOTH, expand=True)
        my_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # mailbox_frame is second_frame
        # canvas is my_canvas
        # mail_scroll is my_scrollbar

        buttons = []

        home = PhotoImage(file='home.png')
        homeButton = Button(my_canvas, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.grid(row=0, column=0)
        homeButton.pack(side=TOP, anchor=NW, pady=(6, 0))

        select = PhotoImage(file='select.png')
        selectButton = Label(scrollable_frame, image=select, height=280, width=1900, bg='white')
        selectButton.image = select

        click_btn1 = PhotoImage(file="151-kk-142.png")
        button1 = Button(scrollable_frame, bg='white', image=click_btn1, height=300, width=1900, borderwidth = 0, command=lambda: up_frame("151-kk-142"))
        button1.image = click_btn1 # keep a reference!

        click_btn2 = PhotoImage(file="181-wx-2860.png")
        button2 = Button(scrollable_frame, bg='white', image=click_btn2, height=300, width=1900, borderwidth = 0, command=lambda: up_frame("181-wx-2860"))
        button2.image = click_btn2

        click_btn3 = PhotoImage(file="171-kk-7900.png")
        button3 = Button(scrollable_frame, bg='white', image=click_btn3, height=300, width=1900, borderwidth = 0, command=lambda: up_frame("171-kk-7900"))
        button3.image = click_btn3

        buttons.append(selectButton)
        buttons.append(button1)
        buttons.append(button2)
        buttons.append(button3)

        for i, b in enumerate(buttons):
            b.pack(side=TOP, anchor=NW)

        container.pack(fill=BOTH, expand=True)
        my_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class individualTruck(tk.Frame):
    def __init__(self, parent, controller, truck):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        s = 'truckPhotos/' + truck[0][:-4] + '-photo' + '.png'
        print(s)
        bg = PhotoImage(file = s)#truckPhoto[])
        label1 = Label(self, bg='white', image=bg)
        label1.image = bg
        label1.grid(row=1, column = 1)

        home = PhotoImage(file='home.png')
        homeButton = Button(self, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.grid(row=0, column=0, pady=(6, 0))

        click_btn1 = PhotoImage(file=truck[0])
        button1 = Label(self, bg='white', image=click_btn1, height=250, width=1410, borderwidth = 0)
        button1.image = click_btn1 # keep a reference!
        button1.grid(row=0, column=1)
     
        viewInspIcon = PhotoImage(file='view-inspection.png')
        viewInsp = Button(self, bg='white', image=viewInspIcon, height=180, width=400, borderwidth= 0, command=lambda: print("Trying to view inspection."))
        viewInsp.image = viewInspIcon
        viewInsp.place(x=1030, y=790)

        infoIcon = PhotoImage(file='info.png')
        info = Button(self, bg='white', image=infoIcon, height=180, width=180, borderwidth = 0, command=lambda: print('Trying to open info page.'))
        info.image = infoIcon
        info.place(x=1450, y=790)

        settingsIcon = PhotoImage(file='icon.png')
        settings = Button(self, bg='white', image=settingsIcon, height=180, width=180, borderwidth = 0, command=lambda: print('Trying to open settings page.'))
        settings.image = settingsIcon
        settings.place(x=1650, y=790)
        # Display some info from the database.
        trucks = truckdb.fetch()
        make, model, color, driver = str(truck[1]), str(truck[2]), str(truck[3]), str(truck[4])


def main():
    x = MainFrame()
    x.state("zoomed")
    x.title('Service Manager')
    x.mainloop()

if __name__ == "__main__":
    main()
