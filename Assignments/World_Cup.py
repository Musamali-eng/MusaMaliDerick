import random

print("WORLD CUP 2026 SIMULATION")
print("=" * 40)

country = input("Enter your country name: ")

balance = 1000000
stage = 1

stages = {
    1: "Group Stage - Match 1",
    2: "Group Stage - Match 2",
    3: "Group Stage - Match 3",
    4: "Round of 16",
    5: "Quarter Final",
    6: "Semi Final",
    7: "Final"
}

print(f"\n{country} starts with a budget of ${balance:,}")
print("Win all matches to become World Cup 2026 Champions!")
print("-" * 40)

while stage <= 7:

    print("\n" + "=" * 40)
    print(f"{stages[stage]}")
    print("=" * 40)
    print(f"Current Budget: ${balance:,}")

    while True:
        try:
            investment = int(input("Enter training investment amount: $"))

            if investment < 0:
                print("Investment cannot be negative.")
                continue  # Ask again

            elif investment > balance:
                print(f"Insufficient budget. You have ${balance:,}")
                continue  # Ask again

            elif investment == 0:
                print("No training investment made. Very low chance to win!")
                pass  # explicitly doing nothing it is a placeholder for zero investment
                break  # Proceed with zero investment

            else:
                break  # Valid positive investment

        except ValueError:
            print("Please enter a valid number.")
            continue  # Ask again

    balance -= investment

    # Winning chances based on investment
    if investment >= 500000:
        win_chance = 0.95
        print("Elite training! Strong preparation!")
    elif investment >= 200000:
        win_chance = 0.80
        print("Good investment! Team is ready!")
    elif investment >= 100000:
        win_chance = 0.65
        print("Decent preparation. Competitive chance.")
    elif investment >= 50000:
        win_chance = 0.50
        print("Average training. 50/50 chance.")
    elif investment >= 10000:
        win_chance = 0.35
        print("Minimal training. Need luck!")
    else:
        win_chance = 0.10
        print("Very poor preparation! Unlikely to win.")
        pass  # Pass statement for low investment scenario

    result = random.random()

    if result < win_chance:
        # WIN!
        prize = investment * 2
        balance += prize

        print(f"\n{country} WON the match!")
        print(f"Prize Money: ${prize:,}")
        print(f"New Budget: ${balance:,}")

        stage += 1

        if stage == 5:
            print("\nReached the Quarter Final!")
        elif stage == 6:
            print("\nReached the Semi Final!")
        elif stage == 7:
            print("\nReached the FINAL!")
        else:
            pass  # No special message for early group matches

    else:
        # LOSS - ELIMINATION (Real World Cup rule)
        print(f"\n {country} LOST the match!")
        print(f"Defeated at {stages[stage]}")
        print("The team has been ELIMINATED from the World Cup.")
        break  # End tournament immediately on loss

# Final Result
if stage > 7:
    print("\n" + "" * 30)
    print(f"CONGRATULATIONS! {country} WINS THE WORLD CUP 2026!")
    print("" * 30)
    print(f"\nFINAL STATISTICS:")
    print(f"Final Budget: ${balance:,}")
    print(f"Total Profit: ${balance - 1000000:,}")
    print(f"Tournament Status: WORLD CHAMPIONS!")

else:
    print("\n" + "=" * 40)
    print(f"Tournament ended at: {stages[stage]}")
    print(f"Remaining Budget: ${balance:,}")
    print("Better luck at World Cup 2030!")
    print("=" * 40)