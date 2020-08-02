import tkinter as tk
from tkinter import *
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt

from moneymanager import MoneyManager

global win
win = tk.Tk()

global number
number = 0

# Set window size here to '540 x 640'
win.geometry("540x640")

# Set the window title to 'FedUni Money Manager'
win.title("FedUni Money Manager")

# The user number and associated variable
user_number_var = tk.StringVar()

# This is set as a default for ease of testing
user_number_var.set('123456')
user_number_entry = tk.Entry(win, textvariable=user_number_var)
user_number_entry.focus_set()

# The pin number entry and associated variables
pin_number_var = tk.StringVar()
# This is set as a default for ease of testing
pin_number_var.set('7890')

# Modify the following to display a series of * rather than the pin ie **** not 1234
user_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var)

# set the user file by default to an empty string
user_file = ''

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
# amount_var = tk.StringVar()
tkVar = StringVar(win)
amount_entry = tk.Entry(win)
entry_type = tk.Entry(win)

# The transaction text widget holds text of the transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The money manager object we will work with
user = MoneyManager()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry():
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    entry2.delete(0, END)
    global number
    number = 0


def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry.'''
    # Limit to 4 chars in length
    global number
    number = (number * 10) + event
    # Set the new user number on the user_number_var
    if number <= 9999:
        entry2.insert(END, event)


def log_in():
    '''Function to log in to the banking system using a known user number and PIN.'''
    global user
    global pin_number_var
    global user_file
    global user_num_entry

    # Create the filename from the entered account number with '.txt' on the end
    try:
        fo = open("accounts.txt", "r");
        fo.close()
    except:
        fo = open("accounts.txt", "w");
        fo.close()

    # Try to open the account file for reading
    try:

        # Open the account file for reading
        fo = open(str(user_number_var.get()) + '.txt', 'r')
        fo.close()

    except:
        #if you want to create new account then comment following 6 lines
        c = Tk()
        c.title('FedUni Money Manager')
        l = Label(c, text='Enter Valid User Number and PIN', font=("Helvetica", 16))
        l.pack()
        c.mainloop()
        return

        fo = open(str(user_number_var.get()) + '.txt', 'w')

        # First line is account number
        fo.write("Account Number : " + str(user_number_var.get()) + "\n");

        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
        fo.write("PIN Number : " + str(pin_number_var.get()) + "\n");

        # Read third and fourth lines (balance and interest rate)
        fo.write("Balance : $ " + str(1000.0) + "\n");
        fo.write("Interest Rate : $ " + str(0.00));
        fo.close();

        fo = open("accounts.txt", "a");
        fo.write("Account Number : " + str(user_number_var.get()) + "\n");
        fo.write("PIN Number : " + str(pin_number_var.get()) + "\n");
        fo.close();
    try:
        username = str(user_number_var.get())
        username = username.strip()
        username = username.replace(" ", "")
        password = str(pin_number_var.get())
        password = password.strip()
        password = password.replace(" ", "")
        if username == '' or password == '':
            c = Tk()
            c.title('FedUni Money Manager')
            l = Label(c, text='Enter User Number and PIN', font=("Helvetica", 16))
            l.pack()
            c.mainloop()
            return
        try:
            u = float(username)/1
            p = float(password)/1
            flagu = 0
            flagp = 0

            read = 'x'

            # Section to read account transactions from file - start an infinite 'do-while' loop here
            fo = open("accounts.txt", "rb");
            while read:

                # Attempt to read a line from the account file, break if we've hit the end of the file. If we
                # read a line then it's the transaction type, so read the next line which will be the transaction amount.
                # and then create a tuple from both lines and add it to the account's transaction_list

                fo.seek(17, 1);
                read = fo.readline();
                read = str(read)
                read = read.replace("b", "")
                read = read.replace("r", "")
                read = read.replace("n", "")
                read = read.replace("\\", "")
                read = read.replace("'", "")
                if username == read:
                    flagu = 1
                    fo.seek(13, 1);
                    read = fo.readline();
                    read = str(read)
                    read = read.replace("b", "")
                    read = read.replace("r", "")
                    read = read.replace("n", "")
                    read = read.replace("\\", "")
                    read = read.replace("'", "")
                    if password == read:
                        flagp = 1
                        fo.close();
                        break
                    else:
                        c = Tk()
                        c.title('FedUni Money Manager')
                        l = Label(c, text='Enter correct PIN', font=("Helvetica", 16))
                        l.pack()
                        c.mainloop()
                        break
                else:
                    read = fo.readline();

            # Close the file now we're finished with it
            fo.close();
            if flagp == 0 and flagu == 0:
                c = Tk()
                c.title('FedUni Money Manager')
                l = Label(c, text='Enter Valid User Number', font=("Helvetica", 16))
                l.pack()
                c.mainloop()
        except:
            c = Tk()
            c.title('FedUni Money Manager')
            l = Label(c, text='Enter Valid Data', font=("Helvetica", 16))
            l.pack()
            c.mainloop()

    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except:

        # Show error messagebox and & reset BankAccount object to default...
        errormsg = Tk()
        errormsglabel = Label(errormsg, padx=70, pady=10, text='Something Went Wrong',font=("Helvetica", 20)).grid()

        #  ...also clear PIN entry and change focus to account number entry
        entry2.delete(0, END)
        entry1.focus()

    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    else:
        win.destroy()
        create_user_screen()


# ---------- Button Handlers for User Screen ----------

def save_and_log_out():

    '''Function  to overwrite the user file with the current state of
       the user object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global user, win, user_number_var, pin_number_var
    global entry1

    # Save the account with any new transactions
    win.destroy()
    win = Tk()

    # Reset the bank acount object
    user_number_var.set("")

    # Reset the account number and pin to blank
    pin_number_var.set("")

    # Remove all widgets and display the login screen again
    create_login_screen()
    entry1.focus()

    # Set window size here to '540 x 640'
    win.geometry("540x640")

    # Set the window title to 'FedUni Money Manager'
    win.title("FedUni Money Manager")

def perform_deposit():

    '''Function to add a deposit for the amount in the amount entry to the
       user's transaction list.'''
    global user
    global amount_entry
    global balance_label
    global balance_var

    try:
        bal = balance_var.get()
        bal = float(bal)
    except:
        c = Tk()
        c.title('FedUni Money Manager')
        l = Label(c, text='Enter Valid Data', font=("Helvetica", 16))
        l.pack()
        c.mainloop()
        return

    # Try to increase the account balance and append the deposit to the account file
    try:
    
        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        balance = balance_var.get()
        balance = balance.strip()
        balance = balance.replace(" ", "")
        file = str(user_number_var.get())
        MoneyManager.deposit_funds(file, balance)
        fo = open(file + ".txt", "rb")
        fo.readline()
        fo.readline()
        fo.seek(12, 1);
        bal = fo.readline();
        bal = str(bal)
        bal = bal.replace("b", "")
        bal = bal.replace("r", "")
        bal = bal.replace("n", "")
        bal = bal.replace("\\", "")
        bal = bal.replace("'", "")
        bal = float(bal)
        fo.close()

        # Deposit funds
        bal = float(bal) + float(balance)

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        MoneyManager.get_transaction_string(file, bal)

        # Change the balance label to reflect the new balance
        global y, variable
        y.set("Balance : $ " + str(bal))
        v = "Deposit "
        MoneyManager.save_to_file(file, v, balance)
        fo = open(file + ".txt", "r")
        fo.readline().replace("\n", "")
        fo.readline().replace("\n", "")
        fo.readline().replace("\n", "")
        fo.readline().replace("\n", "")
        x = fo.readline()
        transaction_list = x
        while x:
            x = fo.readline()
            transaction_list = transaction_list + x
        fo.close()
        Textbox.delete(1.0, END)
        Textbox.insert(END, transaction_list)

        # Clear the amount entry
        global balance_entry
        balance_entry.delete(0, END)

        # Update the interest graph with our new balance
        plot_spending_graph()

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except:
        c = Tk()
        c.title('FedUni Money Manager')
        l = Label(c, text='Something Went Wrong', font=("Helvetica", 16))
        l.pack()
        c.mainloop()

def perform_transaction():

    '''Function to add the entry the amount in the amount entry from the user balance and add an entry to the transaction list.'''
    global user
    global amount_entry
    global balance_label
    global balance_var
    global entry_type

    # Try to decrease the account balance and append the deposit to the account file
    try:

        # Get the cash amount to use. Note: We check legality inside account's withdraw_funds method
        balance = balance_var.get()
        balance = balance.strip()
        balance = balance.replace(" ", "")
        file = str(user_number_var.get())
        MoneyManager.add_entry(file, balance)
        fo = open(file + ".txt", "rb")
        fo.readline()
        fo.readline()
        fo.seek(12, 1);
        bal = fo.readline();
        bal = str(bal)
        bal = bal.replace("b", "")
        bal = bal.replace("r", "")
        bal = bal.replace("n", "")
        bal = bal.replace("\\", "")
        bal = bal.replace("'", "")
        bal = float(bal)
        fo.close()

        # Get the type of entry that will be added ie rent etc
        global variable
        v = variable.get()

        if float(balance) > float(bal):
            c = Tk()
            c.title('FedUni Money Manager')
            l = Label(c, text='No Enough Amount in Account', font=("Helvetica", 16))
            l.pack()
            c.mainloop()
            return


        # Withdraw funds from the balance
        bal = float(bal) - float(balance)

        # Update the transaction widget with the new transaction by calling user.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        MoneyManager.get_transaction_string(file, bal)

        # Change the balance label to reflect the new balance
        global y
        y.set("Balance : $ " + str(bal))
        MoneyManager.save_to_file(file, v, balance)
        fo = open(file + ".txt", "r")
        fo.readline().replace("\n", "")
        fo.readline().replace("\n", "")
        fo.readline().replace("\n", "")
        fo.readline().replace("\n", "")
        x = fo.readline()
        transaction_list = x
        while x:
            x = fo.readline()
            transaction_list = transaction_list + x
        fo.close()
        Textbox.delete(1.0, END)
        Textbox.insert(END, transaction_list)

        # Update the graph
        plot_spending_graph()

        # Clear the amount entry
        global balance_entry
        balance_entry.delete(0, END)

    # Catch and display any returned exception as a messagebox 'showerror'
    except:
        c = Tk()
        c.title('FedUni Money Manager')
        l = Label(c, text='Something Went Wrong', font=("Helvetica", 16))
        l.pack()
        c.mainloop()


def remove_all_widgets():

    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()


def read_line_from_user_file():

    '''Function to read a line from the users file but not the last newline character.
       Note: The user_file must be open to read from for this function to succeed.'''
    global user_file
    return user_file.readline()[0:-1]


def plot_spending_graph():

    '''Function to plot the user spending here.'''
    # YOUR CODE to generate the x and y lists here which will be plotted
    f = Figure(figsize=(5,2), dpi=100)
    z = f.add_subplot(111)
    fo = open(str(user_number_var.get()) + ".txt", "r")
    fo.readline().replace("\n","")
    fo.readline().replace("\n","")
    fo.readline().replace("\n","")
    fo.readline().replace("\n","")
    x = fo.readline().replace("\n","")
    count = 1
    l1 = [1]
    l2 = [1000]
    while x:
        count = count + 1
        l1.append(count)
        if x =='Deposit ':
            x = fo.readline().replace("\n","")
            x = x.replace(".0","")
            x = x.replace(" ","")
            x = int(x)
            x = l2[-1] + x
            l2.append(x)
        else:
            x = fo.readline().replace("\n", "")
            x = x.replace(".0", "")
            x = x.replace(" ", "")
            x = int(x)
            x = l2[-1] - x
            l2.append(x)
        x = fo.readline().replace("\n", "")

    # Your code to display the graph on the screen here - do this last
    z.plot(l1, l2)
    canvas = FigureCanvasTkAgg(f, win)
    canvas.draw()
    canvas.get_tk_widget().grid(row=14,columnspan=3)


# ---------- UI Drawing Functions ----------

def create_login_screen():

    '''Function to create the login screen.'''
    global entry1, entry2, user_number_var, pin_number_var

    # ----- Row 0 -----
    # 'FedUni Money Manager' label here. Font size is 28.
    label1 = Label(win, padx=70, pady=10, text='FedUni Money Manager', font=("Helvetica", 28)).grid(row=0, columnspan=3)

    # ----- Row 1 -----
    # Acount Number / Pin label here
    label2 = Label(win, text='User Number / PIN', font=("Helvetica", 10)).grid(row=1, column=0)

    # Account number entry here
    user_number_var = StringVar()
    entry1 = Entry(win, textvariable=user_number_var, width=29)
    entry1.focus()
    entry1.grid(row=1, column=1)

    # Account pin entry here
    pin_number_var = StringVar()
    entry2 = Entry(win, textvariable=pin_number_var, show="*", width=29)
    entry2.grid(row=1, column=2)

    # ----- Row 2 -----
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button1 = Button(win, padx=83, pady=40, text='1', fg='black', command=lambda: handle_pin_button(1)).grid(row=2,
                                                                                                              column=0)
    button2 = Button(win, padx=83, pady=40, text='2', fg='black', command=lambda: handle_pin_button(2)).grid(row=2,
                                                                                                              column=1)
    button3 = Button(win, padx=83, pady=40, text='3', fg='black', command=lambda: handle_pin_button(3)).grid(row=2,
                                                                                                              column=2)

    # ----- Row 3 -----
    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button4 = Button(win, padx=83, pady=40, text='4', fg='black', command=lambda: handle_pin_button(4)).grid(row=3,
                                                                                                              column=0)
    button5 = Button(win, padx=83, pady=40, text='5', fg='black', command=lambda: handle_pin_button(5)).grid(row=3,
                                                                                                              column=1)
    button6 = Button(win, padx=83, pady=40, text='6', fg='black', command=lambda: handle_pin_button(6)).grid(row=3,
                                                                                                              column=2)

    # ----- Row 4 -----
    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button7 = Button(win, padx=83, pady=40, text='7', fg='black', command=lambda: handle_pin_button(7)).grid(row=4,
                                                                                                              column=0)
    button8 = Button(win, padx=83, pady=40, text='8', fg='black', command=lambda: handle_pin_button(8)).grid(row=4,
                                                                                                              column=1)
    button9 = Button(win, padx=83, pady=40, text='9', fg='black', command=lambda: handle_pin_button(9)).grid(row=4,
                                                                                                              column=2)

    # ----- Row 5 -----
    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    buttonclear = Button(win, padx=50, pady=40, text='Cancel / Clear', fg='black', bg='red',
                         command=clear_pin_entry).grid(row=5, column=0)

    # Button 0 here
    button0 = Button(win, padx=83, pady=40, text='0', fg='black', command=lambda: handle_pin_button(0)).grid(row=5,
                                                                                                              column=1)

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    buttonlogin = Button(win, padx=70, pady=40, text='Log In', fg='black', bg='green', command=log_in).grid(row=5,
                                                                                                            column=2)

    # ----- Set column & row weights -----
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=0)
    win.rowconfigure(3, weight=0)
    win.rowconfigure(4, weight=0)
    win.rowconfigure(5, weight=0)
    win.columnconfigure(0, weight=6)
    win.columnconfigure(1, weight=6)
    win.columnconfigure(2, weight=6)

def create_user_screen():
    '''Function to create the user screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global win
    global balance_var, balance_l, balance_entry

    win = tk.Tk()

    # Set window size here to '540 x 640'
    win.geometry("540x640")

    # Set the window title to 'FedUni Money Manager'
    win.title("FedUni Money Manager")

    # ----- Row 0 -----
    # FedUni Banking label here. Font size should be 24.
    label = Label(win, padx=70, pady=10, text='FedUni Money Manager', font=("Helvetica", 24)).grid(row=0, columnspan=3)

    # ----- Row 1 -----
    # Account number label here
    label_account_number = Label(win, text='User Number: ' + user_number_var.get(), font=("Helvetica", 10), width=18).grid(row=1,column=0)

    # Balance label here
    fo = open(user_number_var.get() + ".txt", "r")
    fo.readline()
    fo.readline()
    read = fo.readline()
    fo.close()
    global y
    y = StringVar()
    y.set(read)
    balance_l = Label(win, textvariable = str(y) , font=("Helvetica", 10), width=18).grid(row=1,column=1)

    # Log out button here
    label_logout = Button(win, padx=83, pady=40, text='Log Out', fg='black',command=save_and_log_out).grid(row=1,column=2)

    # ----- Row 2 -----
    # Amount label here
    label_amount = Label(win, text='Amount ($)', font=("Helvetica", 10)).grid(row=2,column=0)

    # Amount entry here
    balance_var = StringVar()
    balance_entry = Entry(win, textvariable=balance_var, width=22)
    balance_entry.grid(row=2,column=1)

    # Deposit button here
    label_deposit = Button(win, padx=83, pady=40, text='Deposit', fg='black', command=perform_deposit).grid(row=2,column=2)

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.

    # ----- Row 3 -----
    # Entry type label here
    label_entry_tyle = Label(win, text='Entry Type', font=("Helvetica", 10), width=16).grid(row=3,column=0)

    # Entry drop list here
    OPTIONS = ["Rent", 'Food', 'Bills', 'Entertainment']
    global variable
    variable = StringVar(win)
    variable.set(OPTIONS[0])
    w = OptionMenu(win, variable, *OPTIONS).grid(row=3, column=1)

    # Add entry button here
    add_entry = Button(win, padx=78, pady=40, text='Add Entry', fg='black', command=perform_transaction).grid(row=3,column=2)

    # ----- Row 4 -----
    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    global Textbox
    Textbox = tk.Text(win, height="4")
    fo = open(user_number_var.get() + ".txt", "r")
    fo.readline().replace("\n","")
    fo.readline().replace("\n","")
    fo.readline().replace("\n","")
    fo.readline().replace("\n","")
    x = fo.readline()
    rdline = x
    while x:
        x = fo.readline()
        rdline = rdline + x
    fo.close()
    Textbox.insert(END, rdline)
    Textbox.grid(column=0, row=4, columnspan=3, rowspan=1, sticky='W')

    scrollbar = Scrollbar()  # height= not permitted here!
    Textbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=Textbox.yview)
    scrollbar.grid(column=3, row=4, rowspan=7, sticky='W')

    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited
    # Now add the scrollbar and set it to change with the yview of the text widget

    # ----- Row 5 - Graph -----
    # Call plot_interest_graph() here to display the graph
    plot_spending_graph()

    # ----- Set column & row weights -----
    # Set column and row weights here - there are 6 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    win.rowconfigure(0, weight=0)
    win.rowconfigure(1, weight=0)
    win.rowconfigure(2, weight=0)
    win.rowconfigure(3, weight=0)
    win.rowconfigure(4, weight=0)
    win.rowconfigure(7, weight=0)
    win.columnconfigure(0, weight=6)
    win.columnconfigure(1, weight=6)
    win.columnconfigure(2, weight=6)

# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
win.mainloop()
