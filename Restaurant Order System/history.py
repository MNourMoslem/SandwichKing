from tkinter import Label, Frame, LabelFrame, Tk, NSEW, Button, W, E
import pandas as pd


class History:

    def __init__(self, window, main, coords, coords_expand = (1, 1), padx = 0, pady = 0, sticky = None):
        self.window = window
        self.main = main
        self.coords = coords
        self.coords_expand = coords_expand or (1, 1)
        self.padx = padx or 0
        self.pady = pady or 0
        self.sticky = sticky or None

        self.data = pd.read_csv('Data\\Orders.csv', index_col=0)
        self.data_rows = []

        self.frame = Frame(self.window, bg='#F9F5E7')
        self.frame.grid(row=self.coords[0], column=self.coords[1], rowspan=self.coords_expand[0], columnspan=self.coords_expand[1], sticky=self.sticky, padx=self.padx, pady=self.pady)

        self.titleFrame = LabelFrame(self.frame, bg='#F9F5E7')
        self.titleFrame.pack(fill='x')
        self.sheedFrame = LabelFrame(self.frame, bg='white')
        self.sheedFrame.pack(fill='x')
        self.screen = LabelFrame(self.frame, bg='#F9F5E7')
        self.screen.pack(fill='x')

        self.idTitle = Label(self.titleFrame, text='Order id', font=('Arial', 16), width=15, justify='left', padx=10, bg='#F9F5E7')
        self.idTitle.pack(side='left', padx=10, pady=5)

        self.dtimeTitle = Label(self.titleFrame, text='Date and Time', font=('Arial', 16), width=20, justify='left', padx=10, bg='#F9F5E7')
        self.dtimeTitle.pack(side='left', padx=10, pady=5)

        self.presonalInfoTitle = Label(self.titleFrame, text='Customer Informations', font=('Arial', 16), width=20, justify='left', padx=10, bg='#F9F5E7')
        self.presonalInfoTitle.pack(side='left', padx=10, pady=5)

        self.orderInfoTitle = Label(self.titleFrame, text='Order Details', font=('Arial', 16), width=15, justify='left', padx=10, bg='#F9F5E7')
        self.orderInfoTitle.pack(side='left', padx=10, pady=5)

        self.name = Label(self.screen,text='Name: ', font=('Arial', 12), bg='#F9F5E7')
        self.phoneNumber = Label(self.screen,text='Photo Number: ', font=('Arial', 12), bg='#F9F5E7')
        self.address = Label(self.screen, text='Address', font=('Arial', 12), bg='#F9F5E7')

        self.clearHistoryBtn = Button(self.screen, text='Clear History', font=('Arial', 12), command=self.clearHistory)

        self.name.pack(side='left', padx=8)
        self.phoneNumber.pack(side='left', padx=8)
        self.address.pack(side='left', padx=8)
        self.clearHistoryBtn.pack(side='right', padx=15)
    
    def read_orders(self):
        if len(self.data) > 1:
            data = self.data.iloc[1:, 6].values
            orders = []
            for i in data:
                items = str(i).split('|')
                order = []
                for j in items[:-1]:
                    item = str(j).split(';')
                    order.append([item[0], item])
                orders.append(order)
            return orders
        else:
            return []
        
    def set_sheed(self):
        self.data_rows = []
        if len(self.data) > 1:
            data = self.data.iloc[1:, :].values[::-1]
            for i, j in enumerate(data):

                secondframe = Frame(self.sheedFrame, bg='white')

                id_label = Label(secondframe, text=str(j[0]), font=('Courier', 10), width=15, bg='white')
                dtime_label = Label(secondframe, text=str(j[1]), font=('Courier', 10), width=20, bg='white')
                user_info_btn = Button(secondframe, text='Your Info', font=('Courier', 10), command=lambda x = i: self.show_user_info(-x - 1), width=20)
                order_info_btn = Button(secondframe, text='Order Info', font=('Courier', 10), command=lambda x = i: self.show_order_info(-x - 1), width=15)

                id_label.pack(side='left', padx=53, pady=5)
                dtime_label.pack(side='left', padx=53, pady=5)
                user_info_btn.pack(side='left', padx=53, pady=5)
                order_info_btn.pack(side='left', padx=53, pady=5)
               
                separator = Frame(secondframe, height=1, bg='black', relief='solid')
                separator.pack(side='bottom', padx=20, pady=5)

                secondframe.pack()

                self.data_rows.append([i ,id_label, dtime_label, user_info_btn, order_info_btn])
        else:
            label = Label(self.sheedFrame, text="You Don't have any recent orders", font=('Courier', 20, 'bold'))
            label.pack(anchor='center')
    def show_user_info(self, index):
        data = self.data.iloc[index, :].values

        self.name.config(text=f'Name: {data[2]} ')
        self.phoneNumber.config(text=f'Phone Number: {data[3]} ')
        self.address.config(text=f'Address: {data[4]}')

    def show_order_info(self, index):
        data = self.read_orders()[index]
        discount = self.data.iloc[1:, -1].tolist()[index].split('|')[1]
        self.main.showNewInvoice(data, discount)

    def clearHistory(self):
        df = pd.read_csv('Data\\Orders.csv', index_col=0)
        new_df = pd.DataFrame(columns=df.columns)

        for i in new_df.columns:
            new_df[str(i)] = [0]

        new_df.to_csv('Data\\Orders.csv')
        self.window.destroy()