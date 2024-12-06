from tkinter import Tk, Frame, Label, LabelFrame, Radiobutton, Entry, NSEW, StringVar, Button, W, Toplevel
import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import threading
import pandas as pd
import datetime


class Payment:
    def __init__(self, window, main, coords, coords_expand=None, padx=None, pady=None, sticky=None):
        self.window = window
        self.main = main
        self.coords = coords
        self.coords_expand = coords_expand or (1, 1)
        self.padx = padx or 0
        self.pady = pady or 0
        self.sticky = sticky or None
        self.total = 0
        self.discount = ['None', 0]
        self.final_total = 0
        self.order = None

        self.frame = Frame(self.window, bg='#F9F5E7')
        self.frame.grid(
            row=self.coords[0], column=self.coords[1], padx=self.padx, pady=self.pady, rowspan=self.coords_expand[0],
            columnspan=self.coords_expand[1], sticky=self.sticky
        )

        self.leftFrame = Frame(self.frame, bg='#F9F5E7')
        self.leftFrame.pack(side='left', padx=(20, 30))
        self.rightFrame = Frame(self.frame, bg='#F9F5E7')
        self.rightFrame.pack(side='right', padx=(30, 20))
        self.rightFrame.columnconfigure(1, minsize=350)

        def limit_entry(event, element, limit):
            if len(element.get()) > limit:
                element.delete(limit, 'end')
        def validate_input_digit(text):
            if text.isdigit() or text == "" :
                return True
            else:
                return False
        def validate_input_letters( text):
            if text.replace(" ", "").isalpha() or text == "":
                return True
            else:
                return False
            
        def validate_input_nospace(text):
            if text.isalnum() or text=='':
                return True
            return False
            
        self.validate_func_letters = self.window.register(validate_input_letters)
        self.nameLableFrame = LabelFrame(self.leftFrame, text='Full Name', font=('Raavi', 13), relief='flat', bg='#F9F5E7')
        self.nameFrame = Frame(self.nameLableFrame, bg='white', padx=2, pady=2, borderwidth=1, relief='ridge')
        self.nameFrame.pack()
        self.nameEntry = Entry(self.nameFrame, font=('Arial', 12), relief='flat', width=25, validate="key", validatecommand=(self.validate_func_letters, "%P"))
        self.nameLableFrame.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.nameEntry.pack(padx=5, pady=2)
        self.nameWarning = Label(self.nameLableFrame, bg='#F9F5E7')
        self.nameWarning.pack(side='left')
        self.nameEntry.bind('<FocusIn>',  lambda event, x=(self.nameEntry, 'name'):self.on_entry_click(event, x[0], x[1]))
        self.nameEntry.bind('<KeyRelease>', lambda event, x=[self.nameEntry, 20]:limit_entry(event, x[0], x[1]))

        self.validate_func_digit = self.window.register(validate_input_digit)
        self.phonNumberLableFrame = LabelFrame(self.leftFrame, text='Phone Number', font=('Raavi', 13), relief='flat', bg='#F9F5E7')
        self.phonNumberFrame = Frame(self.phonNumberLableFrame, bg='white', padx=2, pady=2, borderwidth=1, relief='ridge')
        self.phonNumberFrame.pack()
        self.phonNumberEntry = Entry(self.phonNumberFrame, font=('Arial', 12), relief='flat', validate="key", validatecommand=(self.validate_func_digit, "%P"))
        self.phonNumberLableFrame.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.phonNumberEntry.pack(padx=5, pady=2)
        self.phonNumberWarning = Label(self.phonNumberLableFrame, bg='#F9F5E7')
        self.phonNumberWarning.pack(side='left')
        self.phonNumberEntry.bind('<FocusIn>',  lambda event, x=(self.phonNumberEntry, 'phone number'):self.on_entry_click(event, x[0], x[1]))
        self.phonNumberEntry.bind('<KeyRelease>', lambda event, x=[self.phonNumberEntry, 11]:limit_entry(event, x[0], x[1]))

        self.addressLableFrame = LabelFrame(self.leftFrame, text='Address', font=('Raavi', 13), relief='flat', bg='#F9F5E7')
        self.addressFrame = Frame(self.addressLableFrame, bg='white', padx=2, pady=2, borderwidth=1, relief='ridge')
        self.addressFrame.pack()
        self.addressEntry = Entry(self.addressFrame, font=('Arial', 12), relief='flat', width=40)
        self.addressLableFrame.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.addressEntry.pack(padx=5, pady=2)
        self.addressWarning = Label(self.addressLableFrame, bg='#F9F5E7')
        self.addressWarning.pack(side='left')
        self.addressEntry.bind('<FocusIn>',  lambda event, x=(self.addressEntry, 'address'):self.on_entry_click(event, x[0], x[1]))
        self.addressEntry.bind('<KeyRelease>', lambda event, x=[self.addressEntry, 70]:limit_entry(event, x[0], x[1]))

        self.paymentOptionLableFrame = LabelFrame(self.leftFrame, text='Payment Option', font=('Arial', 15), relief='flat', bg='#F9F5E7')
        self.paymentOptionLableFrame.grid(row=3, column=0, padx=5, pady=2, sticky='w')

        self.paymentVar = StringVar()
        self.paymentVar.set("Credit Card") 

        self.creditCardRadio = Radiobutton(
            self.paymentOptionLableFrame, text="Credit Card", variable=self.paymentVar, value="Credit Card",
            font=('Arial', 12), relief='flat', command=self.updateCreditCardEntryState, bg='#F9F5E7'
        )
        self.creditCardRadio.pack(anchor='w')

        self.atTheDoorRadio = Radiobutton(
            self.paymentOptionLableFrame, text="At The Door", variable=self.paymentVar, value="On The Door",
            font=('Arial', 12), relief='flat', command=self.updateCreditCardEntryState, bg='#F9F5E7'
        )
        self.atTheDoorRadio.pack(anchor='w')

        self.ccNumberLableFrame = LabelFrame(self.leftFrame, text='Credit Number', font=('Arial', 15), relief='flat', bg='#F9F5E7')
        self.ccNumberFrameEntries = []
        self.ccNumberEntries = []
        for i in range(4):
            secondFrame = Frame(self.ccNumberLableFrame, bg='white', padx=1, pady=1, borderwidth=1, relief='ridge')
            secondFrame.pack(side='left')
            entry = Entry(secondFrame, font=('Arial', 12), relief='flat', width=6, justify='center')
            entry.pack(side='left', padx=5, pady=2)
            entry.bind('<KeyRelease>', lambda event, x='<KeyRelease>': self.handleCreditCard(x, event))
            entry.bind('<BackSpace>', lambda event, x='<BackSpace>': self.handleCreditCard(x, event))
            entry.bind('<Left>', lambda event, x='<Left>': self.handleCreditCard(x, event))
            entry.bind('<Right>', lambda event, x='<Right>': self.handleCreditCard(x, event))
            self.ccNumberFrameEntries.append((entry, secondFrame))
            self.ccNumberEntries.append(entry)
            if len(self.ccNumberEntries) < 4:
                separator = Label(self.ccNumberLableFrame, text='-', padx=8, bg='#F9F5E7')
                separator.pack(side='left', padx=2, pady=10)
            entry.insert(0, 'xxxx') 
            entry.config(fg='gray')  
            entry.bind('<FocusIn>', lambda event, x=(entry, 'xxxx'):self.on_entry_click(event, x[0], x[1]))
            entry.bind('<FocusOut>', lambda event, x=(entry, 'xxxx'):self.on_focus_out(event, x[0], x[1]))

        self.ccNumberLableFrame.grid(row=4, column=0, padx=5, pady=10, sticky='w')
        self.ccLastValidityDateLableFrame = LabelFrame(self.leftFrame, text='Last Offline Validity Date', font=('Arial', 15),
                                                   relief='flat', bg='#F9F5E7')
        
        self.secondFrameMonth = Frame(self.ccLastValidityDateLableFrame, bg='white', padx=1, pady=1, borderwidth=1, relief='ridge')
        self.secondFrameMonth.pack(side='left', padx=10, pady=5)
        self.ccMonth = Entry(self.secondFrameMonth, font=('Arial', 12), relief='flat', width=6, justify='center')
        self.ccMonth.insert(0, 'Month') 
        self.ccMonth.config(fg='gray')  
        self.ccMonth.bind('<FocusIn>', lambda event, x=(self.ccMonth, 'Month'):self.on_entry_click(event, x[0], x[1]))
        self.ccMonth.bind('<FocusOut>', lambda event, x=(self.ccMonth, 'Month'):self.on_focus_out(event, x[0], x[1]))

        self.secondFrameYear = Frame(self.ccLastValidityDateLableFrame, bg='white', padx=1, pady=1, borderwidth=1, relief='ridge')
        self.secondFrameYear.pack(side='left', padx=10, pady=5)
        self.ccYear = Entry(self.secondFrameYear, font=('Arial', 12), relief='flat', width=6, justify='center')
        self.ccYear.insert(0, 'Year')
        self.ccYear.config(fg='gray')
        self.ccYear.bind('<FocusIn>', lambda event, x=(self.ccYear, 'Year'):self.on_entry_click(event, x[0], x[1]))
        self.ccYear.bind('<FocusOut>', lambda event, x=(self.ccYear, 'Year'):self.on_focus_out(event, x[0], x[1]))

        self.secondFrameCVC = Frame(self.ccLastValidityDateLableFrame, bg='white', padx=1, pady=1, borderwidth=1, relief='ridge')
        self.secondFrameCVC.pack(side='left', padx=10, pady=5)
        self.ccCVC = Entry(self.secondFrameCVC, font=('Arial', 12), relief='flat', width=6, justify='center')
        self.ccCVC.insert(0, 'CVC')
        self.ccCVC.config(fg='gray')
        self.ccCVC.bind('<FocusIn>', lambda event, x=(self.ccCVC, 'CVC'):self.on_entry_click(event, x[0], x[1]))
        self.ccCVC.bind('<FocusOut>', lambda event, x=(self.ccCVC, 'CVC'):self.on_focus_out(event, x[0], x[1]))

        self.ccLVDInfo = [(self.ccMonth, 'Month'), (self.ccYear, 'Year'), (self.ccCVC, 'CVC')]

        self.ccMonth.pack(side='left', padx=10, pady=10)
        self.ccYear.pack(side='left', padx=10, pady=10)
        self.ccCVC.pack(side='left', padx=10, pady=10)

        self.invoiceFrame = Frame(self.rightFrame, bg='#F9F5E7')
        self.invoiceFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        self.separator = Frame(self.rightFrame, height=2, relief='sunken', borderwidth=1, bg='black')
        self.separator.grid(row=1, column=0, sticky=NSEW, pady=5, columnspan=2)

        self.taxs = Label(self.rightFrame, text=f'Taxs:   0.00$', bg='#F9F5E7', font=('Arial', 11))
        self.taxs.grid(row=2, column=0, sticky=W, pady=5)
        self.discountamount = Label(self.rightFrame, text=f'Discount:   {self.discount[1]}%', bg='#F9F5E7', font=('Arial', 11))
        self.discountamount.grid(row=3, column=0, sticky=W, pady=5) 
        self.totalLabel = Label(self.rightFrame, text=f'Total:   {self.total}$', bg='#F9F5E7', font=('Arial', 11))
        self.totalLabel.grid(row=4, column=0, sticky=W, pady=5)

        validate_entry_input = self.window.register(validate_input_nospace)
        self.discountLabelFrame = Label(self.rightFrame, padx=3, pady=3, bg='white', relief='flat')
        self.discountEntry = Entry(self.discountLabelFrame, fg='gray', width=30, relief='flat', validate='key', validatecommand=(validate_entry_input, "%P"))
        self.discountEntry.insert(0, 'Discount')
        self.discountEntry.bind('<FocusIn>', lambda event, x=[self.discountEntry, 'Discount']: self.on_entry_click(event, x[0], x[1]))
        self.discountEntry.bind('<FocusOut>', lambda event, x=[self.discountEntry, 'Discount']: self.on_focus_out(event, x[0], x[1]))
        self.discountEntry.bind('<KeyRelease>', lambda event, x=[self.discountEntry, 12]: limit(event, x[0], x[1]))
        def limit(event, element, limit):
            if len(element.get()) > limit:
                self.on_focus_out(event, element=self.discountEntry, text='Discount')
        self.discountBtn = Button(self.rightFrame, text='Enter Disocunt', command=self.checkDiscount, padx=10, pady=5)
        self.discountMsg = Label(self.rightFrame, font=('Arial', 14), bg='#F9F5E7')
        self.discountLabelFrame.grid(row=2, column=1, padx=10, pady=5,sticky=W)
        self.discountEntry.pack(padx=3, pady=3)
        self.discountBtn.grid(row=3, column=1, padx=10, pady=5,sticky=W)
        self.discountMsg.grid(row=4, column=1, padx=10, pady=5,sticky=W)

        self.separator = Frame(self.rightFrame, height=2, relief='sunken', borderwidth=1, bg='black')
        self.separator.grid(row=5, column=0, sticky=NSEW, pady=5, columnspan=2)

        self.finalTotal = Label(self.rightFrame, text=f'Total:   {self.final_total}$', font=('Arial', 20, 'bold'), bg='#F9F5E7')
        self.finalTotal.grid(row=6, column=0, sticky=W, pady=5)

        self.separator = Frame(self.rightFrame, height=2, relief='sunken', borderwidth=1, bg='black')
        self.separator.grid(row=7, column=0, sticky=NSEW, pady=5, columnspan=2)

        self.goBackBtn = Button(self.rightFrame, text='Go Back To Home', padx=10, pady=10, font=('Arial', 16), command=self.window.destroy)
        self.goBackBtn.grid(row=8, column=0, sticky=W, pady=15, padx=(0, 30))
        
        self.payBtn = Button(self.rightFrame, text='Pay', padx=10, pady=10, font=('Arial', 16), command=self.pay)
        self.payBtn.grid(row=8, column=1, sticky='e', pady=15)

        self.ccLastValidityDateLableFrame.grid(row=5, column=0, padx=5, pady=10, sticky='w')

    def handleCreditCard(self, function, event):
        def handleCreditCardEntry(event):
            current_entry = event.widget
            current_entry_index = self.ccNumberEntries.index(current_entry)

            if len(current_entry.get()) == 4:
                if current_entry_index < 3:
                    next_entry = self.ccNumberEntries[current_entry_index + 1]
                    next_entry.focus_set()
                else:
                    current_entry.selection_range(4, 4) 
            elif len(current_entry.get()) > 4:
                current_entry.delete(4, 'end') 

        def handleBackspace(event):
            current_entry = event.widget
            current_entry_index = self.ccNumberEntries.index(current_entry)

            if len(current_entry.get()) == 0:
                if current_entry_index > 0:
                    previous_entry = self.ccNumberEntries[current_entry_index - 1]
                    previous_entry.focus_set()
                    previous_entry.delete(3, 'end') 

        def handleLeftKey(event):
            current_entry = event.widget
            current_entry_index = self.ccNumberEntries.index(current_entry)

            if current_entry_index > 0:
                previous_entry = self.ccNumberEntries[current_entry_index - 1]
                previous_entry.focus_set()

        def handleRightKey(event):
            current_entry = event.widget
            current_entry_index = self.ccNumberEntries.index(current_entry)

            if current_entry_index < 3:
                next_entry = self.ccNumberEntries[current_entry_index + 1]
                next_entry.focus_set()

        def handleEntryFocusIn(event):
            current_entry = event.widget
            current_entry_index = self.ccNumberEntries.index(current_entry)

            if current_entry_index > 0 and (len(self.ccNumberEntries[current_entry_index - 1].get()) < 4 or str(self.ccNumberEntries[current_entry_index - 1].get()) == 'xxxx'):
                if current_entry_index < 3:
                    if str(self.ccNumberEntries[(current_entry_index + 1)].get()) == 'xxxx':
                        previous_entry = self.ccNumberEntries[current_entry_index - 1]
                        previous_entry.focus_set()
                    else:
                        previous_entry = self.ccNumberEntries[current_entry_index + 1]
                        previous_entry.focus_set()
                else:
                    previous_entry = self.ccNumberEntries[current_entry_index - 1]
                    previous_entry.focus_set()
        functions = {
            '<KeyRelease>': handleCreditCardEntry,
            '<BackSpace>': handleBackspace,
            '<Left>': handleLeftKey,
            '<Right>': handleRightKey,
            '<FocusIn>': handleEntryFocusIn
        }
        function = functions[function]
        function(event)

    def on_entry_click(self, event, element, text):
        if element.get() == text:
            element.config(fg='black')
            element.delete(0, 'end')
        if text == 'xxxx':
            self.handleCreditCard("<FocusIn>" ,event)
        elif text == 'name':
            self.nameWarning.config(text='')
        elif text == 'phone number':
            self.phonNumberWarning.config(text='')
        elif text == 'address':
            self.addressWarning.config(text='')
        elif text == 'Discount':
            element.config(fg='black')
            element.delete(0, 'end')
            self.checkDiscount(event, 'entry')

    def on_focus_out(self, event, element, text):
        if element.get() == '':
            element.config(fg='gray')
            element.insert(0, text)
        elif text == 'Month' and element.get() != '':
            element.config(fg='black')
            if int(element.get()) < 13:
                txt = str(int(element.get()))
                element.delete(0, 'end')
                element.insert(0, txt)
            else:
                element.delete(0, 'end')
                self.on_focus_out(event, element, 'Month')
        elif text == 'Year' and element.get() != '':
            element.config(fg='black')
            if 22 <int(element.get()) < 50:
                txt = str(int(element.get()))
                element.delete(0, 'end')
                element.insert(0, txt)
            else:
                element.delete(0, 'end')
                self.on_focus_out(event, element, 'Year')
        elif text == 'CVC' and element.get() != '':
            element.config(fg='black')
            if 0 < int(element.get()) < 1000:
                txt = str(int(element.get()))[-3:]
                element.delete(0, 'end')
                element.insert(0, txt)
            else:
                element.delete(0, 'end')
                self.on_focus_out(event, element, 'CVC')
        elif text == 'Discount':
            if str(element.get()).strip() != '':
                if len(str(element.get())) > 12:
                    txt = str(element.get())[:12]
                    element.delete(0, 'end')
                    element.insert(0, txt)
            else:
                element.config(fg='gray')
                element.delete(0, 'end')
                element.insert(0, 'Discount')

    def updateCreditCardEntryState(self):
        if self.paymentVar.get() == "Credit Card":
            for entry, frame in self.ccNumberFrameEntries:
                entry.config(state='normal')
                entry.delete(0, 'end')
                entry.insert(0, 'xxxx')
                entry.config(fg='gray') 
                entry.bind('<FocusIn>', lambda event, x=(entry, 'xxxx'):self.on_entry_click(event, x[0], x[1]))
                entry.bind('<FocusOut>', lambda event, x=(entry, 'xxxx'):self.on_focus_out(event, x[0], x[1]))
                frame.config(bg='white')
                self.ccNumberLableFrame.config(fg='black')
                self.ccLastValidityDateLableFrame.config(fg='black')
            for entry, txt in self.ccLVDInfo:
                entry.config(state='normal')
                entry.delete(0, 'end')
                entry.insert(0, txt)
                entry.config(fg='gray') 
                entry.bind('<FocusIn>', lambda event, x=(entry, txt):self.on_entry_click(event, x[0], x[1]))
                entry.bind('<FocusOut>', lambda event, x=(entry, txt):self.on_focus_out(event, x[0], x[1]))
        else:
            for entry, frame in self.ccNumberFrameEntries:
                entry.delete(0, 'end')
                entry.config(state='disabled')
                frame.config(bg='#F0F0FF')
                self.ccNumberLableFrame.config(fg='#83838B')
                self.ccLastValidityDateLableFrame.config(fg='#83838B')
            for entry, txt in self.ccLVDInfo:
                entry.delete(0, 'end')
                entry.config(state='disabled')

    def updateTotal(self, new_total):
        self.total = new_total
        self.final_total = self.total
        self.totalLabel.config(text=f'Total:   {self.total}$')
        self.finalTotal.config(text=f'Total:   {self.final_total}$')

    def setOrder(self, info):
        txt = ''
        for i, item in enumerate(info):
            txt += (str(item[0])+ ';' + str(item[1]) + ';' + str(item[2]) + ';'+ str(item[3]) + ';'+ str(int(item[3])* int(item[2])) +'|')
        self.order = txt

    def checkDiscount(self, event = None, order_from = 'button'):
        discounts = pd.read_csv('Data\\Discounts.csv', index_col=0).iloc[:, :].values
        if order_from == 'button':
            if self.discountEntry.get() in discounts[:, 0]:
                index = discounts[:, 0].tolist().index(self.discountEntry.get())
                if discounts[index, 2] == 'Unused':
                    self.discount = discounts[index, :2].tolist()
                    self.final_total = self.total - (float(self.discount[1])*self.total)

                    self.discountamount.config(text=f'Discount:   {self.discount[1]}%')
                    self.finalTotal.config(text = f'Total:   {self.final_total}$')
                    self.discountMsg.config(text='Discount Code Has Been Added!', fg='green')
                    self.discountEntry.bind('<KeyRelease>', lambda x='entry': self.checkDiscount(order_from='entry'))
                else:
                    self.discountMsg.config(text='Discount Code Has Been Used Before', fg='red')
            else:
                    self.final_total = self.total
                    self.discountamount.config(text=f'Discount:   {self.discount[1]}%')
                    self.finalTotal.config(text=f'Total:   {self.final_total}$')
                    self.discountMsg.config(text='Discount Code Is Not Available', fg='red')
        elif order_from == 'entry':
            self.discount = ['None', 0]
            self.final_total = self.total

            self.discountamount.config(text=f'Discount:   {self.discount[1]}%')
            self.finalTotal.config(text=f'Total:   {self.final_total}$')
            self.discountMsg.config(text='')  

    def checkBoxs(self):
        def contaiensSpace(text):
            for i in text:
                if str(i).isspace():
                    return True
            return False
        
        reuslt = True
        if len(self.nameEntry.get()) == 0: 
            self.nameWarning.config(text='*You have to enter a name', fg='red')
            reuslt = False
        elif len(self.nameEntry.get()) < 6 or not contaiensSpace(str(self.nameEntry.get())):
            self.nameWarning.config(text='*Please enter a real name', fg='red')
            reuslt = False
        if len(self.phonNumberEntry.get()) == 0:
            self.phonNumberWarning.config(text='*You have to enter a Phone Number', fg='red')
            reuslt = False
        elif (len(self.phonNumberEntry.get()) > 15 and str(self.phonNumberEntry.get()[:2]) == '00') or (len(self.phonNumberEntry.get()) > 12 and str(self.phonNumberEntry.get()[:2]) != '00'):
            self.phonNumberEntry.config(text='*Please enter a real number')
            reuslt = False
        if len(self.addressEntry.get()) == 0:
            self.addressWarning.config(text='*You have to enter an address', fg='red')
            reuslt = False
        elif len(self.addressEntry.get()) < 12 or not contaiensSpace(str(self.addressEntry.get())):
            self.addressWarning.config(text='*Please enter a real address', fg='red')
            reuslt = False
        if self.paymentVar.get() != "Credit Card":
            if reuslt:
                return True
        if len(self.ccMonth.get()) == 0 or str(self.ccMonth.get()) == 'Month':
            self.ccMonth.config(fg='red')
            reuslt = False
        if len(self.ccYear.get()) == 0 or str(self.ccYear.get()) == 'Year':
            self.ccYear.config(fg='red')
            reuslt = False
        if len(self.ccCVC.get()) == 0 or str(self.ccCVC.get()) == 'CVC':
            self.ccCVC.config(fg='red')
            reuslt = False
        for entry in self.ccNumberEntries:
            if len(entry.get()) < 4 or str(entry.get()) == 'xxxx':
                entry.config(fg='red')
                reuslt = False
        if reuslt:   
            return True
        else:
            return False
    
    def pay(self):
        if self.checkBoxs():
            payment_window = Toplevel(self.window)
            payment_window.transient(self.window)
            payment_window.grab_set()

            ran = ''
            for num in range(6):
                ran += str(random.randint(0, 9))

            dtime = datetime.datetime.strftime(datetime.datetime.today(), '%Y/%m/%d %H:%M:%S')

            cc = '-'.join([entry.get() for entry in self.ccNumberEntries]) + ' M:' + str(self.ccMonth.get()) +' Y:' + str(self.ccYear.get()) +' CVC:' + str(self.ccCVC.get())
            
            if not payment_window.winfo_exists():
                return
            
            user_data = [int(ran), str(dtime), str(self.nameEntry.get()), str(self.phonNumberEntry.get()), str(self.addressEntry.get()), cc, self.order, self.total, 'In The Kitchen', f'{self.discount[0]}|{self.discount[1]}']
            df = pd.read_csv(r'Data\Orders.csv', index_col=0)
            df2 = pd.DataFrame(columns=df.columns)
            for i, j in enumerate(df2.columns):
                df2[str(j)] = [user_data[i]]

            def simulate_payment():
                def update_progress(value, status):
                    progress_bar["value"] = value
                    label_status.config(text=status)
                
                def show_confirmation():
                    if not payment_window.winfo_exists():
                        return
                    label_confirmation.config(text="Your order has been accepted!")
                    estimated_time = random.randint(15, 45)
                    label_delivery.config(text=f"Estimated delivery time: {estimated_time} minutes")
                    label_contact.config(text=f'Your Order ID is {ran}')
                    frame.pack()
                    progress_bar.pack_forget()

                def payment_process():
                    if self.paymentVar.get() == "Credit Card":
                        for i in range(1, 100):
                            if i < 33:
                                txt = "Checking your payment information..."
                                new_df = pd.concat([df, df2])
                            elif i < 66:
                                txt = "Accepting payment..."
                            elif i < 98:
                                txt = 'Last Seconds...'
                            else:
                                txt = 'Done!'
                                new_df.to_csv(r'Data\Orders.csv')
                            update_progress(i, txt)
                            time.sleep(random.randint(1, 5)/100)
                    else:
                        for i in range(1, 100):
                            if i < 33:
                                txt = "Checking your information..."
                                new_df = pd.concat([df, df2])
                            elif i < 98:
                                txt = 'Last Seconds...'
                            else:
                                txt = 'Done!'
                                new_df.to_csv(r'Data\Orders.csv')
                            update_progress(i, txt)
                            time.sleep(random.randint(1, 5)/100)

                    payment_window.after(0, show_confirmation)
                
                threading.Thread(target=payment_process).start()

            def on_closing():
                if threading.active_count() > 1:
                    print("Please wait until the payment process is completed.")
                else:
                    self.window.destroy()
                    payment_window.destroy()

            payment_window.title("Payment Status")
            payment_window.geometry("400x200")
            payment_window.protocol("WM_DELETE_WINDOW", on_closing)

            label_status = tk.Label(payment_window, text="Checking your payment information", font=("Arial", 12))
            label_status.pack(pady=10)

            progress_bar = ttk.Progressbar(payment_window, mode="determinate", length=300)
            progress_bar.pack(pady=10)


            frame = tk.LabelFrame(payment_window)

            label_confirmation = tk.Label(frame, text="", font=("Arial", 14))
            label_confirmation.pack(pady=10)

            label_delivery = tk.Label(frame, text="", font=("Arial", 14))
            label_delivery.pack()

            label_contact = tk.Label(frame, text="", font=("Arial", 14))
            label_contact.pack(pady=8)

            simulate_payment()

            if self.discount[0] != 'None':
                discounts = pd.read_csv('Data\\Discounts.csv', index_col=0)
                discounts.loc[discounts['Discount Code'] == self.discount[0], ['Discount State']] = 'Used'
                discounts.to_csv('Data\\Discounts.csv')
