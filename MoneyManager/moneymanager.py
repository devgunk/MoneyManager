from tkinter import *

class MoneyManager():

    def __init__(self):
        '''Constructor to set username to '', pin_number to an empty string,
           balance to 0.0, and transaction_list to an empty list.'''


    def add_entry(file, balance):

        '''Function to add and entry an amount to the tool. Raises an
        exception if it receives a value for amount that cannot be cast to float. Raises an exception
        if the entry_type is not valid - i.e. not food, rent, bills, entertainment or other'''

        try:
            er = 1
            # Get the type of entry that will be added ie rent etc
            if balance != '':

                check = 0
                try:
                    balance = float(balance) / 1
                    check = 1
                except:
                    c = Tk()
                    c.title('FedUni Money Manager')
                    l = Label(c, text='Enter Valid Data', font=("Helvetica", 16))
                    l.pack()
                    c.mainloop()
                if check == 1:

                    # Withdraw funds from the balance
                    balance = float(balance)
                    file = str(file)
                    fo = open(file + ".txt", "rb")
                    fo.readline()
                    fo.readline()
                    fo.seek(12, 1);
                    bal = fo.readline();
                    fo.close()
                    bal = str(bal)
                    bal = bal.replace("b", "")
                    bal = bal.replace("r", "")
                    bal = bal.replace("n", "")
                    bal = bal.replace("\\", "")
                    bal = bal.replace("'", "")
                    bal = float(bal)
                    if balance <= bal:
                        bal = bal - balance
                    else:
                        return 0
                        c = Tk()
                        c.title('FedUni Money Manager')
                        l = Label(c, text='You Cannot Spend Such Amount', font=("Helvetica", 16))
                        l.pack()
                        c.mainloop()
        except:
            er = 0
        return er


    def deposit_funds(file, balance):

        '''Function to deposit an amount to the user balance. Raises an
           exception if it receives a value that cannot be cast to float. '''
        # Deposit funds
        try:
            er = 1
            if balance != '':

                check = 0
                try:
                    balance = float(balance) / 1
                    check = 1
                except:
                    c = Tk()
                    c.title('FedUni Money Manager')
                    l = Label(c, text='Enter Valid Data', font=("Helvetica", 16))
                    l.pack()
                    c.mainloop()
                if check == 1:
                    file = str(file)
                    balance = float(balance)
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
                    bal = bal + balance
                    fo.close()
        except:
            er = 0
        return er


    def get_transaction_string( file, bal):

        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or the entry type - food etc - on
           the first line, and then the amount deposited or entry amount on the next line.'''
        fo = open(file + ".txt", "r")
        read = fo.readline()
        read = read + fo.readline()
        read = read + "Balance : $ " + str(bal) + "\n"
        fo.readline()
        x = 'x'
        while x:
            x = fo.readline()
            read = read + x
        fo.close()
        fo = open(file + ".txt", "w")
        fo.write(read)
        fo.close()


    def save_to_file( file, v, balance):

        '''Function to overwrite the user text file with the current user
           details. user number, pin number, and balance (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        fo = open(file + ".txt", "a");
        fo.write("\n" + v + "\n" + str(balance));
        fo.close();
