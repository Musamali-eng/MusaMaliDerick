#Multiple pattern in one case
light_color = input("Enter the traffic light color (red, yellow, green):").lower()

match light_color:
    case "red"| "yellow":
        print("Stop!")

    case "green":
        print("Go!")

    case _:
        print("Invalid traffic light color.")
