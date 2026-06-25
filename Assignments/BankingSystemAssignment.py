#Banking system transactuion
class Transaction:
    def process_transaction(self, amount):
        print(f"Processing transaction of UGX {amount}")

class Deposit(Transaction):

    def process_transaction(self, amount):
        print(f"Deposited UGX {amount}")

    def deposit(self, amount, bonus=0):
        total = amount + bonus
        print(f"Deposited UGX {amount} with bonus UGX {bonus}")
        print(f"Total credited: UGX {total}")

class Withdrawal(Transaction):

    def process_transaction(self, amount):
        print(f"Withdrawn UGX {amount}")

class Transfer(Transaction):

    def process_transaction(self, amount):
        print(f"Transferred UGX {amount}")

employee_deposit = Deposit()
employee_withdrawal = Withdrawal()
employee_transfer = Transfer()

print("Employee Banking Transactions")

employee_deposit.process_transaction(500000)
employee_deposit.deposit(500000)
employee_deposit.deposit(500000, 50000)

