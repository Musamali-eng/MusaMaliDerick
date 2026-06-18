# yourname_contact_assignment.py
# Contact Management System - Function-based

import re

# ============================================
# GLOBAL DATA
# ============================================

contacts = []  # List to store all contacts
next_id = 1    # Auto-incrementing ID

# ============================================
# TASK 1: DATA VALIDATION
# ============================================

def validate_phone(phone):
    """
    Validate phone number: only digits, hyphens, and optional plus sign.
    Returns True if valid, False otherwise.
    """
    if not phone:
        return False
    pattern = r'^\+?[\d\-]+$'
    return bool(re.match(pattern, phone))

def validate_email(email):
    """
    Validate email: must contain @ and a period (.) if provided.
    Returns True if valid or empty (email is optional).
    """
    if not email:
        return True  # Email is optional
    return '@' in email and '.' in email

# ============================================
# CONTACT OPERATIONS WITH VALIDATION
# ============================================

def add_contact(name, phone, email=""):
    """
    Add a new contact with validation.
    Returns True if successful, False otherwise.
    """
    global next_id
    
    # Validate phone
    if not validate_phone(phone):
        print("Error: Invalid phone number. Use only digits, hyphens, and optional '+'.")
        return False
    
    # Validate email
    if not validate_email(email):
        print("Error: Invalid email format. Email must contain '@' and '.'")
        return False
    
    # Check duplicate phone
    for contact in contacts:
        if contact[2] == phone:  # phone is at index 2
            print(f"Error: Phone number {phone} already exists.")
            return False
    
    # Add contact as tuple (id, name, phone, email)
    contact = (next_id, name, phone, email)
    contacts.append(contact)
    next_id += 1
    print(f"Contact '{name}' added successfully with ID {contact[0]}.")
    return True

def view_contact(contact_id):
    """
    View a contact by ID.
    Returns contact tuple or None if not found.
    """
    for contact in contacts:
        if contact[0] == contact_id:  # id is at index 0
            return contact
    return None

def update_contact(contact_id, name=None, phone=None, email=None):
    """
    Update a contact's information with validation.
    Returns True if successful, False otherwise.
    """
    # Find the contact
    contact = view_contact(contact_id)
    if not contact:
        print(f"Error: Contact with ID {contact_id} not found.")
        return False
    
    # Validate phone if provided
    if phone is not None:
        if not validate_phone(phone):
            print("Error: Invalid phone number. Use only digits, hyphens, and optional '+'.")
            return False
        # Check duplicate phone (excluding current contact)
        for c in contacts:
            if c[0] != contact_id and c[2] == phone:
                print(f"Error: Phone number {phone} already exists.")
                return False
    
    # Validate email if provided
    if email is not None:
        if not validate_email(email):
            print("Error: Invalid email format. Email must contain '@' and '.'")
            return False
    
    # Update contact
    updated_contact = list(contact)
    if name is not None:
        updated_contact[1] = name
    if phone is not None:
        updated_contact[2] = phone
    if email is not None:
        updated_contact[3] = email
    
    # Replace in list
    index = contacts.index(contact)
    contacts[index] = tuple(updated_contact)
    print(f"Contact ID {contact_id} updated successfully.")
    return True

def delete_contact(contact_id):
    """
    Delete a contact by ID.
    Returns True if successful, False otherwise.
    """
    contact = view_contact(contact_id)
    if not contact:
        print(f"Error: Contact with ID {contact_id} not found.")
        return False
    
    contacts.remove(contact)
    print(f"Contact ID {contact_id} deleted successfully.")
    return True

# ============================================
# TASK 2: ADVANCED SEARCH
# ============================================

def search_contacts(search_term):
    """
    Search contacts by name, phone, or email.
    Returns formatted string with search results.
    """
    if not search_term:
        return "Please provide a search term."
    
    search_lower = search_term.lower()
    results = []
    
    for contact in contacts:
        # Search by name (index 1), phone (index 2), or email (index 3)
        if (search_lower in contact[1].lower() or
            search_lower in contact[2].lower() or
            search_lower in contact[3].lower()):
            results.append(contact)
    
    if not results:
        return f"No contacts found matching '{search_term}'."
    
    # Format results in a clean table
    output = f"\n=== Search Results for '{search_term}' ===\n"
    output += f"{'ID':<5} {'Name':<25} {'Phone':<20} {'Email':<30}\n"
    output += "-" * 80 + "\n"
    for contact in results:
        output += f"{contact[0]:<5} {contact[1]:<25} {contact[2]:<20} {contact[3]:<30}\n"
    output += "-" * 80 + f"\nFound {len(results)} contact(s)"
    return output

# ============================================
# TASK 3: INTERACTIVE CLI MENU
# ============================================

def display_menu():
    """Display the main menu."""
    print("\n=== Contact Manager Menu ===")
    print("1. Add Contact")
    print("2. View Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. Search Contacts")
    print("6. List All Contacts")
    print("7. Exit")

def list_all_contacts():
    """List all contacts in a formatted table."""
    if not contacts:
        print("No contacts found.")
        return
    
    print("\n=== All Contacts ===")
    print(f"{'ID':<5} {'Name':<25} {'Phone':<20} {'Email':<30}")
    print("-" * 80)
    for contact in contacts:
        print(f"{contact[0]:<5} {contact[1]:<25} {contact[2]:<20} {contact[3]:<30}")
    print("-" * 80)

def get_integer_input(prompt):
    """Safely get integer input from user."""
    try:
        return int(input(prompt))
    except ValueError:
        return None

def main():
    """
    Main function with interactive CLI loop.
    """
    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()
        
        if choice == "1":  # Add Contact
            print("\n--- Add Contact ---")
            name = input("Enter name: ").strip()
            if not name:
                print("Error: Name cannot be empty.")
                continue
            
            phone = input("Enter phone number: ").strip()
            if not phone:
                print("Error: Phone number cannot be empty.")
                continue
            
            email = input("Enter email (optional): ").strip()
            add_contact(name, phone, email)
        
        elif choice == "2":  # View Contact
            print("\n--- View Contact ---")
            contact_id = get_integer_input("Enter contact ID: ")
            if contact_id is None:
                print("Error: Please enter a valid number.")
                continue
            
            contact = view_contact(contact_id)
            if contact:
                print(f"\nID: {contact[0]}")
                print(f"Name: {contact[1]}")
                print(f"Phone: {contact[2]}")
                print(f"Email: {contact[3]}")
            else:
                print(f"Contact with ID {contact_id} not found.")
        
        elif choice == "3":  # Update Contact
            print("\n--- Update Contact ---")
            contact_id = get_integer_input("Enter contact ID to update: ")
            if contact_id is None:
                print("Error: Please enter a valid number.")
                continue
            
            contact = view_contact(contact_id)
            if not contact:
                print(f"Contact with ID {contact_id} not found.")
                continue
            
            print(f"\nCurrent name: {contact[1]}")
            name = input("Enter new name (press Enter to keep current): ").strip()
            if not name:
                name = None
            
            print(f"Current phone: {contact[2]}")
            phone = input("Enter new phone (press Enter to keep current): ").strip()
            if not phone:
                phone = None
            
            print(f"Current email: {contact[3]}")
            email = input("Enter new email (press Enter to keep current): ").strip()
            if not email:
                email = None
            
            update_contact(contact_id, name, phone, email)
        
        elif choice == "4":  # Delete Contact
            print("\n--- Delete Contact ---")
            contact_id = get_integer_input("Enter contact ID to delete: ")
            if contact_id is None:
                print("Error: Please enter a valid number.")
                continue
            
            contact = view_contact(contact_id)
            if not contact:
                print(f"Contact with ID {contact_id} not found.")
                continue
            
            confirm = input(f"Are you sure you want to delete contact ID {contact_id}? (y/n): ").strip().lower()
            if confirm == 'y':
                delete_contact(contact_id)
            else:
                print("Deletion cancelled.")
        
        elif choice == "5":  # Search Contacts
            print("\n--- Search Contacts ---")
            search_term = input("Enter search term (name, phone, or email): ").strip()
            if not search_term:
                print("Error: Search term cannot be empty.")
                continue
            print(search_contacts(search_term))
        
        elif choice == "6":  # List All Contacts
            list_all_contacts()
        
        elif choice == "7":  # Exit
            print("Thank you for using the Contact Management System. Goodbye!")
            break
        
        else:
            print("Invalid option. Please enter a number between 1 and 7.")
        
        # Pause so user can see results
        if choice != "7":
            input("\nPress Enter to continue...")

# ============================================
# SCRIPT EXECUTION
# ============================================

if __name__ == "__main__":
    main()