#public member
#class Employee:
 #   def __init__(self, name):
 #       self.name = name #public member
 #   def describe_name(self): #public method
  #      print(self.name)
#emp = Employee("Musamali")
#emp.describe_name()
#print(emp.name)

#private members
class Employee:
    def __init__(self, name, salary):
      self.name = name  # public attribute, can be accessed directly
      self.__salary = salary  #private attribute, cannot be accessed directly.
    def show_salary(self):
        print("Salary",self.__salary)

emp = Employee("Mukasa Micheal", 300000)
print(emp.name) #Prints "Mukasa" because name is public.
emp.show_salary()
#print(emp.__salary)  # Raises an error because __salary is private and hidden.

#Example demostrating prrocted and private method
class BankAccount:
    def __init__(self):
        self.balance = 1000

    def _show_balance(self):
        print(f"Balance: UGX{self.balance}")  # Protected method

    def __update_balance(self, amount):
        self.balance += amount             # Private method

    def deposit(self, amount):
        if amount > 0:
            self.__update_balance(amount)  # Accessing private method internally
            self._show_balance()           # Accessing protected method
        else:
            print("Invalid deposit amount!")
            
account = BankAccount()
account._show_balance()      # Works, but should be treated as internal
# account.__update_balance(500)  # Error: private method
account.deposit(500)         # Uses both methods internally