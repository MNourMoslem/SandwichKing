from tkinter import Frame, Label, Tk, LabelFrame, NSEW
from PIL import Image, ImageTk
import pandas as pd

class Screen:
    def __init__(self, window, main, coords,  padx=None, pady=None,coords_expand=None, sticky = None):
        self.window = window
        self.coords = coords
        self.main = main
        self.coords_expand = coords_expand or (None, 2)
        self.sticky = NSEW if sticky == None else sticky 
        self.padx = 0 if padx == None else padx
        self.pady = 0 if pady == None else pady
        self.frame = Frame(self.window, width=700, height=300, bg='#F9F5E7')
        self.frame.grid(row=int(self.coords[0]), column=int(self.coords[1]), rowspan=self.coords_expand[0], columnspan=int(self.coords_expand[1]), sticky=self.sticky,padx=self.padx, pady=self.pady)

        self.mainFrame = Frame(self.frame)
        self.secondFrame = Frame(self.frame)

        self.last_frame = False
        self.last_img = None
        self.last_name = None
        self.last_section = None
        self.last_price = None
        self.last_description = None

        mainFrameImage = Image.open('Data\images\Welcome.png').resize((639, 290))
        mainFramePhotoImage = ImageTk.PhotoImage(mainFrameImage)
        self.mainLabel = Label(self.mainFrame, image=mainFramePhotoImage)
        self.mainLabel.image = mainFramePhotoImage
        self.mainLabel.pack()

        self.mainFrame.pack()


    def showInfo(self, dish_name, dish_image, dish_section, dish_price, dish_description):

        self.mainFrame.pack_forget()  
        if not self.last_frame:
                self.secondFrame = Frame(self.frame, bg='#F9F5E7')

                image = Image.open(dish_image).resize((150, 150))
                photo_image = ImageTk.PhotoImage(image)
                imgLabel = Label(self.secondFrame, image=photo_image, bg='#F9F5E7')
                imgLabel.image = photo_image

                nameFrame = LabelFrame(self.secondFrame ,text='Dish', font=('Raleway', 15),padx=10, pady=10, bg='#F9F5E7')
                nameLabel = Label(nameFrame, text=dish_name, font=('Raleway', 24), bg='#F9F5E7')

                sectionFrame = LabelFrame(self.secondFrame ,text='Section', font=('Raleway', 12),padx=10, pady=10, bg='#F9F5E7')
                sectionLabel = Label(sectionFrame, text=dish_section, font=('Raleway', 20), bg='#F9F5E7')

                priceFrame = LabelFrame(self.secondFrame ,text='Price', font=('Raleway', 12),padx=7, pady=7, bg='#F9F5E7')
                priceLabel = Label(priceFrame, text=f'{dish_price}$', font=('Raleway', 18), bg='#F9F5E7')

                descriptionFrame = LabelFrame(self.secondFrame ,text='Description', font=('Raleway', 14),padx=7, pady=7, bg='#F9F5E7')
                descriptionLabel = Label(descriptionFrame, text=dish_description, font=('Raleway', 12), wraplength=600, justify='left', bg='#F9F5E7')

                imgLabel.grid(row=0, column=0, rowspan=2, columnspan=2)

                nameFrame.grid(row=0, column=2, columnspan=2, sticky=NSEW, padx=(0, 10))
                nameLabel.pack()

                sectionFrame.grid(row=1, column=2,sticky=NSEW, padx=(0, 10))
                sectionLabel.pack()
                
                priceFrame.grid(row=1, column=3,sticky=NSEW, padx=(0, 10))
                priceLabel.pack()

                descriptionFrame.grid(row=2, column=0, sticky=NSEW, columnspan=4)
                descriptionLabel.pack()
  
                self.secondFrame.pack()

                self.last_frame = True

                self.last_img = imgLabel
                self.last_name = nameLabel
                self.last_section = sectionLabel
                self.last_price = priceLabel
                self.last_description = descriptionLabel
        else:
            image = Image.open(dish_image).resize((150,150))
            photo_image = ImageTk.PhotoImage(image)
            self.last_img.config(image = photo_image)
            self.last_img.image = photo_image

            self.last_name.config(text=dish_name)
            self.last_section.config(text=dish_section)
            self.last_price.config(text=f'{dish_price}$')
            self.last_description.config(text=dish_description)
   
            self.secondFrame.pack()

    def showMain(self):
        self.secondFrame.pack_forget()    
        self.mainFrame.pack()
             