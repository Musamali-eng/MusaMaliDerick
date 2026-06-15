#sets in python is the collection of unique data
#Cars = {"Suzuki", "Honda", "Subaru"
#}
#print(Cars)
#print(type(Cars))

#demostrate data uniquness in sets
#Name ={"Musa", "Derick", 2400726588}
#print(Name)
#print(type(Name))

#Data duplication in sets
Letters = {"A", "B", "C", "D", "A", "B"}
print(Letters)
print(type(Letters))

#Methods
#use Add method to add data to a set
Age = {20, 21, 22 ,23,"Derick"}
Student = {"Musa", "Derick", "Mark", "David"}
W = Age.union(Student)
print(W)
print(type(W))

#Demostrate intersection method
X = Age.intersection(Student)
print(X)