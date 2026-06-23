#Defining a class
class Smartphone:
#Constructor
  def __init__(self,device, brand):
    self.device = device
    self.brand = brand

#method of the class
  def description(self):
    return f"{self.device} of {self.brand} Supports Andriod 14"

#method2 of the class
  def information(self):
    return f"{self.device} {self.brand} is of high quality, reliable, and affordable to many users."

#creating object of the class
phoneObj = Smartphone("Smartphone", "Sumsang")
print(phoneObj.description())
print(phoneObj.information())