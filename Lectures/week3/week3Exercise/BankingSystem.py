# Base class
class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited: ${amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawn: ${amount}")
        else:
            print("Insufficient funds!")

    def display_info(self):
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ${self.balance}")

class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance, interest_rate):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Savings Withdrawal: ${amount}")
        else:
            print("Cannot withdraw more than available balance in a savings account.")

    def display_info(self):
        super().display_info()
        print(f"Interest Rate: {self.interest_rate}%")

class CurrentAccount(BankAccount):
    def __init__(self, account_number, balance, overdraft_limit):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            print(f"Current Account Withdrawal: ${amount}")
        else:
            print("Overdraft limit exceeded!")

    def display_info(self):
        super().display_info()
        print(f"Overdraft Limit: ${self.overdraft_limit}")


def demonstrate():
    savings = SavingsAccount("SA001", 1000, 5)
    current = CurrentAccount("CA001", 1000, 500)

    accounts = [savings, current]

    for account in accounts:
        print("\nACCOUNT DETAILS")
        account.display_info()

        print("\nDepositing $200...")
        account.deposit(200)

        print("Withdrawing $1200...")
        account.withdraw(1200)

        print("\nUpdated Balance:", account.balance)


demonstrate()