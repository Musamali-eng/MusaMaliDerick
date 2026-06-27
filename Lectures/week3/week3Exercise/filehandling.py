# File handling
# "with" automatically closes the file

#with open("Student.txt", "r") as file:
  #  data = file.read()
 #   print(data)

# Read line by line
#with open("Student.txt", "r") as file:
    # Read one line at a time
 #   for line in file:
 #       print(line.strip())

# Add (append) text to a file
with open("Student.txt", "a") as file:
    file.write("\nJohn")
    file.write("\nMary")

print("Data added successfully.")