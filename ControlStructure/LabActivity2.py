#Grading school  grading system using if,elif statements
score = int (input("Enter your score:"))
if score >= 90:
    print("Grade: A")
    message = "Excellent work!"
    print(message)
elif score >= 80:
    print("Grade: B")
    message = "Good work!"
    print(message)
elif score >= 70:
    print("Grade: C")
    message = "Average work!"
    print(message)
elif score >= 60:
    print("Grade: D")
    message = "You need to improve!"
    print(message)
elif score < 60:
    print("Grade: F")
    message = "You have failed!"
    print(message)

    print(f"Your score is: {score}")
    print(message)
