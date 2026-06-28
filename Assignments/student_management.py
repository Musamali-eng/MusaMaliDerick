"""
STUDENT RECORD MANAGEMENT SYSTEM
A menu-driven application for managing student records with CSV and JSON storage.
Enhanced with: Export, Grade Calculation, Advanced Search, and Backup features
Author: Musa Mali Derick
Date: 2026
Course: Software Engineering
Version: 2.0
"""

import csv
import json
import os
import logging
from datetime import datetime
import re
import shutil
from collections import defaultdict


# SECTION 1: CUSTOM EXCEPTIONS


class StudentNotFoundError(Exception):
    """Raised when a student is not found in the database"""
    pass

class InvalidStudentDataError(Exception):
    """Raised when student data is invalid"""
    pass

class DuplicateStudentError(Exception):
    """Raised when trying to add a student with existing registration number"""
    pass

class BackupError(Exception):
    """Raised when backup operations fail"""
    pass

class ExportError(Exception):
    """Raised when export operations fail"""
    pass


# SECTION 2: COLOR CODES & UI HELPERS


class Colors:
    """Terminal color codes for better UI"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_success(msg):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg):
    """Print error message in red"""
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_info(msg):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_warning(msg):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def print_header(msg):
    """Print header in bold purple"""
    print(f"\n{Colors.PURPLE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{msg:^60}{Colors.RESET}")
    print(f"{Colors.PURPLE}{Colors.BOLD}{'='*60}{Colors.RESET}")

# SECTION 3: LOGGING SETUP

def setup_logging():
    """Configure logging for the student management system"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='student_system.log',
        filemode='a'
    )
    
    # Add console handler for real-time feedback
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    logging.info("="*60)
    logging.info("STUDENT MANAGEMENT SYSTEM STARTED")
    logging.info("="*60)

# SECTION 4: FILE PATHS

CSV_FILE = 'students.csv'
JSON_FILE = 'students_details.json'
BACKUP_DIR = 'backups'
EXPORT_DIR = 'exports'

# SECTION 5: VALIDATION FUNCTIONS

def validate_registration_number(reg_no):
    """Validate registration number format: XX/U/XXXX/XXX"""
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

def get_validated_input(prompt, validator, optional=False):
    """
    Get validated input from user with retry logic
    
    Args:
        prompt: Input prompt
        validator: Function that validates input
        optional: If True, empty input is allowed
    """
    while True:
        value = input(prompt).strip()
        if optional and not value:
            return value
        try:
            validator(value)
            return value
        except InvalidStudentDataError as e:
            print_error(str(e))
            continue

# SECTION 6: GRADE CALCULATION

def calculate_grade(score):
    """
    Calculate letter grade and status based on score
    
    Args:
        score: Integer score between 0-100
    
    Returns:
        Tuple of (grade, status, gpa_points)
    """
    try:
        score = int(score)
        if score >= 80:
            return ('A', 'Excellent', 4.0)
        elif score >= 75:
            return ('A-', 'Very Good', 3.7)
        elif score >= 70:
            return ('B+', 'Good', 3.3)
        elif score >= 65:
            return ('B', 'Above Average', 3.0)
        elif score >= 60:
            return ('B-', 'Average', 2.7)
        elif score >= 55:
            return ('C+', 'Satisfactory', 2.3)
        elif score >= 50:
            return ('C', 'Pass', 2.0)
        elif score >= 45:
            return ('D', 'Marginal Pass', 1.0)
        else:
            return ('F', 'Fail', 0.0)
    except ValueError:
        return ('N/A', 'Invalid Score', 0.0)

def get_grade_distribution(students):
    """Get grade distribution for all students"""
    distribution = defaultdict(int)
    for student in students:
        score = int(student['Score'])
        grade, _, _ = calculate_grade(score)
        distribution[grade] += 1
    return dict(distribution)

def display_grade_report():
    """Display comprehensive grade report for all students"""
    print_header("STUDENT GRADE REPORT")
    
    try:
        students = read_students_from_csv()
        
        if not students:
            print_warning("No students found in database.")
            print("\nPress Enter to continue...")
            input()
            return
        
        # Sort by score (highest first)
        sorted_students = sorted(students, key=lambda x: int(x['Score']), reverse=True)
        
        # Display grade table
        print(f"\n{Colors.BOLD}{'Name':<25} {'Score':<8} {'Grade':<6} {'Status':<20} {'GPA':<6}{Colors.RESET}")
        print("-"*80)
        
        total_gpa = 0
        for student in sorted_students:
            score = int(student['Score'])
            grade, status, gpa = calculate_grade(score)
            
            # Color code based on grade
            if grade == 'A' or grade == 'A-':
                color = Colors.GREEN
            elif grade in ['B+', 'B', 'B-']:
                color = Colors.BLUE
            elif grade in ['C+', 'C']:
                color = Colors.YELLOW
            elif grade == 'D':
                color = Colors.PURPLE
            else:
                color = Colors.RED
            
            print(f"{student['Name']:<25} {score:<8} {color}{grade:<6}{Colors.RESET} "
                  f"{status:<20} {gpa:<.2f}")
            total_gpa += gpa
        
        print("-"*80)
        avg_gpa = total_gpa / len(students) if students else 0
        
        # Display statistics
        print(f"\n{Colors.BOLD}Summary Statistics:{Colors.RESET}")
        print(f"Total Students: {len(students)}")
        print(f"Average GPA: {avg_gpa:.2f}")
        print(f"Highest Score: {max(int(s['Score']) for s in students)}")
        print(f"Lowest Score: {min(int(s['Score']) for s in students)}")
        
        # Display grade distribution
        distribution = get_grade_distribution(students)
        print(f"\n{Colors.BOLD}Grade Distribution:{Colors.RESET}")
        for grade in sorted(distribution.keys()):
            count = distribution[grade]
            percentage = (count / len(students)) * 100
            bar = '█' * int(percentage)
            print(f"  {grade}: {count:>3} students ({percentage:>5.1f}%) {bar}")
        
        logging.info("Grade report displayed successfully")
        
    except Exception as e:
        logging.error(f"Error displaying grade report: {e}")
        print_error(f"An error occurred: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

# SECTION 7: FILE OPERATIONS


def initialize_files():
    """Create CSV and JSON files if they don't exist"""
    
    # Create directories if they don't exist
    for directory in [BACKUP_DIR, EXPORT_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")
    
    # Create CSV file with headers
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
    
    # Create JSON file
    if not os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'w') as file:
                json.dump({}, file, indent=4)
            logging.info(f"Created new JSON file: {JSON_FILE}")
        except Exception as e:
            logging.error(f"Error creating JSON file: {e}")
            raise

def read_students_from_csv():
    """Read all students from CSV file"""
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
    """Write all students to CSV file"""
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
    """Read student details from JSON file"""
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
    """Write student details to JSON file"""
    try:
        with open(JSON_FILE, 'w') as file:
            json.dump(details, file, indent=4)
        logging.info("Student details successfully written to JSON")
    except Exception as e:
        logging.error(f"Error writing to JSON file: {e}")
        raise


# SECTION 8: EXPORT FUNCTIONALITY


def export_to_csv(students, filename=None):
    """Export students to CSV file"""
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{EXPORT_DIR}/students_export_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as file:
            fieldnames = ['RegistrationNo', 'Name', 'Gender', 'Age', 'Course', 'Score', 'Grade', 'Status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for student in students:
                score = int(student['Score'])
                grade, status, _ = calculate_grade(score)
                row = student.copy()
                row['Grade'] = grade
                row['Status'] = status
                writer.writerow(row)
        
        print_success(f"Exported {len(students)} students to: {filename}")
        logging.info(f"Exported students to CSV: {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"Export to CSV failed: {e}")
        raise ExportError(f"Failed to export to CSV: {e}")

def export_to_excel(students, filename=None):
    """Export students to Excel file (requires pandas and openpyxl)"""
    try:
        import pandas as pd
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{EXPORT_DIR}/students_export_{timestamp}.xlsx"
        
        # Prepare data with grades
        data = []
        for student in students:
            score = int(student['Score'])
            grade, status, gpa = calculate_grade(score)
            data.append({
                'Registration No': student['RegistrationNo'],
                'Name': student['Name'],
                'Gender': student['Gender'],
                'Age': int(student['Age']),
                'Course': student['Course'],
                'Score': score,
                'Grade': grade,
                'Status': status,
                'GPA': gpa
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel writer with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Students', index=False)
            
            # Add statistics sheet
            stats = {
                'Statistic': ['Total Students', 'Average Score', 'Highest Score', 'Lowest Score', 'Average GPA'],
                'Value': [
                    len(students),
                    df['Score'].mean(),
                    df['Score'].max(),
                    df['Score'].min(),
                    df['GPA'].mean()
                ]
            }
            stats_df = pd.DataFrame(stats)
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
        
        print_success(f"Exported {len(students)} students to: {filename}")
        logging.info(f"Exported students to Excel: {filename}")
        return filename
        
    except ImportError:
        print_warning("pandas or openpyxl not installed. Falling back to CSV export.")
        return export_to_csv(students)
    except Exception as e:
        logging.error(f"Export to Excel failed: {e}")
        raise ExportError(f"Failed to export to Excel: {e}")

def export_to_json(students, details, filename=None):
    """Export students and details to JSON file"""
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{EXPORT_DIR}/students_export_{timestamp}.json"
        
        export_data = {
            'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'total_students': len(students),
            'students': []
        }
        
        for student in students:
            reg_no = student['RegistrationNo']
            score = int(student['Score'])
            grade, status, gpa = calculate_grade(score)
            
            student_data = {
                'registration_number': reg_no,
                'name': student['Name'],
                'gender': student['Gender'],
                'age': int(student['Age']),
                'course': student['Course'],
                'score': score,
                'grade': grade,
                'status': status,
                'gpa': gpa,
                'details': details.get(reg_no, {})
            }
            export_data['students'].append(student_data)
        
        with open(filename, 'w') as file:
            json.dump(export_data, file, indent=4)
        
        print_success(f"Exported {len(students)} students to: {filename}")
        logging.info(f"Exported students to JSON: {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"Export to JSON failed: {e}")
        raise ExportError(f"Failed to export to JSON: {e}")

def generate_report(students, details, filename=None):
    """Generate a comprehensive text report"""
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{EXPORT_DIR}/report_{timestamp}.txt"
        
        with open(filename, 'w') as file:
            file.write("="*80 + "\n")
            file.write("STUDENT MANAGEMENT SYSTEM - COMPREHENSIVE REPORT\n")
            file.write("="*80 + "\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Total Students: {len(students)}\n")
            file.write("="*80 + "\n\n")
            
            if students:
                # Calculate statistics
                scores = [int(s['Score']) for s in students]
                avg_score = sum(scores) / len(scores)
                
                # Grade distribution
                distribution = get_grade_distribution(students)
                
                file.write("SUMMARY STATISTICS\n")
                file.write("-"*40 + "\n")
                file.write(f"Average Score: {avg_score:.2f}\n")
                file.write(f"Highest Score: {max(scores)}\n")
                file.write(f"Lowest Score: {min(scores)}\n")
                file.write("\nGrade Distribution:\n")
                for grade in sorted(distribution.keys()):
                    count = distribution[grade]
                    percentage = (count / len(students)) * 100
                    file.write(f"  {grade}: {count} ({percentage:.1f}%)\n")
                
                file.write("\n\nSTUDENT DETAILS\n")
                file.write("-"*40 + "\n")
                
                # Sort by name for report
                sorted_students = sorted(students, key=lambda x: x['Name'])
                
                for student in sorted_students:
                    score = int(student['Score'])
                    grade, status, gpa = calculate_grade(score)
                    reg_no = student['RegistrationNo']
                    
                    file.write(f"\nName: {student['Name']}\n")
                    file.write(f"Registration: {reg_no}\n")
                    file.write(f"Gender: {student['Gender']}\n")
                    file.write(f"Age: {student['Age']}\n")
                    file.write(f"Course: {student['Course']}\n")
                    file.write(f"Score: {score}\n")
                    file.write(f"Grade: {grade}\n")
                    file.write(f"Status: {status}\n")
                    file.write(f"GPA: {gpa:.2f}\n")
                    
                    # Add additional details if available
                    if reg_no in details:
                        detail = details[reg_no]
                        file.write("Additional Details:\n")
                        for key, value in detail.items():
                            file.write(f"  {key}: {value}\n")
                    file.write("-"*40 + "\n")
            
            file.write("\n" + "="*80 + "\n")
            file.write("END OF REPORT\n")
            file.write("="*80 + "\n")
        
        print_success(f"Report generated: {filename}")
        logging.info(f"Generated report: {filename}")
        return filename
        
    except Exception as e:
        logging.error(f"Report generation failed: {e}")
        raise ExportError(f"Failed to generate report: {e}")

def export_menu():
    """Display export options menu"""
    while True:
        print_header("EXPORT DATA")
        print("1. Export to CSV")
        print("2. Export to Excel")
        print("3. Export to JSON")
        print("4. Generate Text Report")
        print("5. Return to Main Menu")
        print("="*60)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '5':
            break
        
        students = read_students_from_csv()
        if not students:
            print_warning("No students to export.")
            continue
        
        try:
            if choice == '1':
                export_to_csv(students)
            elif choice == '2':
                export_to_excel(students)
            elif choice == '3':
                details = read_student_details_from_json()
                export_to_json(students, details)
            elif choice == '4':
                details = read_student_details_from_json()
                generate_report(students, details)
            else:
                print_error("Invalid choice. Please try again.")
                continue
            
            # Ask if user wants to open the file
            open_file = input("\nOpen exported file? (y/n): ").strip().lower()
            if open_file == 'y':
                # This will work on Windows, Mac, and Linux
                import subprocess
                import platform
                
                if platform.system() == 'Windows':
                    os.startfile(filename)
                elif platform.system() == 'Darwin':
                    subprocess.run(['open', filename])
                else: 
                    subprocess.run(['xdg-open', filename])
        
        except ExportError as e:
            print_error(str(e))
        except Exception as e:
            print_error(f"Unexpected error: {e}")
        
        print("\nPress Enter to continue...")
        input()

# SECTION 9: ADVANCED SEARCH


def search_by_registration(students):
    """Search students by registration number"""
    reg_no = input("Enter Registration Number (partial match allowed): ").strip().upper()
    if not reg_no:
        print_warning("Search cancelled.")
        return []
    
    results = [s for s in students if reg_no in s['RegistrationNo']]
    return results

def search_by_name(students):
    """Search students by name (partial match)"""
    name = input("Enter Name (partial match allowed): ").strip()
    if not name:
        print_warning("Search cancelled.")
        return []
    
    results = [s for s in students if name.lower() in s['Name'].lower()]
    return results

def search_by_course(students):
    """Search students by course (partial match)"""
    course = input("Enter Course (partial match allowed): ").strip()
    if not course:
        print_warning("Search cancelled.")
        return []
    
    results = [s for s in students if course.lower() in s['Course'].lower()]
    return results

def search_by_score_range(students):
    """Search students by score range"""
    try:
        min_score = input("Enter Minimum Score (0-100): ").strip()
        max_score = input("Enter Maximum Score (0-100): ").strip()
        
        if not min_score:
            min_score = '0'
        if not max_score:
            max_score = '100'
        
        min_score = int(min_score)
        max_score = int(max_score)
        
        if min_score < 0 or min_score > 100 or max_score < 0 or max_score > 100:
            print_error("Scores must be between 0 and 100")
            return []
        
        if min_score > max_score:
            min_score, max_score = max_score, min_score
            print_info("Swapped min and max values.")
        
        results = [s for s in students if min_score <= int(s['Score']) <= max_score]
        return results
        
    except ValueError:
        print_error("Please enter valid numbers.")
        return []

def search_by_grade(students):
    """Search students by grade"""
    valid_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F']
    print(f"Valid grades: {', '.join(valid_grades)}")
    
    grade = input("Enter Grade: ").strip().upper()
    if grade not in valid_grades:
        print_error(f"Invalid grade. Must be one of: {', '.join(valid_grades)}")
        return []
    
    results = []
    for student in students:
        score = int(student['Score'])
        student_grade, _, _ = calculate_grade(score)
        if student_grade == grade:
            results.append(student)
    
    return results

def search_by_gender(students):
    """Search students by gender"""
    print("Genders: M, F, OTHER")
    gender = input("Enter Gender: ").strip().upper()
    if gender not in ['M', 'F', 'OTHER']:
        print_error("Invalid gender. Must be M, F, or OTHER")
        return []
    
    results = [s for s in students if s['Gender'] == gender]
    return results

def search_by_age_range(students):
    """Search students by age range"""
    try:
        min_age = input("Enter Minimum Age: ").strip()
        max_age = input("Enter Maximum Age: ").strip()
        
        if not min_age:
            min_age = '0'
        if not max_age:
            max_age = '200'
        
        min_age = int(min_age)
        max_age = int(max_age)
        
        if min_age < 0 or max_age < 0:
            print_error("Age must be positive")
            return []
        
        if min_age > max_age:
            min_age, max_age = max_age, min_age
            print_info("Swapped min and max values.")
        
        results = [s for s in students if min_age <= int(s['Age']) <= max_age]
        return results
        
    except ValueError:
        print_error("Please enter valid numbers.")
        return []

def display_search_results(results):
    """Display search results in a formatted table"""
    if not results:
        print_warning("No students found matching your search criteria.")
        return
    
    print_header(f"SEARCH RESULTS ({len(results)} found)")
    
    print(f"{'Reg No':<15} {'Name':<25} {'Gender':<8} {'Age':<5} {'Course':<20} {'Score':<6} {'Grade':<6}")
    print("-"*90)
    
    for student in results:
        score = int(student['Score'])
        grade, _, _ = calculate_grade(score)
        print(f"{student['RegistrationNo']:<15} "
              f"{student['Name']:<25} "
              f"{student['Gender']:<8} "
              f"{student['Age']:<5} "
              f"{student['Course']:<20} "
              f"{student['Score']:<6} "
              f"{grade:<6}")
    
    print("-"*90)

def advanced_search_menu():
    """Display advanced search menu"""
    while True:
        print_header("ADVANCED SEARCH")
        print("1. Search by Registration Number")
        print("2. Search by Name")
        print("3. Search by Course")
        print("4. Search by Score Range")
        print("5. Search by Grade")
        print("6. Search by Gender")
        print("7. Search by Age Range")
        print("8. Return to Main Menu")
        print("="*60)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '8':
            break
        
        students = read_students_from_csv()
        
        if not students:
            print_warning("No students in database.")
            continue
        
        search_functions = {
            '1': search_by_registration,
            '2': search_by_name,
            '3': search_by_course,
            '4': search_by_score_range,
            '5': search_by_grade,
            '6': search_by_gender,
            '7': search_by_age_range
        }
        
        if choice in search_functions:
            results = search_functions[choice](students)
            display_search_results(results)
        else:
            print_error("Invalid choice. Please try again.")
        
        print("\nPress Enter to continue...")
        input()


# SECTION 10: BACKUP FUNCTIONALITY


def create_backup():
    """Create backup of all data files"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"{BACKUP_DIR}/backup_{timestamp}"
        
        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup CSV file
        if os.path.exists(CSV_FILE):
            shutil.copy2(CSV_FILE, f"{backup_dir}/{CSV_FILE}")
        
        # Backup JSON file
        if os.path.exists(JSON_FILE):
            shutil.copy2(JSON_FILE, f"{backup_dir}/{JSON_FILE}")
        
        # Backup log file
        if os.path.exists('student_system.log'):
            shutil.copy2('student_system.log', f"{backup_dir}/student_system.log")
        
        # Create backup manifest
        manifest = {
            'backup_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'files': os.listdir(backup_dir),
            'total_students': len(read_students_from_csv())
        }
        
        with open(f"{backup_dir}/manifest.json", 'w') as f:
            json.dump(manifest, f, indent=4)
        
        print_success(f"Backup created: {backup_dir}")
        logging.info(f"Backup created: {backup_dir}")
        return backup_dir
        
    except Exception as e:
        logging.error(f"Backup creation failed: {e}")
        raise BackupError(f"Failed to create backup: {e}")

def list_backups():
    """List all available backups"""
    try:
        if not os.path.exists(BACKUP_DIR):
            print_warning("No backups found.")
            return []
        
        backups = [d for d in os.listdir(BACKUP_DIR) 
                  if os.path.isdir(os.path.join(BACKUP_DIR, d)) and d.startswith('backup_')]
        
        if not backups:
            print_warning("No backups found.")
            return []
        
        print_header("AVAILABLE BACKUPS")
        print(f"{'#':<5} {'Backup Name':<25} {'Date':<20} {'Students':<10}")
        print("-"*65)
        
        backup_list = []
        for idx, backup in enumerate(sorted(backups, reverse=True), 1):
            backup_path = os.path.join(BACKUP_DIR, backup)
            manifest_path = os.path.join(backup_path, 'manifest.json')
            
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                date = manifest.get('backup_date', 'Unknown')
                students = manifest.get('total_students', 'Unknown')
            else:
                date = backup.replace('backup_', '').replace('_', '-')
                students = 'Unknown'
            
            print(f"{idx:<5} {backup:<25} {date:<20} {students:<10}")
            backup_list.append(backup)
        
        print("-"*65)
        return backup_list
        
    except Exception as e:
        logging.error(f"Error listing backups: {e}")
        print_error(f"Error listing backups: {e}")
        return []

def restore_backup(backup_name):
    """Restore data from a backup"""
    try:
        backup_path = os.path.join(BACKUP_DIR, backup_name)
        
        if not os.path.exists(backup_path):
            raise BackupError(f"Backup not found: {backup_name}")
        
        # Confirm restore
        print_warning("Restoring will overwrite current data!")
        confirm = input("Are you sure? Type 'YES' to confirm: ").strip().upper()
        
        if confirm != 'YES':
            print_info("Restore cancelled.")
            return
        
        # Restore CSV
        backup_csv = os.path.join(backup_path, CSV_FILE)
        if os.path.exists(backup_csv):
            shutil.copy2(backup_csv, CSV_FILE)
        
        # Restore JSON
        backup_json = os.path.join(backup_path, JSON_FILE)
        if os.path.exists(backup_json):
            shutil.copy2(backup_json, JSON_FILE)
        
        # Restore log (optional)
        backup_log = os.path.join(backup_path, 'student_system.log')
        if os.path.exists(backup_log):
            shutil.copy2(backup_log, 'student_system.log')
        
        print_success(f"Successfully restored from: {backup_name}")
        logging.info(f"Restored from backup: {backup_name}")
        
    except Exception as e:
        logging.error(f"Restore failed: {e}")
        raise BackupError(f"Failed to restore backup: {e}")

def backup_menu():
    """Display backup management menu"""
    while True:
        print_header("BACKUP MANAGEMENT")
        print("1. Create New Backup")
        print("2. List Available Backups")
        print("3. Restore from Backup")
        print("4. Return to Main Menu")
        print("="*60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '4':
            break
        elif choice == '1':
            try:
                create_backup()
            except BackupError as e:
                print_error(str(e))
        elif choice == '2':
            list_backups()
        elif choice == '3':
            backups = list_backups()
            if backups:
                try:
                    choice_num = input("\nEnter backup number to restore (or 0 to cancel): ").strip()
                    if choice_num == '0':
                        continue
                    
                    idx = int(choice_num) - 1
                    if 0 <= idx < len(backups):
                        restore_backup(backups[idx])
                    else:
                        print_error("Invalid backup number.")
                except ValueError:
                    print_error("Please enter a valid number.")
        else:
            print_error("Invalid choice. Please try again.")
        
        print("\nPress Enter to continue...")
        input()

# ============================================
# SECTION 11: MAIN STUDENT OPERATIONS
# ============================================

def add_student():
    """Add a new student to the system"""
    logging.info("Adding new student...")
    
    try:
        print_header("ADD NEW STUDENT")
        
        # Get registration number
        reg_no = get_validated_input(
            "Enter Registration Number (e.g., 24/U/3001/EVE): ",
            validate_registration_number
        )
        
        # Check for duplicate registration number
        students = read_students_from_csv()
        if any(s['RegistrationNo'] == reg_no for s in students):
            raise DuplicateStudentError(f"Student with registration number {reg_no} already exists")
        
        # Get student details
        name = get_validated_input("Enter Student Name: ", validate_name)
        gender = get_validated_input("Enter Gender (M/F/OTHER): ", validate_gender)
        age = get_validated_input("Enter Age: ", validate_age)
        
        course = input("Enter Course: ").strip()
        if not course:
            course = "Not Specified"
        
        score = get_validated_input("Enter Score (0-100): ", validate_score)
        
        # Get additional details
        print("\n--- Additional Details (Optional) ---")
        address = input("Enter Address: ").strip()
        phone = input("Enter Phone Number: ").strip()
        email = input("Enter Email: ").strip()
        program = input("Enter Program: ").strip()
        year_of_study = input("Enter Year of Study: ").strip()
        
        # Validate optional fields if provided
        if phone:
            try:
                validate_phone(phone)
            except InvalidStudentDataError as e:
                print_warning(str(e))
        
        if email:
            try:
                validate_email(email)
            except InvalidStudentDataError as e:
                print_warning(str(e))
        
        # Create student record
        student = {
            'RegistrationNo': reg_no,
            'Name': name,
            'Gender': gender,
            'Age': age,
            'Course': course,
            'Score': score
        }
        
        # Create additional details
        details = {
            'address': address if address else "Not Provided",
            'phone': phone if phone else "Not Provided",
            'email': email if email else "Not Provided",
            'program': program if program else "Not Specified",
            'year_of_study': year_of_study if year_of_study else "Not Specified",
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to CSV
        students.append(student)
        write_students_to_csv(students)
        
        # Save to JSON
        all_details = read_student_details_from_json()
        all_details[reg_no] = details
        write_student_details_to_json(all_details)
        
        print_success(f"Student {name} ({reg_no}) added successfully!")
        logging.info(f"Student {name} ({reg_no}) added successfully")
        
    except DuplicateStudentError as e:
        print_error(str(e))
        logging.warning(f"Duplicate student: {e}")
    except InvalidStudentDataError as e:
        print_error(str(e))
        logging.warning(f"Invalid data: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        logging.error(f"Error adding student: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

def view_all_students():
    """Display all students in a formatted table with grades"""
    logging.info("Viewing all students")
    
    try:
        students = read_students_from_csv()
        
        if not students:
            print_warning("No students found in the database.")
            print("\nPress Enter to continue...")
            input()
            return
        
        # Display students with grades
        print_header("ALL STUDENTS")
        print(f"{Colors.BOLD}{'Reg No':<15} {'Name':<25} {'Gender':<8} {'Age':<5} {'Course':<20} {'Score':<6} {'Grade':<6}{Colors.RESET}")
        print("="*90)
        
        for student in students:
            score = int(student['Score'])
            grade, status, _ = calculate_grade(score)
            
            # Color code based on grade
            if grade in ['A', 'A-']:
                color = Colors.GREEN
            elif grade in ['B+', 'B', 'B-']:
                color = Colors.BLUE
            elif grade in ['C+', 'C']:
                color = Colors.YELLOW
            elif grade == 'D':
                color = Colors.PURPLE
            else:
                color = Colors.RED
            
            print(f"{student['RegistrationNo']:<15} "
                  f"{student['Name']:<25} "
                  f"{student['Gender']:<8} "
                  f"{student['Age']:<5} "
                  f"{student['Course']:<20} "
                  f"{student['Score']:<6} "
                  f"{color}{grade:<6}{Colors.RESET}")
        
        print("="*90)
        print(f"{Colors.BOLD}Total Students: {len(students)}{Colors.RESET}")
        
        logging.info(f"Displayed {len(students)} students")
        
    except Exception as e:
        print_error(f"Error viewing students: {e}")
        logging.error(f"Error viewing students: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

def search_student():
    """Legacy search by registration number (kept for backward compatibility)"""
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
        
        score = int(student['Score'])
        grade, status, gpa = calculate_grade(score)
        
        print_header("STUDENT INFORMATION")
        print(f"Registration Number: {Colors.BOLD}{student['RegistrationNo']}{Colors.RESET}")
        print(f"Name:               {student['Name']}")
        print(f"Gender:             {student['Gender']}")
        print(f"Age:                {student['Age']}")
        print(f"Course:             {student['Course']}")
        print(f"Score:              {student['Score']}")
        print(f"Grade:              {grade}")
        print(f"Status:             {status}")
        print(f"GPA:                {gpa:.2f}")
        
        if details:
            print("\n--- Additional Details ---")
            for key, value in details.items():
                print(f"{key.replace('_', ' ').title():<20}: {value}")
        
        print("="*60)
        logging.info(f"Student {reg_no} found and displayed")
        
    except StudentNotFoundError as e:
        print_error(str(e))
        logging.warning(f"Student not found: {e}")
    except InvalidStudentDataError as e:
        print_error(str(e))
        logging.warning(f"Invalid input: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        logging.error(f"Error searching for student: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

def update_student():
    """Update student information"""
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
        
        print_header("UPDATE STUDENT")
        print("Current Information:")
        print("-"*50)
        print(f"Name:      {student['Name']}")
        print(f"Gender:    {student['Gender']}")
        print(f"Age:       {student['Age']}")
        print(f"Course:    {student['Course']}")
        print(f"Score:     {student['Score']}")
        print("-"*50)
        
        print("\nLeave blank to keep current value")
        
        # Update fields
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
        
        # Update CSV
        students[student_index] = student
        write_students_to_csv(students)
        
        # Update JSON details if provided
        all_details = read_student_details_from_json()
        if reg_no in all_details:
            details = all_details[reg_no]
            
            print("\n--- Additional Details (Optional) ---")
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
        
        print_success(f"Student {reg_no} updated successfully!")
        logging.info(f"Student {reg_no} updated successfully")
        
    except StudentNotFoundError as e:
        print_error(str(e))
        logging.warning(f"Student not found: {e}")
    except InvalidStudentDataError as e:
        print_error(str(e))
        logging.warning(f"Invalid data: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        logging.error(f"Error updating student: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

def delete_student():
    """Delete a student from the system"""
    logging.info("Deleting student...")
    
    try:
        reg_no = input("\nEnter Registration Number to delete: ").strip().upper()
        
        if not reg_no:
            raise InvalidStudentDataError("Registration number cannot be empty")
        
        students = read_students_from_csv()
        student = next((s for s in students if s['RegistrationNo'] == reg_no), None)
        
        if student is None:
            raise StudentNotFoundError(f"Student with registration number {reg_no} not found")
        
        print_warning(f"Are you sure you want to delete: {student['Name']} ({reg_no})?")
        confirm = input("Type 'YES' to confirm: ").strip().upper()
        
        if confirm != 'YES':
            print_info("Deletion cancelled.")
            logging.info(f"Deletion of {reg_no} cancelled by user")
            print("\nPress Enter to continue...")
            input()
            return
        
        # Remove from CSV
        students = [s for s in students if s['RegistrationNo'] != reg_no]
        write_students_to_csv(students)
        
        # Remove from JSON
        all_details = read_student_details_from_json()
        if reg_no in all_details:
            del all_details[reg_no]
            write_student_details_to_json(all_details)
        
        print_success(f"Student {reg_no} deleted successfully!")
        logging.info(f"Student {reg_no} deleted successfully")
        
    except StudentNotFoundError as e:
        print_error(str(e))
        logging.warning(f"Student not found: {e}")
    except InvalidStudentDataError as e:
        print_error(str(e))
        logging.warning(f"Invalid input: {e}")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        logging.error(f"Error deleting student: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

def view_statistics():
    """Display statistics about the student database"""
    logging.info("Viewing statistics")
    
    try:
        students = read_students_from_csv()
        
        if not students:
            print_warning("No students in database to display statistics.")
            print("\nPress Enter to continue...")
            input()
            return
        
        print_header("STUDENT DATABASE STATISTICS")
        
        # Calculate statistics
        total_students = len(students)
        scores = [int(s['Score']) for s in students]
        
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        # Gender distribution
        gender_count = {}
        for s in students:
            gender = s['Gender']
            gender_count[gender] = gender_count.get(gender, 0) + 1
        
        # Course distribution
        course_count = {}
        for s in students:
            course = s['Course']
            course_count[course] = course_count.get(course, 0) + 1
        
        # Grade distribution
        grade_dist = get_grade_distribution(students)
        
        print(f"{Colors.BOLD}General Statistics:{Colors.RESET}")
        print(f"Total Students:        {total_students}")
        print(f"Average Score:         {avg_score:.2f}")
        print(f"Highest Score:         {max_score}")
        print(f"Lowest Score:          {min_score}")
        
        print(f"\n{Colors.BOLD}Gender Distribution:{Colors.RESET}")
        for gender, count in gender_count.items():
            percentage = (count / total_students) * 100
            bar = '█' * int(percentage / 2)
            print(f"  {gender}: {count} ({percentage:.1f}%) {bar}")
        
        print(f"\n{Colors.BOLD}Course Distribution:{Colors.RESET}")
        for course, count in sorted(course_count.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_students) * 100
            bar = '█' * int(percentage / 2)
            print(f"  {course}: {count} ({percentage:.1f}%) {bar}")
        
        print(f"\n{Colors.BOLD}Grade Distribution:{Colors.RESET}")
        for grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D', 'F']:
            count = grade_dist.get(grade, 0)
            if count > 0:
                percentage = (count / total_students) * 100
                bar = '█' * int(percentage / 2)
                print(f"  {grade}: {count} ({percentage:.1f}%) {bar}")
        
        print("="*60)
        logging.info("Statistics displayed successfully")
        
    except Exception as e:
        print_error(f"Error displaying statistics: {e}")
        logging.error(f"Error displaying statistics: {e}")
    finally:
        print("\nPress Enter to continue...")
        input()

def view_logs():
    """Display recent system logs"""
    print_header("SYSTEM LOGS (Last 50 lines)")
    
    try:
        if not os.path.exists('student_system.log'):
            print_warning("No log file found.")
            print("\nPress Enter to continue...")
            input()
            return
        
        with open('student_system.log', 'r') as file:
            lines = file.readlines()
            for line in lines[-50:]:
                print(line.rstrip())
        
        print("="*60)
        
    except Exception as e:
        print_error(f"Error reading log file: {e}")
    
    print("\nPress Enter to continue...")
    input()

# SECTION 12: MAIN MENU


def main_menu():
    """Display the main menu and handle user input"""
    while True:
        print("\n" + "="*60)
        print(f"{Colors.PURPLE}{Colors.BOLD}STUDENT RECORD MANAGEMENT SYSTEM{Colors.RESET}")
        print("="*60)
        print(f"{Colors.CYAN}Main Operations:{Colors.RESET}")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search for Student")
        print("4. Update Student Details")
        print("5. Delete Student")
        print("6. View Statistics")
        print(f"\n{Colors.CYAN}Enhanced Features:{Colors.RESET}")
        print("7. Grade Report")
        print("8. Advanced Search")
        print("9. Export Data")
        print("10. Backup Management")
        print(f"\n{Colors.CYAN}System:{Colors.RESET}")
        print("11. View System Logs")
        print("12. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-12): ").strip()
        
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
            display_grade_report()
        elif choice == '8':
            advanced_search_menu()
        elif choice == '9':
            export_menu()
        elif choice == '10':
            backup_menu()
        elif choice == '11':
            view_logs()
        elif choice == '12':
            logging.info("="*60)
            logging.info("STUDENT MANAGEMENT SYSTEM CLOSED")
            logging.info("="*60)
            print(f"\n{Colors.GREEN}Thank you for using the Student Record Management System!{Colors.RESET}")
            print(f"{Colors.GREEN}Goodbye!{Colors.RESET}\n")
            break
        else:
            print_error("Invalid choice. Please enter a number between 1 and 12.")
            logging.warning(f"Invalid menu choice: {choice}")


# SECTION 13: PROGRAM ENTRY POINT

def main():
    """Main program entry point"""
    try:
        setup_logging()
        initialize_files()
        
        # Display welcome banner
        print_header("WELCOME TO STUDENT RECORD MANAGEMENT SYSTEM")
        print(f"{Colors.CYAN}Version: 2.0 (Enhanced){Colors.RESET}")
        print(f"{Colors.CYAN}Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        
        # Show system status
        students = read_students_from_csv()
        if students:
            print_info(f"Loaded {len(students)} student records")
        else:
            print_info("System ready. No records found.")
        
        print("="*60)
        
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print_info("Program interrupted by user. Goodbye!")
        logging.info("Program interrupted by user")
    except Exception as e:
        print_error(f"A critical error occurred: {e}")
        logging.critical(f"Critical error: {e}")
    finally:
        logging.info("Program execution completed")

if __name__ == "__main__":
    main()