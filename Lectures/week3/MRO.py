class A:
    def x(self):
        print("A")
class B:
    def x(self):
        print("B")
class C:
    def x(self):
        print("C")
class D(B,C):
    pass

obj = D()
obj.x()
print(D.__mro__)

#implementing with super() method in mro
class A:
    def w(self):
        print("A")

class B(A):
    def w(self):
        print("B")
        super().w()  # Calls C's w() if it exists

class C(A):
    def w(self):
        print("C")
        super().w()  # Calls A's w()

class D(B, C):
    def w(self):
        print("D")
        super().w()  # Calls B's w()

obj = D()
obj.w()
