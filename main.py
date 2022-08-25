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

        global container
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

        # Creating the inspection pages.
        page_name = addInspectionPage.__name__
        frame = addInspectionPage(parent = container, controller = self)
        frame.configure(bg='white')
        frame.grid(row=0, column=0, sticky='nsew')
        allPages[page_name] = frame

        # Creating the info pages
        trucks = truckdb.fetch()
        for i, truck in enumerate(trucks):
            page_name = trucks[i][0][:-4] + 'info'
            frame = infoPage(parent = container, controller = self, truck = truck)
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
        homeButton.place(x=0, y=0)

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

        # Truck image
        s = 'truckPhotos/' + truck[0][:-4] + '-photo' + '.png'
        print(s)
        bg = PhotoImage(file = s)#truckPhoto[])
        label1 = Label(self, bg='white', image=bg)
        label1.image = bg
        label1.place(x=550, y=250)

        home = PhotoImage(file='home.png')
        homeButton = Button(self, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.place(x=0, y=0)
        #homeButton.grid(row=0, column=0, pady=(0, 37))

        goback = PhotoImage(file='goback.png')
        gobackButton = Button(self, image=goback, borderwidth=0, bg='white', command=lambda: up_frame('truckPage'))
        gobackButton.image = goback
        gobackButton.place(x=0, y=200)

        # Truck text
        click_btn1 = PhotoImage(file=truck[0])
        button1 = Label(self, bg='white', image=click_btn1, height=250, width=1510, borderwidth = 0)
        button1.image = click_btn1 # keep a reference!
        button1.place(x=200, y=10)

        AddInspIcon = PhotoImage(file='add-inspection.png')
        addInsp = Button(self, bg='white', image=AddInspIcon, height=180, width=400, borderwidth= 0, command=lambda: [print("Opening add inspection page."), up_frame('addInspectionPage')])
        addInsp.image = AddInspIcon
        addInsp.place(x=480, y=790)

        ViewInspIcon = PhotoImage(file='view-inspection.png')
        viewInsp = Button(self, bg='white', image=ViewInspIcon, height=180, width=400, borderwidth= 0, command=lambda: print("Trying to view inspection."))
        viewInsp.image = ViewInspIcon
        viewInsp.place(x=860, y=790)

        infoIcon = PhotoImage(file='info.png')
        info = Button(self, bg='white', image=infoIcon, height=180, width=180, borderwidth = 0, command=lambda: [print('Opening the info page for ' + truck[0][:-4] + 'info'), up_frame(truck[0][:-4] + 'info')])
        info.image = infoIcon
        info.place(x=1270, y=790)

        # Display some info from the database.
        trucks = truckdb.fetch()
        make, model, color, driver = str(truck[1]), str(truck[2]), str(truck[3]), str(truck[4])

class infoPage(tk.Frame):
    def __init__(self, parent, controller, truck):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = PhotoImage(file='home.png')
        homeButton = Button(self, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.place(x=0, y=0)
        
        goback = PhotoImage(file='goback.png')
        gobackButton = Button(self, image=goback, borderwidth=0, bg='white', command=lambda: up_frame(truck[0][:-4]))
        gobackButton.image = goback
        gobackButton.place(x=0, y=200)
    
        click_btn1 = PhotoImage(file=truck[0])
        button1 = Label(self, bg='white', image=click_btn1, height=250, width=1510, borderwidth = 0)
        button1.image = click_btn1 # keep a reference!
        button1.place(x=200, y=10)

        s = 'truckPhotos/' + truck[0][:-4] + '-photo' + '.png'
        print(s)
        bg = PhotoImage(file = s)#truckPhoto[])
        label1 = Label(self, bg='white', image=bg)
        label1.image = bg
        label1.place(x=1100, y=290)
        
        global my_list
        my_list = tk.Listbox(self, height=7, width=25, font=('Arial', 30))
        my_list.place(x=400, y=360)

        def initialListboxPopulate():
            my_list.delete(0, END)
            trucks = truckdb.fetch()
            for tr in trucks:
                if tr == truck:
                    make = 'Make: ' + tr[1]
                    my_list.insert(END, make)
            # Display some info from the database.
        
        initialListboxPopulate()
        trucks = truckdb.fetch()
        make, model, color, driver = str(truck[1]), str(truck[2]), str(truck[3]), str(truck[4])

class addInspectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        home = PhotoImage(file='home.png')
        homeButton = Button(self, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.place(x=0, y=0)

        line1 = PhotoImage(file="line1.png")
        line1Button = Button(self, image=line1, borderwidth=0, bg='white', command=lambda: changeStatus())
        line1Button.image = line1
        line1Button.pack()

        def changeStatus():
            print('Changing from green to red.')
            page_name = refreshInspectionPage.__name__
            frame = refreshInspectionPage(parent = container, controller = self)
            frame.configure(bg='white')
            frame.grid(row=0, column=0, sticky='nsew')
            allPages[page_name] = frame
            up_frame(page_name)
            
class refreshInspectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        home = PhotoImage(file='home.png')
        homeButton = Button(self, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.place(x=0, y=0)

        line1 = PhotoImage(file="line1-red.png")
        line1Button = Button(self, image=line1, borderwidth=0, bg='white', command=lambda: up_frame('addInspectionPage'))
        line1Button.image = line1
        line1Button.pack()

def main():
    x = MainFrame()
    x.state("zoomed")
    x.title('Service Manager')
    x.mainloop()

if __name__ == "__main__":
    main()
