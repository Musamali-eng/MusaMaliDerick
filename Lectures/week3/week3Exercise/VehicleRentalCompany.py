class Vehicle:
    def __init__(self, registration_number, rental_price_per_day, manufacturer):
        self.registration_number = registration_number
        self.rental_price_per_day = rental_price_per_day
        self.manufacturer = manufacturer

    def calculate_rental_cost(self, days):
        return self.rental_price_per_day * days

    def display_info(self):
        return (
            f"Registration Number: {self.registration_number}\n"
            f"Manufacturer: {self.manufacturer}\n"
            f"Rental Price: ${self.rental_price_per_day}/day"
        )


class Car(Vehicle):
    def __init__(self, registration_number, rental_price_per_day, manufacturer, seating_capacity):
        super().__init__(registration_number, rental_price_per_day, manufacturer)
        self.seating_capacity = seating_capacity

    def display_info(self):
        return (
            f"{super().display_info()}\n"
            f"Seating Capacity: {self.seating_capacity}"
        )


class Motorcycle(Vehicle):
    def __init__(self, registration_number, rental_price_per_day, manufacturer, engine_capacity):
        super().__init__(registration_number, rental_price_per_day, manufacturer)
        self.engine_capacity = engine_capacity

    def display_info(self):
        return (
            f"{super().display_info()}\n"
            f"Engine Capacity: {self.engine_capacity} cc"
        )


def demonstrate():
    car = Car("CAR-001", 50, "Toyota", 5)
    motorcycle = Motorcycle("MOTO-001", 30, "Honda", 250)

    vehicles = [car, motorcycle]

    print("VEHICLE DETAILS ")

    for vehicle in vehicles:
        print(vehicle.display_info())
        print(f"3-Day Rental Cost: ${vehicle.calculate_rental_cost(3)}")


demonstrate()