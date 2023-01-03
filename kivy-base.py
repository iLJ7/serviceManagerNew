import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition, Screen
from ctypes import windll
from threading import Timer

# Importing Event from the threading module
from threading import Event
windll.shcore.SetProcessDpiAwareness(1)

class HomeWindow(Screen):
    pass

global truckButtons
truckButtons = []
seen = []

global indicator
indicator = 0

class TrucksWindow(Screen):

    def remove(self, id):
        grid = self.ids.trucksgrid

        if id in grid.children:
            print('yeah')
            grid.remove_widget(id)
        
        print(len(grid.children))

    def storeButtons(self, id):
        
        global indicator
        if not(indicator):

            for c in id.children:
                if c not in seen:
                    truckButtons.append(c)
                
                else:
                    seen.append(c)
            
            indicator = 1
        
        self.bindSearch()

    def refill(self, id):

        tmp = []
        for c in id.children:
            print(c)
            tmp.append(c)
        
        for t in tmp:
            id.remove_widget(t)

        print('Refilling - there are ' + str(len(id.children)))

        for i, c in enumerate(truckButtons):
            print(c)
            id.add_widget(truckButtons[len(truckButtons) - i - 1])

    pass

    def loadTrucks(self, id):
        self.storeButtons(id)
        self.refill(id)

    def bindSearch(self):

        grid = self.ids.trucksgrid
        searchBar = self.ids.search

        def refill(self, e):
            print('Change detected.')

            tmp = []
            for c in grid.children:
                print(c)
                tmp.append(c)

            for t in tmp:
                grid.remove_widget(t)
            
            for i, c in enumerate(reversed(truckButtons)):
                print(c)
                
                if c.name == "select" or searchBar.text in c.name:
                    grid.add_widget(truckButtons[len(truckButtons) - i - 1])

        self.ids.search.bind(text=refill)

class WindowManager(ScreenManager):
    pass

# Builder.load_file('home.kv')

kv = Builder.load_file('design.kv')

class MyApp(App):

    def build(self):
        Window.maximize()
        return kv

if __name__ == '__main__':
    MyApp().run()
    print(len(truckButtons))
