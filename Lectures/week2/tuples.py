#creating a tuple
Books = ("Python", "Java", "C++", "JavaScript")
print(Books)
print(type(Books))

#Demonstrating Heterogenenous 

#how to  delete a tuple
Books = ("Python", "Java", "C++", "JavaScript")
Books = list(Books)
del Books[0]
print(Books)

#update a tuple
Books = ("Python", "Java", "C++", "JavaScript")
Books = list(Books)
Books[0] = "HTML"
print(Books)

#concatenate a tuple
Books1 = ("Python", "Java", "C++", "JavaScript")
Books2 = ("HTML", "CSS", "PHP")
Books3 = Books1 + Books2
print(Books3)