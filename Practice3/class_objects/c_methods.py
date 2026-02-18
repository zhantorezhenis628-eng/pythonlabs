class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def show_balance(self):
        print(f"{self.owner}'s balance: {self.balance}")

account = BankAccount("Alice", 100)
account.deposit(50)
account.show_balance()
