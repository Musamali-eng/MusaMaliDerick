class Animal:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def info(self):
        print("Animal name:", self.name)
        print("Breed:",self.breed)

#creat a child class
class Dog(Animal):
    def sound(self):
        print(self.name,"barks")
w = Dog("Buddy","German Shepard")
w.info()
w.sound()
 