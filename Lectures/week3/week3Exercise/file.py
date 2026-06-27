# STEP 1: Create the file
with open(r"C:\Users\DERRICK\Desktop\geek.txt", "w") as f:

    f.write("Hello, I am a geek!")

print("File created success fully!")

#Reading a file
with open(r"C:\Users\DERRICK\Desktop\geek.txt","r") as f:
    content = f.read()
    print(content)
#Multiple lines

# STEP 3: Write multiple lines
with open(r"C:\Users\DERRICK\Desktop\geek.txt", "w") as f:
    f.write("Hello, I am Musa Mali Derick !\n")
    f.write("I love Python\n")
    f.write("Am Learning data science and file handling!\n")

# Read it back
with open(r"C:\Users\DERRICK\Desktop\geek.txt", "r") as f:
    print(f.read())

#Read first line only
with open(r"C:\Users\DERRICK\Desktop\geek.txt","r") as f:
    line1 = f.read()
    print("First line:", line1)

    line2 = f.read()
    print("Second line:", line2)

#Read all lines
with open(r"C:\Users\DERRICK\Desktop\geek.txt", "r") as f:
    all_lines = f.readlines()
    print(all_lines)

#loop through line we use strip()
with open(r"C:\Users\DERRICK\Desktop\geek.txt","r") as f:
    for line in f:
        print("->", line.strip()) # strip() removes \n

#append used for adding new line
with open(r"C:\Users\DERRICK\Desktop\geek.txt","a") as f:
    f.write("\nThis is my new line added using append method")
    f.write("\nNo one can stop me from learning new things in programming")

with open(r"C:\Users\DERRICK\Desktop\geek.txt","r") as f:
    print(f.read())

