# list_processor_team_assignment.py

import csv
from functools import reduce

# Load CSV file
def load_data(filename):
    """Load CSV file into a list of dictionaries."""
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    # Convert numeric fields
    for row in data:
        row["Age"] = int(row["Age"])
        row["Purchase_Amount"] = float(row["Purchase_Amount"])
    return data

def main():
    data = load_data(r"C:\Users\DERRICK\Desktop\user_data (1).csv")


    #  Filter + Map
    filtered_users = list(filter(
        lambda u: u["Age"] > 30 and u["Purchase_Amount"] > 100,
        data
    ))
    emails = list(map(lambda u: u["Email"], filtered_users))

    print("\nUsers over 30 with purchases > $100:")
    for u in filtered_users:
        print(f"{u['Name']} ({u['Age']} yrs) - ${u['Purchase_Amount']}")
    print("\nEmails of filtered users:", emails)

    # List comprehension for New York
    ny_users = [f"{u['Name']}: {u['Age']}" for u in data if u["City"] == "New York"]
    print("\nUsers in New York (Name: Age):", ny_users)

    #  Reduce + Sorting
    total_purchase = reduce(lambda acc, u: acc + u["Purchase_Amount"], data, 0)
    print("\nTotal purchase amount of dataset:", total_purchase)

    oldest = sorted(data, key=lambda u: u["Age"], reverse=True)[:5]
    print("\nTop 5 oldest users:")
    for u in oldest:
        print(f"{u['Name']} - {u['Age']} yrs")

    # Integration + Formatting already handled above

if __name__ == "__main__":
    main()