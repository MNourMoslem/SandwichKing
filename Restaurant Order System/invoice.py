from tkinter import Frame, Label, LabelFrame, Canvas, Scrollbar, Tk, Button


class Invoice:

    def __init__(self, window, main, coords, coords_expand = None, sticky = None , padx = None, pady= None):
        self.window = window
        self.main = main
        self.coords = coords
        self.coords_expand = coords_expand or (1, 1)
        self.sticky = sticky
        self.invoiceItems = []
        self.cost = 0
        self.discount = 0

        self.frame = Frame(self.window, bg="#F9F5E7")
        self.frame.grid(row=self.coords[0], column=self.coords[1], rowspan=self.coords_expand[0], columnspan=self.coords_expand[1], sticky=self.sticky, padx=padx, pady=pady)

        self.labelFrame = LabelFrame(self.frame, bg="#F9F5E7")

        self.invoiceTitleLabel = Label(self.labelFrame, text=f'    Food', font=('Arial', 10, 'bold'), justify='left', width=32, anchor='w', bg="#F9F5E7")
        self.invoiceTitleLabel.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.priceTitleLabel = Label(self.labelFrame, text=f'  Price', font=('Arial', 10, 'bold'), justify='left', width=12, anchor='w', bg="#F9F5E7")
        self.priceTitleLabel.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.quantityTitleLabel = Label(self.labelFrame, text='Quantity', font=('Arial', 10, 'bold'), justify='left', width=12, anchor='w', bg="#F9F5E7")
        self.quantityTitleLabel.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        self.totalTitleLabel = Label(self.labelFrame, text=f'  Total', font=('Arial', 10, 'bold'), justify='left', width=12, anchor='w', bg="#F9F5E7")
        self.totalTitleLabel.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        self.invoiceCanvas = Canvas(self.labelFrame, bg='white', height=200)
        self.scrollBar = Scrollbar(self.labelFrame)

        self.invoiceCanvas.config(yscrollcommand=self.scrollBar.set)
        self.invoiceCanvas.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky='nsew')
        self.scrollBar.grid(row=1, column=4, sticky='ns')

        self.invoiceLabel = Frame(self.invoiceCanvas, bg="#F9F5E7")

        self.invoiceCanvas.create_window((0, 0), window=self.invoiceLabel, anchor='nw')

        self.invoiceTotalFrame = LabelFrame(self.frame, bg='white')
        self.invoiceTotalTextLabel = Label(self.invoiceTotalFrame, text='Total:',font=('Courier', 18, 'bold'), fg='black', bg='white')
        self.invoiceTotalNumLabel = Label(self.invoiceTotalFrame, text='0$',font=('Courier', 18, 'bold'), fg='black', bg='white')

        self.goToPaymentBtn = Button(self.frame, text='Go To Payment', padx=5, pady=5, font=('Courier', 12), command=self.goToPayment)

        self.discountLabel = Label(self.frame)

        self.labelFrame.pack(fill='x')
        self.invoiceTotalFrame.pack(fill='x', padx=(15, 0), pady=10, side='left')
        self.goToPaymentBtn.pack(padx=5, pady=10, side='right')
        self.invoiceTotalTextLabel.pack(side='left', padx=15)
        self.invoiceTotalNumLabel.pack(side='right', padx=15)

        self.invoiceCanvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def addToInvoice(self, info):
        def resizeText(text):
            if len(text) > 30:
                return str(text[:28]) + '...'
            else:
                return text

        if len(self.invoiceItems) != 0:
            for item in self.invoiceItems:
                if info[0] == item[0]:
                    item[1][3] += 1
                    item[1][4] = item[1][2] * item[1][3]
                    self.refreshInvoice()
                    return
            self.invoiceItems.append([info[0], [resizeText(info[0]), info[1], info[2], info[3], info[2] * info[3]]])
            self.refreshInvoice()
        else:
            self.invoiceItems.append([info[0], [resizeText(info[0]), info[1], info[2], info[3], info[2] * info[3]]])
            self.refreshInvoice()

    def removeFromInvoice(self, dish):
        for item in self.invoiceItems:
            if dish == item[0]:
                if item[1][3] > 1:
                    item[1][3] -= 1
                    item[1][4] = item[1][2] * item[1][3]
                else:
                    self.invoiceItems.remove(item)
        self.refreshInvoice()
                    
    def refreshInvoice(self):
        for widget in self.invoiceLabel.winfo_children():
            widget.destroy()

        self.cost = 0
        for i, item in enumerate(self.invoiceItems):
            item3 = str(item[1][3]) + 'x'

            item_frame = Frame(self.invoiceLabel, bg='white')

            food_label = Label(item_frame, text=f'{item[1][0]}\n({item[1][1]})', font=('Courier', 10), anchor='w', width=32, bg='white', justify='left')
            price_label = Label(item_frame, text=f'{item[1][2]}$', font=('Courier', 10), anchor='w', width=12, bg='white')
            quantity_label = Label(item_frame, text=item3, font=('Courier', 10), anchor='w', width=12, bg='white')
            total_label = Label(item_frame, text=f'{item[1][4]}$', font=('Courier', 10), anchor='w', width=7, bg='white')

            food_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
            price_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            quantity_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')
            total_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')

            separator = Frame(item_frame, height=2, relief='sunken', borderwidth=1, bg='black')
            separator.grid(row=1, column=0, columnspan=5, sticky='we')

            item_frame.grid(row=i, column=0, padx=10, pady=5, sticky='w')

            self.cost += int(item[1][4])
            
        self.cost -= self.cost*float(self.discount)
        self.invoiceTotalNumLabel.config(text=f'{self.cost}$')

        self.invoiceLabel.update_idletasks()

        self.invoiceCanvas.config(scrollregion=self.invoiceCanvas.bbox('all'))

        self.invoiceCanvas.yview_moveto(0.0)
        self.scrollBar.config(command=self.invoiceCanvas.yview)

        if len(self.invoiceItems) > 0:
            self.invoiceLabel.configure(borderwidth=1, relief='solid', bg='white')
        else:
            self.invoiceLabel.configure(borderwidth=0)


    def goToPayment(self):
        if len(self.invoiceItems) > 0:
            self.main.goToPayment()
        else:
            self.main.setWarning('You have to choose something first!')

    def showInvoiceInfo(self):
        self.invoiceTotalFrame.pack_forget()
        self.goToPaymentBtn.pack_forget()

    def showInvoiceInfoNoButton(self):
        self.invoiceTotalFrame.pack()
        self.goToPaymentBtn.pack_forget()
        if float(self.discount) != 0.:
            self.discountLabel.config(text=f'With {self.discount}% discount')
            self.discountLabel.pack(side='right', padx=20, pady=5)

    def showAll(self):
        self.invoiceTotalFrame.pack(fill='x', padx=(15, 0), pady=10, side='left')
        self.goToPaymentBtn.pack(padx=5, pady=10, side='right')

    def on_mousewheel(self, event):
        try:
            self.invoiceCanvas.yview_scroll(-1 * int(event.delta / 120), "units")
        except:
            pass
