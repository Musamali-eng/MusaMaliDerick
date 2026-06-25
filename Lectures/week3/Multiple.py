#Multiple inheritance
class Class1:
    def w(self):
        print("Method from class1")

class Class2(Class1):
    def w(self):
        print("Method from class2")

class Class3(Class1):
    def w(self):
        print("Method from class3")
class Class4(Class2, Class3):
    pass
obj = Class4()
obj.w()

