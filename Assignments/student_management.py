"""
STUDENT RECORD MANAGEMENT SYSTEM
A menu-driven application for managing student records with CSV and JSON storage.
Author: [MUSA MALI DERICK]
Date: 2026
"""

import csv
import json
import os
import logging
from datetime import datetime
import re

class StudentNotFoundError(Exception):
    """Raised when a student is not found in the database"""
    pass

class InvalidStudentDataError(Exception):
    """Raised when student data is invalid"""
    pass

class DuplicateStudentError(Exception):
    """Raised when trying to add a student with existing registration number"""
    pass


def setup_logging():
    """Configure logging for the student management system"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='student_system.log',
        filemode='a'
    )
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    logging.info("="*60)
    logging.info("STUDENT MANAGEMENT SYSTEM STARTED")
    logging.info("="*60)


CSV_FILE = 'students.csv'
JSON_FILE = 'students_details.json'

def validate_registration_number(reg_no):
    """
    Validate registration number format
    Expected format: 24/U/3001/EVE or similar
    """
    pattern = r'^\d{2}/[A-Z]/\d{4}/[A-Z]{3}$'
    if not re.match(pattern, reg_no):
        raise InvalidStudentDataError(
            f"Invalid registration number format: {reg_no}. Expected format: XX/U/XXXX/XXX"
        )
    return True


def validate_name(name):
    """Validate student name"""
    if not name or len(name.strip()) < 2:
        raise InvalidStudentDataError("Name must be at least 2 characters long")
    if not all(c.isalpha() or c.isspace() or c in ".-'" for c in name):
        raise InvalidStudentDataError("Name contains invalid characters")
    return True


def validate_age(age):
    """Validate student age"""
    try:
        age_int = int(age)
        if age_int < 16 or age_int > 100:
            raise InvalidStudentDataError("Age must be between 16 and 100")
        return True
    except ValueError:
        raise InvalidStudentDataError("Age must be a number")


def validate_score(score):
    """Validate student score"""
    try:
        score_int = int(score)
        if score_int < 0 or score_int > 100:
            raise InvalidStudentDataError("Score must be between 0 and 100")
        return True
    except ValueError:
        raise InvalidStudentDataError("Score must be a number")


def validate_gender(gender):
    """Validate gender"""
    if gender.upper() not in ['M', 'F', 'OTHER']:
        raise InvalidStudentDataError("Gender must be M, F, or OTHER")
    return True


def validate_phone(phone):
    """Validate phone number"""
    if phone and not re.match(r'^[0-9+\-() ]{10,15}$', phone):
        raise InvalidStudentDataError("Invalid phone number format")
    return True


def validate_email(email):
    """Validate email address"""
    if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise InvalidStudentDataError("Invalid email format")
    return True

def initialize_files():
    """Create CSV and JSON files if they don't exist"""
    
    if not os.path.exists(CSV_FILE):
        try:
            with open(CSV_FILE, 'w', newline='') as file:
                fieldnames = ['RegistrationNo', 'Name', 'Gender', 'Age', 'Course', 'Score']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            logging.info(f"Created new CSV file: {CSV_FILE}")
        except Exception as e:
            logging.error(f"Error creating CSV file: {e}")
            raise

    if not os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'w') as file:
                json.dump({}, file, indent=4)
            logging.info(f"Created new JSON file: {JSON_FILE}")
        except Exception as e:
            logging.error(f"Error creating JSON file: {e}")
            raise


def read_students_from_csv():
    """
    Read all students from CSV file
    Returns: List of student dictionaries
    """
    students = []
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
        return students
    except FileNotFoundError:
        logging.warning("CSV file not found, returning empty list")
        return []
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise


def write_students_to_csv(students):
    """
    Write all students to CSV file
    Args: List of student dictionaries
    """
    try:
        with open(CSV_FILE, 'w', newline='') as file:
            fieldnames = ['RegistrationNo', 'Name', 'Gender', 'Age', 'Course', 'Score']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        logging.info(f"Successfully wrote {len(students)} students to CSV")
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")
        raise


def read_student_details_from_json():
    """
    Read student details from JSON file
    Returns: Dictionary with registration numbers as keys
    """
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning("JSON file not found, returning empty dict")
        return {}
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in file")
        return {}
    except Exception as e:
        logging.error(f"Error reading JSON file: {e}")
        raise


def write_student_details_to_json(details):
    """
    Write student details to JSON file
    Args: Dictionary with registration numbers as keys
    """
    try:
        with open(JSON_FILE, 'w') as file:
            json.dump(details, file, indent=4)
        logging.info("Student details successfully written to JSON")
    except Exception as e:
        logging.error(f"Error writing to JSON file: {e}")
        raise



def add_student():
    """
    Add a new student to the system
    Prompts user for all required information
    """
    logging.info("Adding new student...")
    
    try:
    
        print("\n" + "="*50)
        print("ADD NEW STUDENT")
        print("="*50)
        
    
        while True:
            reg_no = input("Enter Registration Number (e.g., 24/U/3001/EVE): ").strip().upper()
            try:
                validate_registration_number(reg_no)
                break
            except InvalidStudentDataError as e:
                print(f"Error: {e}")
                continue
        
        
        students = read_students_from_csv()
        if any(s['RegistrationNo'] == reg_no for s in students):
            raise DuplicateStudentError(f"Student with registration number {reg_no} already exists")
        
        
        while True:
            name = input("Enter Student Name: ").strip()
            try:
                validate_name(name)
                break
            except InvalidStudentDataError as e:
                print(f"Error: {e}")
                continue
        
    
        while True:
            gender = input("Enter Gender (M/F/OTHER): ").strip().upper()
            try:
                validate_gender(gender)
                break
            except InvalidStudentDataError as e:
                print(f"Error: {e}")
                continue
        
        
        while True:
            age = input("Enter Age: ").strip()
            try:
                validate_age(age)
                break
            except InvalidStudentDataError as e:
                print(f"Error: {e}")
                continue
        
        
        course = input("Enter Course: ").strip()
        if not course:
            course = "Not Specified"
        
    
        while True:
            score = input("Enter Score (0-100): ").strip()
            try:
                validate_score(score)
                break
            except InvalidStudentDataError as e:
                print(f"Error: {e}")
                continue
        
        
        print("\nAdditional Details")
        address = input("Enter Address (optional): ").strip()
        phone = input("Enter Phone Number (optional): ").strip()
        email = input("Enter Email (optional): ").strip()
        program = input("Enter Program (optional): ").strip()
        year_of_study = input("Enter Year of Study (optional): ").strip()
        
        
        if phone:
            try:
                validate_phone(phone)
            except InvalidStudentDataError as e:
                print(f"Warning: {e}")
        
        if email:
            try:
                validate_email(email)
            except InvalidStudentDataError as e:
                print(f"Warning: {e}")
        
        
        student = {
            'RegistrationNo': reg_no,
            'Name': name,
            'Gender': gender,
            'Age': age,
            'Course': course,
            'Score': score
        }
        
    
        details = {
            'address': address if address else "Not Provided",
            'phone': phone if phone else "Not Provided",
            'email': email if email else "Not Provided",
            'program': program if program else "Not Specified",
            'year_of_study': year_of_study if year_of_study else "Not Specified",
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        
        students.append(student)
        write_students_to_csv(students)
        
        all_details = read_student_details_from_json()
        all_details[reg_no] = details
        write_student_details_to_json(all_details)
        
        logging.info(f"Student {name} ({reg_no}) added successfully")
        print(f"\n✓ Student {name} added successfully!")
        print(f"  Registration Number: {reg_no}")
        
    except DuplicateStudentError as e:
        logging.warning(f"Duplicate student: {e}")
        print(f"\nError: {e}")
    except InvalidStudentDataError as e:
        logging.warning(f"Invalid data: {e}")
        print(f"\nError: {e}")
    except Exception as e:
        logging.error(f"Error adding student: {e}")
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()


def view_all_students():
    """
    Display all students in a formatted table
    """
    logging.info("Viewing all students")
    
    try:
        students = read_students_from_csv()
        
        if not students:
            print("\nNo students found in the database.")
            logging.info("No students found")
            print("\nPress Enter to continue...")
            input()
            return
        
        
        print("\n" + "="*90)
        print(f"{'Reg No':<15} {'Name':<25} {'Gender':<8} {'Age':<5} {'Course':<20} {'Score':<6}")
        print("="*90)
        
        for student in students:
            print(f"{student['RegistrationNo']:<15} "
                  f"{student['Name']:<25} "
                  f"{student['Gender']:<8} "
                  f"{student['Age']:<5} "
                  f"{student['Course']:<20} "
                  f"{student['Score']:<6}")
        
        print("="*90)
        print(f"Total Students: {len(students)}")
        
        logging.info(f"Displayed {len(students)} students")
        
    except Exception as e:
        logging.error(f"Error viewing students: {e}")
        print(f"\nError: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()


def search_student():
    """
    Search for a student by registration number
    Displays both CSV and JSON details if found
    """
    logging.info("Searching for student...")
    
    try:
        reg_no = input("\nEnter Registration Number to search: ").strip().upper()
        
        if not reg_no:
            raise InvalidStudentDataError("Registration number cannot be empty")
        
        
        students = read_students_from_csv()
        student = next((s for s in students if s['RegistrationNo'] == reg_no), None)
        
        if student is None:
            raise StudentNotFoundError(f"Student with registration number {reg_no} not found")
        
    
        all_details = read_student_details_from_json()
        details = all_details.get(reg_no, {})
        

        print("\n" + "="*60)
        print("STUDENT INFORMATION")
        print("="*60)
        print(f"Registration Number: {student['RegistrationNo']}")
        print(f"Name:               {student['Name']}")
        print(f"Gender:             {student['Gender']}")
        print(f"Age:                {student['Age']}")
        print(f"Course:             {student['Course']}")
        print(f"Score:              {student['Score']}")
        
        if details:
            print("\n--- Additional Details ---")
            print(f"Address:      {details.get('address', 'Not Provided')}")
            print(f"Phone:        {details.get('phone', 'Not Provided')}")
            print(f"Email:        {details.get('email', 'Not Provided')}")
            print(f"Program:      {details.get('program', 'Not Specified')}")
            print(f"Year of Study: {details.get('year_of_study', 'Not Specified')}")
            print(f"Date Added:   {details.get('date_added', 'Not Available')}")
        
        print("="*60)
        logging.info(f"Student {reg_no} found and displayed")
        
    except StudentNotFoundError as e:
        logging.warning(f"Student not found: {e}")
        print(f"\nError: {e}")
    except InvalidStudentDataError as e:
        logging.warning(f"Invalid input: {e}")
        print(f"\nError: {e}")
    except Exception as e:
        logging.error(f"Error searching for student: {e}")
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()


def update_student():
    """
    Update student information
    Allows updating both CSV and JSON data
    """
    logging.info("Updating student information...")
    
    try:
        reg_no = input("\nEnter Registration Number to update: ").strip().upper()
        
        if not reg_no:
            raise InvalidStudentDataError("Registration number cannot be empty")
        
        
        students = read_students_from_csv()
        student_index = next((i for i, s in enumerate(students) if s['RegistrationNo'] == reg_no), None)
        
        if student_index is None:
            raise StudentNotFoundError(f"Student with registration number {reg_no} not found")
        
        student = students[student_index]
        
    
        print("\nCurrent Information:")
        print("-"*50)
        print(f"Name:      {student['Name']}")
        print(f"Gender:    {student['Gender']}")
        print(f"Age:       {student['Age']}")
        print(f"Course:    {student['Course']}")
        print(f"Score:     {student['Score']}")
        print("-"*50)
        
        print("\nLeave blank to keep current value")
        
        
        name = input(f"New Name [{student['Name']}]: ").strip()
        if name:
            validate_name(name)
            student['Name'] = name
        
        gender = input(f"New Gender [{student['Gender']}]: ").strip().upper()
        if gender:
            validate_gender(gender)
            student['Gender'] = gender
        
        age = input(f"New Age [{student['Age']}]: ").strip()
        if age:
            validate_age(age)
            student['Age'] = age
        
        course = input(f"New Course [{student['Course']}]: ").strip()
        if course:
            student['Course'] = course
        
        score = input(f"New Score [{student['Score']}]: ").strip()
        if score:
            validate_score(score)
            student['Score'] = score
        
        
        students[student_index] = student
        write_students_to_csv(students)
        
        
        all_details = read_student_details_from_json()
        if reg_no in all_details:
            details = all_details[reg_no]
            
            print("\nAdditional Details (Optional)")
            print("Leave blank to keep current value")
            
            address = input(f"New Address [{details.get('address', 'Not Provided')}]: ").strip()
            if address:
                details['address'] = address
            
            phone = input(f"New Phone [{details.get('phone', 'Not Provided')}]: ").strip()
            if phone:
                validate_phone(phone)
                details['phone'] = phone
            
            email = input(f"New Email [{details.get('email', 'Not Provided')}]: ").strip()
            if email:
                validate_email(email)
                details['email'] = email
            
            program = input(f"New Program [{details.get('program', 'Not Specified')}]: ").strip()
            if program:
                details['program'] = program
            
            year_of_study = input(f"New Year of Study [{details.get('year_of_study', 'Not Specified')}]: ").strip()
            if year_of_study:
                details['year_of_study'] = year_of_study
            
            details['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_details[reg_no] = details
            write_student_details_to_json(all_details)
        
        logging.info(f"Student {reg_no} updated successfully")
        print(f"\n✓ Student {reg_no} updated successfully!")
        
    except StudentNotFoundError as e:
        logging.warning(f"Student not found: {e}")
        print(f"\nError: {e}")
    except InvalidStudentDataError as e:
        logging.warning(f"Invalid data: {e}")
        print(f"\nError: {e}")
    except Exception as e:
        logging.error(f"Error updating student: {e}")
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()


def delete_student():
    """
    Delete a student from the system
    Removes from both CSV and JSON
    """
    logging.info("Deleting student...")
    
    try:
        reg_no = input("\nEnter Registration Number to delete: ").strip().upper()
        
        if not reg_no:
            raise InvalidStudentDataError("Registration number cannot be empty")
        
        
        students = read_students_from_csv()
        student = next((s for s in students if s['RegistrationNo'] == reg_no), None)
        
        if student is None:
            raise StudentNotFoundError(f"Student with registration number {reg_no} not found")
        
        
        print(f"\nAre you sure you want to delete: {student['Name']} ({reg_no})?")
        confirm = input("Type 'YES' to confirm: ").strip().upper()
        
        if confirm != 'YES':
            print("\nDeletion cancelled.")
            logging.info(f"Deletion of {reg_no} cancelled by user")
            print("\nPress Enter to continue...")
            input()
            return
        
        
        students = [s for s in students if s['RegistrationNo'] != reg_no]
        write_students_to_csv(students)
        
    
        all_details = read_student_details_from_json()
        if reg_no in all_details:
            del all_details[reg_no]
            write_student_details_to_json(all_details)
        
        logging.info(f"Student {reg_no} deleted successfully")
        print(f"\nStudent {reg_no} deleted successfully!")
        
    except StudentNotFoundError as e:
        logging.warning(f"Student not found: {e}")
        print(f"\nError: {e}")
    except InvalidStudentDataError as e:
        logging.warning(f"Invalid input: {e}")
        print(f"\nError: {e}")
    except Exception as e:
        logging.error(f"Error deleting student: {e}")
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()


def view_statistics():
    """
    Display statistics about the student database
    """
    logging.info("Viewing statistics")
    
    try:
        students = read_students_from_csv()
        
        if not students:
            print("\nNo students in database to display statistics.")
            print("\nPress Enter to continue...")
            input()
            return
        
        
        total_students = len(students)
        scores = [int(s['Score']) for s in students]
        
        if scores:
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
        else:
            avg_score = max_score = min_score = 0
        
        
        gender_count = {}
        for s in students:
            gender = s['Gender']
            gender_count[gender] = gender_count.get(gender, 0) + 1
        
        
        course_count = {}
        for s in students:
            course = s['Course']
            course_count[course] = course_count.get(course, 0) + 1
    
    
        print("\n" + "="*60)
        print("STUDENT DATABASE STATISTICS")
        print("="*60)
        print(f"Total Students:        {total_students}")
        print(f"Average Score:         {avg_score:.2f}")
        print(f"Highest Score:         {max_score}")
        print(f"Lowest Score:          {min_score}")
        
        print("\n--- Gender Distribution ---")
        for gender, count in gender_count.items():
            percentage = (count / total_students) * 100
            print(f"{gender}: {count} ({percentage:.1f}%)")
        
        print("\nCourse Distribution")
        for course, count in sorted(course_count.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_students) * 100
            print(f"{course}: {count} ({percentage:.1f}%)")
        
        print("="*60)
        logging.info("Statistics displayed successfully")
        
    except Exception as e:
        logging.error(f"Error displaying statistics: {e}")
        print(f"\nError: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()


def view_logs():
    """
    Display recent system logs
    """
    print("\n" + "="*60)
    print("SYSTEM LOGS (Last 50 lines)")
    print("="*60)
    
    try:
        if not os.path.exists('student_system.log'):
            print("No log file found.")
            print("\nPress Enter to continue...")
            input()
            return
        
        with open('student_system.log', 'r') as file:
            lines = file.readlines()
            
            for line in lines[-50:]:
                print(line.rstrip())
        
        print("="*60)
        
    except Exception as e:
        print(f"Error reading log file: {e}")
    
    print("\nPress Enter to continue...")
    input()

def main_menu():
    """
    Display the main menu and handle user input
    """
    while True:
        print("\n" + "="*60)
        print("STUDENT RECORD MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search for Student")
        print("4. Update Student Details")
        print("5. Delete Student")
        print("6. View Statistics")
        print("7. View System Logs")
        print("8. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_student()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            view_statistics()
        elif choice == '7':
            view_logs()
        elif choice == '8':
            logging.info("="*60)
            logging.info("STUDENT MANAGEMENT SYSTEM CLOSED")
            logging.info("="*60)
            print("\nThank you for using the Student Record Management System!")
            print("Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 8.")
            logging.warning(f"Invalid menu choice: {choice}")


def main():
    """
    Main program entry point
    """
    try:
        # Setup logging
        setup_logging()
        
        # Initialize files
        initialize_files()
        
        # Run main menu
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        logging.info("Program interrupted by user")
    except Exception as e:
        print(f"\nA critical error occurred: {e}")
        logging.critical(f"Critical error: {e}")
    finally:
        logging.info("Program execution completed")


if __name__ == "__main__":
    main()