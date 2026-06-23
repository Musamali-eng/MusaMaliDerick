class MobileMoney:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        # CONDITION 1: Check if amount is valid
        if amount > 0:
            self.balance += amount
            print(f"Deposited: ${amount}")
        else:
            print("Amount must be greater than 0!")
    
    def withdraw(self, amount):
        # CONDITION 1: Check if amount is valid
        if amount <= 0:
            print("Amount must be greater than 0!")
        # CONDITION 2: Check if sufficient balance
        elif amount > self.balance:
            print("Insufficient balance!")
        else:
            self.balance -= amount
            print(f"Withdrawn: ${amount}")
    
    def check_balance(self):
        # CONDITION: Display balance with status
        if self.balance >= 1000:
            print(f"Balance: ${self.balance} (Excellent)")
        elif self.balance >= 500:
            print(f"Balance: ${self.balance} (Good)")
        elif self.balance >= 100:
            print(f"Balance: ${self.balance} (Fair)")
        else:
            print(f"Balance: ${self.balance} (Low)")


# Test the application
print(" MOBILE MONEY\n")

# Create account
account = MobileMoney(1000)
account.check_balance()

print("\nDepositing")
account.deposit(500)

print("\n Withdrawing")
account.withdraw(200)

print("\nFinal Balance After Withdraw")
account.check_balance()

print("\nTesting Conditions")
account.withdraw(-50)     
account.withdraw(5000)     