class Car:
    def __init__(self, brand, model, price):
        self.brand = brand          
        self._model = model         
        self.__price = price        
    
    def display_info(self):
        print("Car Details:")
        print("Brand:", self.brand)
        print("Model:", self._model)
        print("Price: $", self.__price)

car1 = Car("Toyota", "Camry", 35000)
car1.display_info()
print("\Accessing Attributes")
print("Brand (public):", car1.brand)

print("Model (protected):", car1._model)
