"""
Menu-Driven GUI Calculator

Operations: Addition, Subtraction, Multiplication, Division, Exponentiation, Square Root
"""

import tkinter as tk
from tkinter import messagebox, ttk
import math

# ============================================================
# SECTION 1: CALCULATOR OPERATIONS (FUNCTIONS)
# ============================================================

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b

def multiply(a, b):
    """Return the product of two numbers."""
    return a * b

def divide(a, b):
    """Return the quotient of two numbers. Raises error if dividing by zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

def exponentiate(a, b):
    """Return a raised to the power of b."""
    return a ** b

def square_root(a):
    """Return the square root of a number. Raises error for negative numbers."""
    if a < 0:
        raise ValueError("Cannot take square root of a negative number.")
    return math.sqrt(a)


# ============================================================
# SECTION 2: GUI APPLICATION CLASS
# ============================================================

class CalculatorApp:
    """Main GUI calculator application with menu-driven interface."""
    
    def __init__(self, root):
        """Initialize the calculator window and all components."""
        self.root = root
        self.root.title("Menu-Driven GUI Calculator")
        self.root.geometry("450x370")
        self.root.resizable(False, False)
        
        # Variables for input fields and operation selection
        self.num1_var = tk.StringVar()
        self.num2_var = tk.StringVar()
        self.operation_var = tk.StringVar(value="add")
        
        # Build the GUI components
        self.create_menu()
        self.create_input_fields()
        self.create_buttons()
        self.create_result_display()
        self.create_status_bar()
    
    # --------------------------------------------------------
    # GUI Creation Methods
    # --------------------------------------------------------
    
    def create_menu(self):
        """Create the top menu bar with Operation and Help menus."""
        menubar = tk.Menu(self.root)
        
        # ----- Operation Menu -----
        op_menu = tk.Menu(menubar, tearoff=0)
        op_menu.add_command(label="Addition", command=lambda: self.set_operation("add"))
        op_menu.add_command(label="Subtraction", command=lambda: self.set_operation("subtract"))
        op_menu.add_command(label="Multiplication", command=lambda: self.set_operation("multiply"))
        op_menu.add_command(label="Division", command=lambda: self.set_operation("divide"))
        op_menu.add_separator()
        op_menu.add_command(label="Exponentiation", command=lambda: self.set_operation("exponentiate"))
        op_menu.add_command(label="Square Root", command=lambda: self.set_operation("sqrt"))
        menubar.add_cascade(label="Operation", menu=op_menu)
        
        # ----- Help Menu -----
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # ----- Operation Dropdown (for quick selection) -----
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=8)
        
        tk.Label(frame_top, text="Select Operation:").pack(side=tk.LEFT, padx=5)
        
        operations = ["add", "subtract", "multiply", "divide", "exponentiate", "sqrt"]
        op_dropdown = ttk.Combobox(
            frame_top, 
            textvariable=self.operation_var, 
            values=operations, 
            state="readonly", 
            width=12
        )
        op_dropdown.pack(side=tk.LEFT, padx=5)
        op_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_status())
        
        # Note for square root
        tk.Label(
            frame_top, 
            text="(sqrt uses only Number 1)", 
            font=("Arial", 8), 
            fg="gray"
        ).pack(side=tk.LEFT, padx=5)
    
    def create_input_fields(self):
        """Create input fields for Number 1 and Number 2."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        # Number 1
        tk.Label(frame, text="Number 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry1 = tk.Entry(frame, textvariable=self.num1_var, width=15)
        self.entry1.grid(row=0, column=1, padx=5, pady=5)
        
        # Number 2
        tk.Label(frame, text="Number 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry2 = tk.Entry(frame, textvariable=self.num2_var, width=15)
        self.entry2.grid(row=1, column=1, padx=5, pady=5)
        
        # Hint for square root
        tk.Label(
            frame, 
            text="(For square root, only Number 1 is used)", 
            font=("Arial", 8), 
            fg="gray"
        ).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Set focus to first entry
        self.entry1.focus_set()
    
    def create_buttons(self):
        """Create Calculate and Clear buttons."""
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        
        tk.Button(
            frame, 
            text="Calculate", 
            command=self.calculate, 
            width=10, 
            bg="lightgreen"
        ).grid(row=0, column=0, padx=10)
        
        tk.Button(
            frame, 
            text="Clear", 
            command=self.clear_fields, 
            width=10, 
            bg="lightcoral"
        ).grid(row=0, column=1, padx=10)
    
    def create_result_display(self):
        """Create the label that displays calculation results."""
        self.result_label = tk.Label(
            self.root, 
            text="Result: ", 
            font=("Arial", 12, "bold"), 
            fg="blue"
        )
        self.result_label.pack(pady=15)
    
    def create_status_bar(self):
        """Create the status bar at the bottom of the window."""
        self.status = tk.Label(
            self.root, 
            text="Ready", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
    
    # --------------------------------------------------------
    # Core Functionality Methods
    # --------------------------------------------------------
    
    def set_operation(self, op):
        """Set the current operation from menu selection."""
        self.operation_var.set(op)
        self.update_status()
    
    def update_status(self):
        """Update the status bar with the current operation name."""
        op = self.operation_var.get()
        op_names = {
            "add": "Addition",
            "subtract": "Subtraction",
            "multiply": "Multiplication",
            "divide": "Division",
            "exponentiate": "Exponentiation",
            "sqrt": "Square Root"
        }
        self.status.config(text=f"Selected: {op_names.get(op, op)}")
    
    def calculate(self):
        """
        Perform the selected operation and display the result.
        Handles errors for invalid input and mathematical errors.
        """
        op = self.operation_var.get()
        
        # ---- Square Root (only needs Number 1) ----
        if op == "sqrt":
            try:
                num1 = float(self.num1_var.get().strip())
                result = square_root(num1)
                self.result_label.config(text=f"Result: √{num1} = {result}")
                self.status.config(text=f"Last operation: √  Result: {result}")
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
                self.result_label.config(text="Result: Error")
            return
        
        # ---- All Other Operations (need both numbers) ----
        try:
            num1 = float(self.num1_var.get().strip())
            num2 = float(self.num2_var.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return
        
        # Perform the calculation
        try:
            if op == "add":
                result = add(num1, num2)
                symbol = "+"
            elif op == "subtract":
                result = subtract(num1, num2)
                symbol = "−"
            elif op == "multiply":
                result = multiply(num1, num2)
                symbol = "×"
            elif op == "divide":
                result = divide(num1, num2)
                symbol = "÷"
            elif op == "exponentiate":
                result = exponentiate(num1, num2)
                symbol = "^"
            else:
                messagebox.showerror("Operation Error", "Please select a valid operation.")
                return
            
            # Display result
            self.result_label.config(text=f"Result: {num1} {symbol} {num2} = {result}")
            self.status.config(text=f"Last operation: {symbol}  Result: {result}")
            
        except ValueError as e:
            messagebox.showerror("Math Error", str(e))
            self.result_label.config(text="Result: Error")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.result_label.config(text="Result: Error")
    
    def clear_fields(self):
        """Clear all input fields and reset the result display."""
        self.num1_var.set("")
        self.num2_var.set("")
        self.result_label.config(text="Result: ")
        self.entry1.focus_set()
        self.status.config(text="Fields cleared")
    
    def show_about(self):
        """Display the About dialog with program information."""
        messagebox.showinfo(
            "About Calculator",
            "Menu-Driven GUI Calculator\n"
            "============================\n\n"
            "Operations:\n"
            "  • Addition\n"
            "  • Subtraction\n"
            "  • Multiplication\n"
            "  • Division\n"
            "  • Exponentiation\n"
            "  • Square Root\n\n"
            "Created with Python Tkinter\n"
            "Version 2.0"
        )


# ============================================================
# SECTION 3: MAIN PROGRAM ENTRY POINT
# ============================================================

def main():
    """Create and run the calculator application."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()