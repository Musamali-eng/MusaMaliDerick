def e_commerce_system():
    print("===================================")
    print(" Welcome to the E-Commerce System ")
    print("===================================")

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:

        username = input("Enter username: ")
        password = input("Enter password: ")

        if username == "admin":
            if password == "admin123":
                role = "Admin"
                print("Login Successful!")
                print("Access Level: All Features")
                break
            else:
                attempts += 1
                print(f"Incorrect Password! Attempts left: {max_attempts - attempts}")

        elif username == "customer":
            if password == "cust123":
                role = "Customer"
                print("Login Successful!")
                print("Access Level: Shopping Features")
                break
            else:
                attempts += 1
                print(f"Incorrect Password! Attempts left: {max_attempts - attempts}")

        elif username == "cashier":
            if password == "cash123":
                role = "Cashier"
                print("Login Successful!")
                print("Access Level: Sales and Billing")
                break
            else:
                attempts += 1
                print(f"Incorrect Password! Attempts left: {max_attempts - attempts}")

        else:
            attempts += 1
            print(f"Username Not Found! Attempts left: {max_attempts - attempts}")

    if attempts == max_attempts:
        print("Account locked! Too many failed attempts.")
        return

    subtotal = float(input("\nEnter product subtotal: "))

    if subtotal >= 500000:
        discount = 0.20
    elif subtotal >= 200000:
        discount = 0.10
    else:
        discount = 0.05

    coupon = input("Enter coupon code: ")

    if coupon == "SAVE10":
        coupon_discount = 0.10
        print("Valid coupon applied.")
    else:
        coupon_discount = 0
        print("Invalid coupon code.")

    location = input("Enter location (Kampala/Jinja/Mbarara): ")

    if location == "Kampala":
        tax_rate = 0.18
    elif location == "Jinja":
        tax_rate = 0.15
    elif location == "Mbarara":
        tax_rate = 0.12
    else:
        tax_rate = 0.10

    discount_amount = subtotal * discount
    coupon_amount = subtotal * coupon_discount

    price_after_discount = subtotal - discount_amount - coupon_amount
    tax_amount = price_after_discount * tax_rate
    final_price = price_after_discount + tax_amount

    print("\n========== RECEIPT ==========")
    print(f"User Role: {role}")
    print(f"Subtotal: {subtotal}")
    print(f"Discount: {discount_amount}")
    print(f"Coupon Discount: {coupon_amount}")
    print(f"Tax: {tax_amount}")
    print(f"Final Price: {final_price}")
    print("=============================")


# Call the function
e_commerce_system()