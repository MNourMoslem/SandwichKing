from menu import Menu
from tkinter import Tk, Frame, Toplevel, Label, NSEW, Button, PhotoImage
from screen import Screen
from invoice import Invoice
from payment import Payment
from history import History

wn = Tk()

class Main(Screen):

    def __init__(self, window, title):
        self.window = window
        self.window.title(title)
        self.window.configure(bg='#FFD89C')
        self.window.iconphoto(True, PhotoImage(file='Data\\images\\restaurant.png'))
        self.width = 1150
        self.height = 700
        screen_window_w = self.window.winfo_screenwidth()
        screen_window_h = self.window.winfo_screenheight()
        x = (screen_window_w/2) - (self.width/2)
        y = (screen_window_h/2) - (self.height/2)
        self.window.geometry('%dx%d-%d-%d' % (self.width, self.height, x, y))
        self.window.minsize(self.width, self.height)

        self.frame = Frame(self.window, bg='#769179')
        self.main = Menu(self.frame, self, (0, 0), padx=5, pady=5, coords_expand=(3, 1), sticky='n')
        self.screen = Screen(self.frame, self, coords=(0, 1), coords_expand=(1, 2), pady=5)
        self.invoice = Invoice(self.frame, self, (1, 1), coords_expand=(1, 2), sticky=NSEW)
        
        self.frame.rowconfigure(0, minsize=300)
        self.frame.rowconfigure(1, minsize=325)
        self.frame.rowconfigure(2, minsize=65)
        self.frame.columnconfigure(1, minsize=500)
        self.frame.columnconfigure(2, minsize=650)
        self.warning_msg = Label(self.frame, text='. . .', bg='white', font=('Arial', 14), padx=10, pady=10, relief='ridge', justify='left', width=40)
        self.warning_msg.grid(row=2, column=1, sticky=NSEW, pady=10)

        self.frame.columnconfigure(2, minsize=50)

        self.orderHistoryBtn = Button(self.frame, text='Order History', font=('Raleway', 12),pady=2, command=self.showHistory, bg='#DDDDDD')
        self.orderHistoryBtn.grid(row=2, column=2, pady=5, padx=10)

        self.frame.pack(anchor='center', fill='y')

    def displayInfo(self, info):
        self.screen.showInfo(*info)

    def displayMain(self):
        self.screen.showMain()

    def setWarning(self, info):
        self.warning_msg.config(text=info)
    
    def goToPayment(self):
        self.payment_window = Toplevel(self.window)
        self.payment_window.transient(self.window)
        self.payment_window.grab_set()
        self.payment_window.title('Payment')
        self.payment = Payment(self.payment_window, self, (0, 0))
        self.paymentInvoice = Invoice(self.payment.invoiceFrame, self, (0, 0), coords_expand=None, sticky=None)

        self.paymentInvoice.invoiceItems = self.invoice.invoiceItems
        self.paymentInvoice.refreshInvoice()
        self.paymentInvoice.cost = self.invoice.cost
        self.paymentInvoice.showInvoiceInfo()
        self.payment.updateTotal(self.paymentInvoice.cost)
        self.payment.setOrder([i[1] for i in self.paymentInvoice.invoiceItems])

    def showHistory(self):
        history_window = Toplevel(self.window)
        history_window.transient(self.window)
        history_window.grab_set()
        history_window.title('History')

        history = History(history_window, self, (0, 0))
        history.set_sheed()

    def showNewInvoice(self, data, discount):
        invoice_window = Toplevel(self.window)
        invoice_window.transient(self.window)
        invoice_window.grab_set()
        invoice_window.title('Order Details')

        newInvoice = Invoice(invoice_window, self, (0, 0), coords_expand=None, sticky=None)
        newInvoice.invoiceItems = data
        newInvoice.discount = discount
        newInvoice.refreshInvoice()
        newInvoice.showInvoiceInfoNoButton()

    def addDishToInvoice(self, dish):
        self.invoice.addToInvoice(dish)
    
    def removeDishFromInvoice(self, dish):
        self.invoice.removeFromInvoice(dish)

    def run(self):
        self.window.mainloop()

program = Main(wn, 'Restaurant Order System')
program.run()
