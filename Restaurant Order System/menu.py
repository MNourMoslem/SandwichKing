from tkinter import Frame, Label, Button, LabelFrame, NSEW, Canvas, Scrollbar
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd



class MainFrame:
    def __init__(self, window, menu):
        self.window = window
        self.title = 'Menu'
        self.menu = menu
        self.sections = []
        self.sections_name = []
        self.last_section = 'main'
        self.n_selected_dishs = 0
        self.selected_dishs_price = 0

        self.frame = LabelFrame(self.window, bg='#F9F5E7', relief='flat')
        self.titleFrame = Frame(self.frame, relief='solid', bg='#F9F5E7')
        self.menuCanvas = Canvas(self.frame, bg='#F9F5E7')
        self.menuFrame = Frame(self.menuCanvas, bg='#F9F5E7')
        self.scrollbar = Scrollbar(self.menuCanvas, orient='vertical', command=self.menuCanvas.yview, bg='#F9F5E7')

        self.menuCanvas.config(yscrollcommand=self.scrollbar.set)

        backBtn = Button(self.titleFrame, text='Back', command=self.closeSection, font=('Raleway', 12), bg='#DDDDDD')
        self.title_label = Label(self.titleFrame, text=self.title, font=('Raleway', 24), bg='#F9F5E7')
        showOrderBtn = Button(self.titleFrame, text='Show Order', command=self.showOrder, font=('Raleway', 12), bg='#DDDDDD')

        self.titleFrame.columnconfigure(0, minsize=75)
        self.titleFrame.columnconfigure(1, minsize=300)
        self.titleFrame.columnconfigure(2, minsize=75)

        self.titleFrame.grid(row=0, column=0, pady=10)
        self.menuCanvas.grid(row=1, column=0, pady=5)
        self.menuFrame.pack(side='left')
        self.scrollbar.pack(side='right', fill='y')

        backBtn.grid(row=0, column=0, sticky='w', padx=(20, 0))
        self.title_label.grid(row=0, column=1)
        showOrderBtn.grid(row=0, column=2, sticky='e', padx=(0 ,20))

        self.frame.pack()

    def addSection(self, section):
        self.sections.append(section)
        self.sections_name.append([section.name, (len(self.sections) - 1)])

    def removeSection(self, section_name):
        for section in self.sections_name:
            if section[0] == section_name:
                self.sections.pop(section[1])
                self.sections_name.pop(section[1])

    def openSection(self, section):
        self.title_label.config(text=f"Menu - {section.name}", font=('Raleway', 16))
        self.offshow()
        section.openDishes()
        self.last_section = section

    def closeSection(self):
        if self.last_section == 'order':
            for section in self.sections:
                section.closeSelectedDishes()
            self.title_label.config(text=self.title, font=('Raleway', 24))
            self.last_section = 'main'
            self.onshow()

        elif self.last_section != 'main':
            self.last_section.closeDishes()
            self.title_label.config(text=self.title, font=('Raleway', 24))
            self.last_section = 'main'
            self.onshow()
        self.menu.main.displayMain()

    def showOrder(self):
        if self.n_selected_dishs == 0:
            self.menu.sentWarning("You don't have anything in your order")
        else:
            if self.last_section == 'main':
                self.title_label.config(text=f"Menu - Your Order", font=('Raleway', 16))
                self.offshow()
                for section in self.sections:
                    section.openSelectedDishes()
                self.last_section = 'order'
            elif self.last_section == 'order':
                self.closeSection()
                self.showOrder()
            elif self.last_section != 'main' and self.last_section != 'order':
                self.closeSection()
                self.showOrder()
    
    def onshow(self):
        for section in self.sections:
            section.onshow()

    def offshow(self):
        for section in self.sections:
            section.offshow()


class Section:
    def __init__(self, master, name, image_path, mainframe):
        self.mainframe = mainframe
        self.master = master
        self.name = name
        self.image = ImageTk.PhotoImage(Image.open(image_path).resize((65, 65)))
        self.dishes = []
        self.dishes_name = []

        self.frame = LabelFrame(self.master, bg='#A2CDB0', relief='flat')

        sectionImg = Label(self.frame, image=self.image, bg='#A2CDB0')
        sectionName = Label(self.frame, font=('Raleway', 18), text=self.name, bg='#A2CDB0')

        openSectionBtn = Button(self.frame, text='Open', command=self.openSection, padx=10, pady=10, font=('Raleway', 14), bg='#DDDDDD')

        self.frame.columnconfigure(0, minsize=75)
        self.frame.columnconfigure(1, minsize=250)
        self.frame.columnconfigure(2, minsize=75)

        sectionImg.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        sectionName.grid(row=0, column=1, padx=5, pady=5)
        openSectionBtn.grid(row=0, column=2, sticky='e', padx=(15, 5), pady=5)

    def addDish(self, dish):
        self.dishes.append(dish)
        self.dishes_name.append([dish.name, (len(self.dishes) - 1)])

    def removeDish(self, dish_name):
        for dish in self.dishes_name:
            if dish[0] == dish_name:
                self.dishes.pop(dish[1])
                self.dishes_name.pop(dish[1])

    def openSection(self):
        self.mainframe.openSection(self)

    def openDishes(self):
        for dish in self.dishes:
            dish.onshow()

    def closeDishes(self):
        for dish in self.dishes:
            dish.offshow()
    
    def openSelectedDishes(self):
        for dish in self.dishes:
            if dish.dish_is_selected:
                dish.onshowSelected()
    
    def closeSelectedDishes(self):
        for dish in self.dishes:
                dish.offshowSelected()

    def onshow(self):
        self.frame.pack(pady=1)

    def offshow(self):
        self.frame.pack_forget()


class Dish:
    def __init__(self, name, price, section_name, description,image_path, section_class):
        self.section = section_class
        self.section_name = section_name
        self.name = name
        self.image_path = image_path
        self.image = ImageTk.PhotoImage(Image.open(self.image_path).resize((65, 65)))
        self.description = description
        self.price = price
        self.n_selection = 0
        self.dish_is_selected = False
        self.message = None

        self.frame = LabelFrame(section_class.master, bg='#A2CDB0')

        dishImg = Label(self.frame, image=self.image, bg='#A2CDB0')
        dishName = Label(self.frame, text=self.name, font=('Raleway', 10), bg='#A2CDB0')
        dishPrice = Label(self.frame, text=f'{self.price}$', font=('Arial', 10, 'bold'), bg='#A2CDB0')
        addDishBtn = Button(self.frame, text='Add', command=self.addDish, padx=12, bg='#DDDDDD')
        removeDishBtn = Button(self.frame, text='Remove', command=self.removeDish, bg='#DDDDDD')
        infoDishBtn = Button(self.frame, text='Info', pady=20, command= self.showDishInfo, bg='#DDDDDD')
        self.numOfSelection = Label(self.frame, text=self.n_selection, font=('Raleway', 12, 'bold'), background='red', bg='white')

        self.frame.columnconfigure(1, minsize=75)
        self.frame.columnconfigure(2, minsize=200)
        self.frame.columnconfigure(3, minsize=25)
        self.frame.columnconfigure(4, minsize=35)
        self.frame.columnconfigure(5, minsize=25)

        dishImg.grid(row=0, column=1, rowspan=2,sticky='w', padx=(0, 5), pady=5)
        dishName.grid(row=0, column=2, rowspan=2, padx=6, pady=5)
        addDishBtn.grid(row=0, column=3, padx=6, pady=5)
        removeDishBtn.grid(row=1, column=3, padx=6, pady=5)
        dishPrice.grid(row=0, column=4, rowspan=2, padx=6, pady=5)
        infoDishBtn.grid(row=0, column=5, rowspan=2, sticky='e', padx=6, pady=5)

    def addDish(self):
        if self.section.mainframe.selected_dishs_price + self.price <= 1000: 
            self.section.mainframe.n_selected_dishs += 1
            self.section.mainframe.selected_dishs_price += self.price
            self.n_selection += 1
            self.numOfSelection.config(text=self.n_selection)
            if self.n_selection == 1:
                self.dish_is_selected = True
                self.numOfSelection.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)
                self.frame.columnconfigure(0, minsize=25)
            self.section.mainframe.menu.addDishToInvoice([self.name, self.section_name, self.price, 1])
        else:
            self.section.mainframe.menu.sentWarning("Your Order Total Cost Can't Be More Than 1000$")
    def removeDish(self):
        if self.n_selection > 0:
            self.section.mainframe.n_selected_dishs -= 1
            self.section.mainframe.selected_dishs_price -= self.price
            self.n_selection -= 1
            self.numOfSelection.config(text=self.n_selection)
        if self.n_selection == 0:
            self.dish_is_selected = False
            self.numOfSelection.grid_forget()
            self.frame.columnconfigure(0, minsize=0)
        self.section.mainframe.menu.removeDishFromInvoice(self.name)

    def showDishInfo(self):
        self.section.mainframe.menu.showDishInfo((self.name, self.image_path, self.section_name, self.price, self.description))

    def onshowSelected(self):
        self.frame.pack(pady=1)

    def offshowSelected(self):
        self.frame.pack_forget()

    def onshow(self):
        self.frame.pack(pady=1)

    def offshow(self):
        self.frame.pack_forget()


class Menu:
    def __init__(self, window, main, coords, padx=None, pady=None,coords_expand = None, sticky = None):
        self.window = window
        self.coords = coords
        self.main = main
        self.coords_expand = ((1, 1) if coords_expand == None else coords_expand)
        self.sticky = sticky
        self.frame = Frame(self.window, relief='solid', bg='white')
        self.padx = 0 if padx == None else padx
        self.pady = 0 if pady == None else pady
        self.mainframe = MainFrame(self.frame, self)
        self.data = pd.read_csv('Data\\Menu.csv', index_col=0)

        self.sections_names = self.data['Class'].unique()
        self.dishes_data = self.data[['Food', 'Price', 'Class', 'Description', 'Path']].values

        self.section_dish_index = {}

        self.sections = [Section(self.mainframe.menuFrame, section, f'Data\\Dishes\\{section}\\Section Photo.jpg', self.mainframe)
                         for section in self.sections_names]
        for section in self.sections:
            self.section_dish_index[section.name] = section

        self.dishes = []
        for dish in self.dishes_data:
            item = Dish(dish[0], dish[1], dish[2], dish[3], dish[4], self.section_dish_index[dish[2]])
            self.section_dish_index[dish[2]].addDish(item)
            self.dishes.append(item)

        for section in self.sections:
            self.mainframe.addSection(section)

        
        self.frame.grid(row=self.coords[0], column=self.coords[1], rowspan=self.coords_expand[0], columnspan=self.coords_expand[1], sticky=self.sticky, padx=self.padx, pady=self.pady)
        self.mainframe.onshow()

    def showDishInfo(self, info):
        if self.main != None:
            self.main.displayInfo(info)

    def addDishToInvoice(self, dish):
        self.main.addDishToInvoice(dish)

    def removeDishFromInvoice(self, dish):
        self.main.removeDishFromInvoice(dish)

    def sentWarning(self, info):
        self.main.setWarning(info)
