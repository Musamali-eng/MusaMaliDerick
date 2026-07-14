# app.py - Main Application
from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    init_db, 
    add_student, 
    get_all_students, 
    get_student_by_name, 
    get_student_by_id,
    update_student,
    delete_student_permanently,
    soft_delete_student
)
from models import db, Student
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production!

# Custom filter to format dates
@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d'):
    """Format a datetime object to a string."""
    if value is None:
        return 'N/A'
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return value
    return value.strftime(format)

# Initialize database
init_db(app)

@app.route('/')
def home():
    total_students = Student.query.filter_by(is_active=True).count()
    return render_template('home.html', total_students=total_students)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_data = {
            'student_name': request.form.get('student_name', '').strip(),
            'registration_number': request.form.get('registration_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'programme': request.form.get('programme', '').strip()
        }
        
        if not all(student_data.values()):
            flash('All fields are required!', 'error')
            return render_template('register.html', form_data=student_data)
        
        success, message, student = add_student(student_data)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('student_profile', name=student.student_name))
        else:
            flash(message, 'error')
            return render_template('register.html', form_data=student_data)
    
    return render_template('register.html', form_data=None)

@app.route('/student/<name>')
def student_profile(name):
    students = get_student_by_name(name)
    if students:
        return render_template('confirmation.html', student=students[0])
    else:
        flash('Student not found!', 'error')
        return redirect(url_for('register'))

@app.route('/students')
def students_list():
    all_students = get_all_students()
    return render_template('students_list.html', students=all_students)

@app.route('/search', methods=['GET'])
def search_students():
    search_term = request.args.get('q', '').strip()
    if search_term:
        students = get_student_by_name(search_term)
        return render_template('students_list.html', students=students, search_term=search_term)
    return redirect(url_for('students_list'))

@app.route('/student/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash('Student not found!', 'error')
        return redirect(url_for('students_list'))
    
    if request.method == 'POST':
        update_data = {
            'student_name': request.form.get('student_name', '').strip(),
            'registration_number': request.form.get('registration_number', '').strip(),
            'email': request.form.get('email', '').strip(),
            'programme': request.form.get('programme', '').strip()
        }
        
        if not all(update_data.values()):
            flash('All fields are required!', 'error')
            return render_template('edit_student.html', student=student)
        
        success, message, updated_student = update_student(student_id, update_data)
        
        if success:
            flash(message, 'success')
            return redirect(url_for('student_profile', name=updated_student.student_name))
        else:
            flash(message, 'error')
            return render_template('edit_student.html', student=student)
    
    return render_template('edit_student.html', student=student)

@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    success, message = delete_student_permanently(student_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('students_list'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)