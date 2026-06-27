import csv
#read csv file
#open csv file
with open("D:\Recess\MusaMaliDerick\Lectures\week3\students.csv","r") as file:
    reader = csv.reader(file)

#loop through each row
    for row in reader:
     print(row)

#Lab activity add your ['RegistrationNo', 'Name', 'Gender', 'Age', 'Course', 'Score'] 
# to the students.csv, using a dictionary csv writer
import csv

Student = {
    'RegistrationNo': '24/U/3001/EVE',
    'Name': 'Wandera Vicent',
    'Gender': 'M',
    'Age': '26',
    'Course': 'Computer Science',
    'Score': '89'
}


file_path = r"D:\Recess\MusaMaliDerick\Lectures\week3\students.csv"

# Write to CSV
with open(file_path, 'w', newline='') as file:
    fieldnames = ['RegistrationNo', 'Name', 'Gender', 'Age', 'Course', 'Score']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write header row
    writer.writeheader()
    
    # Write data row (just the single student)
    writer.writerow(Student)
    
    print('Student details added successfully!')

# Verify by reading the file
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    print('\nStudents CSV Content:')
    for row in reader:
        print(row)
#JSON FILE HANDLING
