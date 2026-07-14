# database.py - Database Operations
from flask_sqlalchemy import SQLAlchemy
from models import db, Student
from datetime import datetime

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
        
        if Student.query.count() == 0:
            add_sample_data()

def add_sample_data():
    sample_students = [
        Student(
            student_name='Mukisa Samuel',
            registration_number='2400/U/003',
            email='mukisa.samuel@mak.ac.com',
            programme='Computer Science',
            created_at=datetime.utcnow()
        ),
        Student(
            student_name='Jane Nakato',
            registration_number='23/U/2342/EVE',
            email='jane.nakato@mak.com',
            programme='Information Technology',
            created_at=datetime.utcnow()
        ),
        Student(
            student_name='John Doe',
            registration_number='STU2024001',
            email='john.doe@university.edu',
            programme='Computer Science',
            created_at=datetime.utcnow()
        ),
        Student(
            student_name='Jane Smith',
            registration_number='STU2024002',
            email='jane.smith@university.edu',
            programme='Information Technology',
            created_at=datetime.utcnow()
        )
    ]
    
    for student in sample_students:
        db.session.add(student)
    db.session.commit()
    print("📚 Sample data added!")

def get_all_students():
    return Student.query.filter_by(is_active=True).all()

def get_student_by_name(name):
    return Student.query.filter(
        Student.student_name.contains(name),
        Student.is_active == True
    ).all()

def get_student_by_registration(registration_number):
    return Student.query.filter_by(registration_number=registration_number).first()

def get_student_by_id(student_id):
    """Get a student by their ID"""
    return Student.query.get(student_id)

def add_student(student_data):
    try:
        existing = get_student_by_registration(student_data['registration_number'])
        if existing:
            return False, "Registration number already exists!", None
        
        existing_email = Student.query.filter_by(email=student_data['email']).first()
        if existing_email:
            return False, "Email already registered!", None
        
        new_student = Student(
            student_name=student_data['student_name'],
            registration_number=student_data['registration_number'],
            email=student_data['email'],
            programme=student_data['programme'],
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_student)
        db.session.commit()
        return True, "Student registered successfully!", new_student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None

def update_student(student_id, update_data):
    """
    Update an existing student's information
    Returns: (success, message, student)
    """
    try:
        # Get the student by ID
        student = get_student_by_id(student_id)
        if not student:
            return False, "Student not found!", None
        
        # Check if registration number is being changed and if it already exists
        new_reg = update_data.get('registration_number')
        if new_reg and new_reg != student.registration_number:
            existing = get_student_by_registration(new_reg)
            if existing:
                return False, "Registration number already exists!", None
        
        # Check if email is being changed and if it already exists
        new_email = update_data.get('email')
        if new_email and new_email != student.email:
            existing_email = Student.query.filter_by(email=new_email).first()
            if existing_email:
                return False, "Email already registered!", None
        
        # Update student fields
        updatable_fields = ['student_name', 'registration_number', 'email', 'programme']
        for field in updatable_fields:
            if field in update_data and update_data[field] is not None:
                setattr(student, field, update_data[field])
        
        # ✅ Update timestamp
        student.updated_at = datetime.utcnow()
        
        db.session.commit()
        return True, "Student updated successfully!", student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None

def delete_student_permanently(student_id):
    """
    Permanently delete a student from the database
    Returns: (success, message)
    """
    try:
        student = get_student_by_id(student_id)
        if not student:
            return False, "Student not found!"
        
        db.session.delete(student)
        db.session.commit()
        return True, "Student permanently deleted successfully!"
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"

def soft_delete_student(student_id):
    """
    Soft delete a student (set is_active to False)
    Returns: (success, message, student)
    """
    try:
        student = get_student_by_id(student_id)
        if not student:
            return False, "Student not found!", None
        
        student.is_active = False
        db.session.commit()
        return True, "Student deactivated successfully!", student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None

def reactivate_student(student_id):
    """
    Reactivate a soft-deleted student
    Returns: (success, message, student)
    """
    try:
        student = Student.query.filter_by(id=student_id, is_active=False).first()
        if not student:
            return False, "Student not found or already active!", None
        
        student.is_active = True
        db.session.commit()
        return True, "Student reactivated successfully!", student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None

def get_all_students_including_inactive():
    """Get all students including inactive ones"""
    return Student.query.all()

def get_inactive_students():
    """Get only inactive students"""
    return Student.query.filter_by(is_active=False).all()