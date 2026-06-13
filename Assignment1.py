# Bill Split Calculator

print("=== Bill Split Calculator ===")

# Input validation for bill amount
while True:
    try:
        total_bill = float(input("Enter total bill amount: "))
        if total_bill > 0:
            break
        else:
            print("Bill amount must be greater than 0.")
    except ValueError:
        print("Please enter a valid number.")

# Input validation for number of people
while True:
    try:
        num_people = int(input("Enter number of people: "))
        if num_people > 0:
            break
        else:
            print("Number of people must be greater than 0.")
    except ValueError:
        print("Please enter a valid whole number.")

# Tip percentage selection
print("\nTip Options:")
print("1. 10%")
print("2. 15%")
print("3. 20%")
print("4. Custom")

choice = input("Choose an option (1-4): ")

if choice == "1":
    tip_percent = 10
elif choice == "2":
    tip_percent = 15
elif choice == "3":
    tip_percent = 20
elif choice == "4":
    tip_percent = float(input("Enter custom tip percentage: "))
else:
    print("Invalid choice. Defaulting to 10%.")
    tip_percent = 10

# Calculations
tip_amount = total_bill * (tip_percent / 100)
total_with_tip = total_bill + tip_amount
amount_per_person = total_with_tip / num_people

# Formatted Receipt
print("\n===== RECEIPT =====")
print(f"Bill Amount:      ${total_bill:.2f}")
print(f"Tip Percentage:   {tip_percent}%")
print(f"Tip Amount:       ${tip_amount:.2f}")
print(f"Total Bill:       ${total_with_tip:.2f}")
print(f"People Sharing:   {num_people}")
print(f"Each Person Pays: ${amount_per_person:.2f}")
print("===================")