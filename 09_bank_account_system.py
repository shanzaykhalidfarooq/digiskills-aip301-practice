#Bank Account System
class Customer:
    def __init__(self, name, account):
        self.name = name
        self.account = account
    def display_info(self):
        print(f"Customer Name: {self.name}")
        print(f"Account Number: {self.account.account_number}")

class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: Rs. {amount}")
        else:
            print("Deposit amount must be positive.")
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew: Rs. {amount}")
        else:
            print("Insufficient funds or invalid withdrawal amount.")
    def display_balance(self):
        print(f"Current Balance: Rs. {self.balance}")

acc1 = Account("1234567890", 1000)
cust1 = Customer("Alice", acc1)
cust1.display_info()
cust1.account.display_balance()
cust1.account.deposit(500)
cust1.account.display_balance()
cust1.account.withdraw(200)
cust1.account.display_balance()