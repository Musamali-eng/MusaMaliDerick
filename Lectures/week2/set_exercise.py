#1.	Create a list with 5 items (names of people) and write a python program to output the 2nd item.
names = ["Mukisa","Musoke","Mulindwa","Masa","Mugera"]
print(names[1])

#2.	Write a python program to change the value of the first item to a new value
Fruits = ["orange","pinaple","mango","jackfruit"]
print("Display original lists of fruits:\n", Fruits)

print("Display the updated list of fruits:\n", Fruits)
Fruits[0] = "strawberry"

#3.	Write a python program to add a sixth item to the list
countries = ["Uganda","Kenya","Tanzania","Rwanda","Burundi"]
print("Display list of five countries in East Africa:\n",countries)
print(" East Africa has",len(countries),"countries\n")
# Add a sixth item using append()method
countries.append("Somalia")
print("Display list of countries found in East Africa:\n", countries)
print("East Africa has",len(countries),"countries\n")

# Create a list with 5 names
names = ["Alice", "Bob", "Charlie", "Diana", "Eva"]


print("Original list:", names)
print("Length of list:", len(names))

# Add "Bathel" as the 3rd item (index 2) using insert()
names.insert(2, "Bathel")


print("Updated list:", names)
print("Length of list:", len(names))