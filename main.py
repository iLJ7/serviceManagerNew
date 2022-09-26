#!/usr/bin/env python3
from mailbox import linesep
from datetime import datetime
import os, time, copy
import tkinter as tk
from truckDB import truckDB
from rectificationDB import rectificationDB 
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

        global lines, statuses
        lines = []
        statuses = {}

        for i in range(0, 67):
            line = 'line' + str(i)
            statuses[line] = True
            lines.append(line)
  
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

            page_name = addInspectionPage.__name__ + trucks[i][0][:-4]
            frame = addInspectionPage(parent = container, controller = self, truck = truck, index = 1)
            frame.configure(bg='white')
            frame.grid(row=0, column=0, sticky='nsew')
            allPages[page_name] = frame
            global currentPage
            currentPage = 1
    
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
        addInsp = Button(self, bg='white', image=AddInspIcon, height=180, width=400, borderwidth= 0, command=lambda: [print("Opening add inspection page."), up_frame('addInspectionPage' + truck[0][:-4])])
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

class addInspectionPage(tk.Frame):
    def __init__(self, parent, controller, truck, index=1):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        home = PhotoImage(file='home.png')
        homeButton = Button(self, image=home, borderwidth=0, bg='white', command=lambda: up_frame('homePage'))
        homeButton.image = home
        homeButton.place(x=0, y=0)

        print(truck)
        goback = PhotoImage(file='goback.png')
        gobackButton = Button(self, image=goback, borderwidth=0, bg='white', command=lambda: [print('test'), passAllItems(), up_frame(truck[0][:-4])])
        gobackButton.image = goback
        gobackButton.place(x=0, y=200)

        buttons = []

        def buttonsFill():
            for i, line in enumerate(lines):
                lineimg = PhotoImage(file=line + '.png')
                lineButton = Button(self, text='Defect added.', fg="white", image=lineimg, borderwidth=0, bg='white')
                lineButton.image = lineimg
                lineButton.name = line
                index = i
                lineButton.configure(command= lambda index=index: changeIt(index), text='Defect added.', fg="white", font=('Arial', 7), compound= LEFT)
                buttons.append(lineButton)

        print(lines)

        def fill(a, z):
            for button in buttons[a:z]:
                button.pack(padx=(0, 310))

        for i, button in enumerate(buttons):
            button.id = i
            #print(button.id)
        
        def changeIt(buttonID):

            # How do we determine which buttons to change?
            x = PhotoImage(file='line' + str(buttonID) + '-red' + '.png')
            y = PhotoImage(file='line' + str(buttonID) + '.png')
            
            if statuses[buttons[buttonID].name] is False:
                buttons[buttonID].configure(text='Defect added.', fg="white", font=('Arial', 7), image=y, compound= LEFT)
                buttons[buttonID].image = y
                statuses[buttons[buttonID].name] = True
            
            else:
                buttons[buttonID].configure(text='Defect added.', fg="black", font=('Arial', 7), image=x, compound= LEFT)
                buttons[buttonID].image = x
                statuses[buttons[buttonID].name] = False

        # Adding the title 'Vehicle Inspection Report'.
        y = PhotoImage(file='vehicle-inspection-report.png')
        heading = Label(self, image=y, borderwidth=0, relief="groove")
        heading.image=y
        heading.pack(pady=(0, 270))

        z = PhotoImage(file='operator.png')
        check = Label(self, image=z, bg='white', borderwidth=0, width=100)
        check.image = z
        check.place(x=245, y=140)

        odometerImage = PhotoImage(file='odometer-reading.png')
        odometer = Label(self, image=odometerImage, bg='white', borderwidth=0)
        odometer.image = odometerImage
        odometer.place(x=232, y=210)

        nameOfInspector = PhotoImage(file='name-of-inspector.png')
        nameOfInspectorLabel = Label(self, image=nameOfInspector, bg='white', borderwidth=0)
        nameOfInspectorLabel.image = nameOfInspector
        nameOfInspectorLabel.place(x=234, y=280)

        odBox = Text(self, height = 1, width = 14)
        odBox.place(x=430, y=215)
        
        insBox = Text(self, height = 1, width = 14)
        insBox.place(x=430, y=285)
        
        clicked = StringVar()

        drop = ttk.OptionMenu(self, clicked, 'John Doe', 'John Doe', 'James Low', 'Henry Smith')
        drop.place(x=430, y=142)
        
        vehicleRegFleetNo = PhotoImage(file='vehicle-reg-fleet-no.png')
        vehicleRegFleetNoLabel = Label(self, image=vehicleRegFleetNo, bg='white', borderwidth=0)
        vehicleRegFleetNoLabel.image = vehicleRegFleetNo
        vehicleRegFleetNoLabel.place(x=600, y=140)

        insideCab = PhotoImage(file='inside-cab.png')
        insideCabLabel = Label(self, image=insideCab, bg='white', borderwidth=0)
        insideCabLabel.image = insideCab
        insideCabLabel.place(x=153, y=345)        
        
        vehicleRegFleetNo = PhotoImage(file='vehicle-reg-fleet-no.png')
        vehicleRegFleetNoLabel = Label(self, image=vehicleRegFleetNo, bg='white', borderwidth=0)
        vehicleRegFleetNoLabel.image = vehicleRegFleetNo
        vehicleRegFleetNoLabel.place(x=600, y=140)

        vehicleRegFleetText = truck[0][:-4]
        vehicleRegFleetNoLabel = Label(self, text=vehicleRegFleetText, bg='white', borderwidth=0, font=('Arial', 12))
        vehicleRegFleetNoLabel.place(x=808, y=142)

        vehicleMakeModel = PhotoImage(file='make-model.png')
        vehicleMakeModelLabel = Label(self, image=vehicleMakeModel, bg='white', borderwidth=0)
        vehicleMakeModelLabel.image = vehicleMakeModel
        vehicleMakeModelLabel.place(x=600, y=210)
        
        vehicleMakeAndModel = truck[1] + ' ' + truck[2]
        print(vehicleMakeAndModel)
        vehicleMakeModelAnswer = Label(self, text=vehicleMakeAndModel, bg='white', borderwidth=0, font=('Arial', 12))
        vehicleMakeModelAnswer.place(x=808, y=212)

        date = PhotoImage(file='date.png')
        dateLabel = Label(self, image=date, bg='white', borderwidth=0)
        dateLabel.image = date
        dateLabel.place(x=600, y=280)

        now = datetime.now()
        currentDate = str(now.strftime("%d/%m/%Y"))

        dateLabelAnswer = Label(self, text=currentDate, bg='white', borderwidth=0, font=('Arial', 12))
        dateLabelAnswer.place(x=808, y=283)
        
        heading = PhotoImage(file='heading.png')
        headingLabel = Label(self, image=heading, bg='black', borderwidth=1, font=('Arial', 12))
        headingLabel.image = heading
        headingLabel.place(x=190, y=370)

        passAll = PhotoImage(file='pass-all.png')
        passAllButton = Button(self, image=passAll, bg='white', borderwidth=0, command= lambda: passAllItems())
        passAllButton.image = passAll
        passAllButton.place(x=1650, y=381)

        buttonsFill()
        fill(0, 22)

        def passAllItems():
            
            clicked.set('John Doe')
            odBox.delete('1.0', END)
            insBox.delete('1.0', END)
            
            try:
                for i, button in enumerate(buttons):
                    t = PhotoImage(file=lines[i] + ".png")
                    button.image = t
                    button.configure(image=t, text='Defect added.', fg="white", font=('Arial', 7), compound= LEFT)
                    statuses[buttons[i].name] = True
            
            except:
                pass
        
        next = PhotoImage(file='next-2-3.png')
        nextButton = Button(self, image=next, bg='white', borderwidth=0, command=lambda: nextPage())
        nextButton.image = next
        nextButton.place(x=1650, y=890)
        
        prev = PhotoImage(file='prev-1-3.png')
        prevButton = Button(self, bg='white', borderwidth=0, command=lambda: prevPage())
        prevButton.image = prev
        prevButton.place(x=20, y=890)

        finish = PhotoImage(file='finish.png')
        finishButton = Button(self, bg='white', borderwidth=0, command=lambda: [finishPage()])
        finishButton.image = finish
        finishButton.place(x=1650, y=890)

        global rectLabels
        rectLabels = []

        def nextPage():

            for button in buttons:
                button.pack_forget()

            global currentPage
            currentPage += 1
            print(currentPage)

            if currentPage == 1:
                finishButton.place_forget()
                next1 = PhotoImage(file='next-2-3.png')
                nextButton.configure(image=next1)
                nextButton.image(next1)

                fill(0, 22)

            elif currentPage == 2:
                finishButton.place_forget()
                next2 = PhotoImage(file='next-3-3.png')
                nextButton.configure(image=next2)
                nextButton.image = next2

                prev1 = PhotoImage(file='prev-1-3.png')
                prevButton.configure(image=prev1)
                prevButton.image = prev1
                prevButton.place(x=7, y=890)

                fill(22, 45) # fill the respective pages
            
            else:
                nextButton.place_forget()
                
                prev2 = PhotoImage(file='prev-2-3.png')
                prevButton.configure(image=prev2)
                prevButton.image = prev2
                prevButton.place(x=7, y=890)

                finish = PhotoImage(file='finish.png')
                finishButton.configure(image=finish)
                finishButton.image = finish
                finishButton.place(x=1650, y=890)

                fill(45, 68) # fill the respective pages
                
            print(truck)
        
        def prevPage():

            for button in buttons:
                button.pack_forget()

            global currentPage
            currentPage -= 1
            
            print(currentPage)

            if currentPage == 1:
                
                finishButton.place_forget()
                next1 = PhotoImage(file='next-2-3.png')
                nextButton.configure(image=next1)
                nextButton.image = next1
                nextButton.place(x=1650, y=890)

                prevButton.place_forget()
                fill(0, 22)

            elif currentPage == 2:

                finishButton.place_forget()
                next2 = PhotoImage(file='next-3-3.png')
                nextButton.configure(image=next2)
                nextButton.image = next2
                nextButton.place(x=1650, y=890)

                prev1 = PhotoImage(file='prev-1-3.png')
                prevButton.configure(image=prev1)
                prevButton.image = prev1
                prevButton.place(x=7, y=890)
                fill(22, 45)

            else:
                nextButton.place_forget()
                prev2 = PhotoImage(file='prev-2-3.png')
                prevButton.configure(image=prev2)
                prevButton.image = prev2
                prevButton.place(x=7, y=890)
                fill(45, 68) # fill the respective pages

        def finishPage():
            headingLabel.place_forget()
            prevButton.place_forget()
            finishButton.place_forget()
            insideCabLabel.place_forget()
            passAllButton.place_forget()
            # We also want to remove past rectifications.

            global rectLabels

            for label in rectLabels:
                label.place_forget()

            global generateSheetButton
            try:
                generateSheetButton.place_forget()

            except:
                pass

            try:
                global signatureOfInspectorLabel
                signatureOfInspectorLabel.pack_forget()

            except:
                pass

            try:
                global backToRectificationsButton
                backToRectificationsButton.place_forget()

            except:
                pass

            try:
                global signatureButtons

                for button in signatureButtons:
                    button.pack_forget()
            
            except:
                pass

            for button in buttons:
                button.pack_forget()

            headingRectification = PhotoImage(file='heading-rectification.png')
            headingRectificationLabel = Label(self, image=headingRectification, bg='black', borderwidth=1, font=('Arial', 12))
            headingRectificationLabel.image = headingRectification
            headingRectificationLabel.place(x=251, y=375)

            cancel = PhotoImage(file='cancel.png')
            cancelButton = Button(self, image=cancel, borderwidth = 0, bg='white', command=lambda: cancelIt())
            cancelButton.image = cancel
            cancelButton.place(x=230, y=890)

            def cancelIt():

                print('Cancelling')
                next1 = PhotoImage(file='next-2-3.png')
                nextButton.configure(image=next1)
                nextButton.image = next1
                nextButton.place(x=1650, y=890)

                passAllItems()

                addRectificationButton.place_forget()
                cancelButton.place_forget()
                headingRectificationLabel.place_forget()
                signButton.place_forget()
                headingLabel.place(x=190, y=370)

                for label in rectLabels:
                    label.place_forget()

                global currentPage
                currentPage = 1
                fill(0, 22)

            addRectification = PhotoImage(file='add-rectification.png')
            addRectificationButton = Button(self, image=addRectification, borderwidth = 0, bg='white', command=lambda: addRect())
            addRectificationButton.image = addRectification
            addRectificationButton.place(x=760, y=876)

            sign = PhotoImage(file='sign.png')
            signButton = Button(self, image=sign, borderwidth = 0, bg='white', command=lambda: signIt())
            signButton.image = sign
            signButton.place(x=1430, y=876)
            
            def signIt():
                
                print('Opening sign page.')
                headingRectificationLabel.place_forget()
                addRectificationButton.place_forget()
                signButton.place_forget()
                cancelButton.place_forget()

                for label in rectLabels:
                    label.place_forget()

                global signatureOfInspectorLabel

                signatureOfInspector = PhotoImage(file='signature-of-inspector.png')
                signatureOfInspectorLabel = Label(self, image=signatureOfInspector, borderwidth=0)
                signatureOfInspectorLabel.image = signatureOfInspector
                signatureOfInspectorLabel.pack()

                global backToRectificationsButton

                backToRectifications = PhotoImage(file='rectificationsBack.png')
                backToRectificationsButton = Button(self, image=backToRectifications, borderwidth = 0, bg='white', command=lambda: finishPage())
                backToRectificationsButton.image = backToRectifications
                backToRectificationsButton.place(x=5, y=900)

                global generateSheetButton
                generateSheet = PhotoImage(file='generate-sheet.png')
                generateSheetButton = Button(self, image=generateSheet, borderwidth = 0, bg='white', command=lambda: generate())
                generateSheetButton.image = generateSheet
                generateSheetButton.place(x=1450, y=900)

                signatures = ['signature-luke.png', 'signature-alex.png']
                global signatureButtons
                signatureButtons = []

                for index, sig in enumerate(signatures):
                    sigImage = PhotoImage(file='signatures/' + sig)
                    sigButton = Button(self, text='Defect added.', fg="white", image=sigImage, command= lambda index=index: selectSignature(index),  borderwidth=0, bg='white')
                    sigButton.image = sigImage
                    signatureButtons.append(sigButton)
                
                for button in signatureButtons:
                    button.pack()

                global selectedSignature
                selectedSignature = None

                def selectSignature(index):
                    print('Changing signature')

                    global selectedSignature
                    selectedSignature = index

                    signatureButtons[index].configure(borderwidth = 1, relief='groove')

                    for i, button in enumerate(signatureButtons):
                        if i != selectedSignature:
                            button.configure(borderwidth = 0)

                    print(selectedSignature)


            def generate():
                # Here, we generate our inspection page.

                if selectedSignature is None:
                    print('Select a signature first.')

                print('We need to capture the information.')

                print('-------------')
                print(truck)
                print(selectedSignature)
                print(clicked.get())
                print(odBox.get('1.0',END).strip())
                print(insBox.get('1.0',END).strip())
                print(truck[0])
                now = datetime.now()
                currentDate = str(now.strftime("%d/%m/%Y"))
                print(currentDate)

                rectDB = rectificationDB('rectifications.db')
                rects = rectDB.fetch()
                    
            rectDB = rectificationDB('rectifications.db')
            rects = rectDB.fetch()
            print(rects)
            print(truck[0])

            for i, rect in enumerate(rects):
                checkNo = rect[1]
                rectAction = rect[2]
                rectBy = rect[3]

                print(checkNo, rectAction, rectBy)

                checkNoLabel = Label(self, text=checkNo, bg='white', font='Arial')
                checkNoLabel.text = checkNo
                rectLabels.append(checkNoLabel)

                rectActionLabel = Label(self, text=rectAction, width=20, borderwidth=0, bg='white', relief='solid', font='Arial')
                rectActionLabel.text = rectAction
                rectLabels.append(rectActionLabel)

                rectByLabel = Label(self, text=rectBy, width=20, borderwidth=0, bg='white', relief='solid', font='Arial')
                rectByLabel.text = rectBy
                rectLabels.append(rectByLabel)

                if rect[0] == truck[0]:
                    checkNoLabel.place(x=310, y=430 + (i * 30))
                    rectActionLabel.place(x=830, y=430 + (i * 30))
                    rectByLabel.place(x=1484, y=430 + (i * 30))

                #a = Label(self, text = " ".join(rect[1:2]) + " " * 100 + " ".join(rect[2:3]), bg='white', font='Arial')
                #a.pack()

            # Prompt box

            def addRect():
                x = Toplevel(self, height=200, width=350)
                x.title('Add Rectification')

                checkNoText = Label(x, text='Check No:')
                checkNoText.place(x=1, y=1)
                checkNoBox = Text(x, height=1, width=15)
                checkNoBox.place(x=150, y=5)

                rectActionText = Label(x, text='Rectification Action: ')
                rectActionText.place(x=1, y=40)
                rectActionBox = Text(x, height=1, width=15)
                rectActionBox.place(x=150, y=43)

                rectByText = Label(x, text='Rectified by:')
                rectByText.place(x=1, y=78)
                rectByBox = Text(x, height=1, width=15)
                rectByBox.place(x=150, y=81)

                confirmRect = Button(x, text='Confirm rectification.', command=lambda: [print('Trying to add rectification.'), insertRect()])
                confirmRect.place(x=100, y=130)
                
                def insertRect():

                    a = checkNoBox.get("1.0",END).strip()
                    b = rectActionBox.get("1.0",END).strip()
                    c = rectByBox.get("1.0",END).strip()

                    rectDB.insert(truck[0], a, b, c)

                    rects = rectDB.fetch()
                    lastRect = rects[len(rects) - 1]
                    print(lastRect)
              
                    checkNo = lastRect[1]
                    rectAction = lastRect[2]
                    rectBy = lastRect[3]

                    print(checkNo, rectAction, rectBy)

                    checkNoLabel = Label(self, text=checkNo, bg='white', font='Arial')
                    checkNoLabel.text = checkNo
                    checkNoLabel.place(x=310, y=430 + ((len(rects) - 1) * 30))

                    rectActionLabel = Label(self, text=rectAction, width=20, bg='white', font='Arial')
                    rectActionLabel.text = rectAction
                    rectActionLabel.place(x=830, y=430 + ((len(rects) - 1) * 30))

                    rectByLabel = Label(self, text=rectBy, width=20, bg='white', font='Arial')
                    rectByLabel.text = rectBy
                    rectByLabel.place(x=1484, y=430 + ((len(rects) - 1) * 30))

                    rectLabels.append(checkNoLabel)
                    rectLabels.append(rectActionLabel)
                    rectLabels.append(rectByLabel)
                
                    x.destroy()
                
            print('Finishing.')

def main():
    x = MainFrame()
    x.state("zoomed")
    x.title('Service Manager')
    x.mainloop()

if __name__ == "__main__":
    main()
