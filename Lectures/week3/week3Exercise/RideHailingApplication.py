# ==========================================
# RIDE-HAILING APPLICATION
# ==========================================

# Base Class
class Driver:
    def __init__(self, name, vehicle_registration, rating):
        self.name = name
        self.vehicle_registration = vehicle_registration
        self.rating = rating

    # Abstract-like method
    def calculate_earnings(self):
        raise NotImplementedError(
            "Subclasses must implement calculate_earnings()"
        )

    def display_info(self):
        print("\nDriver Name:", self.name)
        print("Vehicle Registration:", self.vehicle_registration)
        print("Rating:", self.rating)


# Taxi Driver Class
class TaxiDriver(Driver):
    def __init__(self, name, vehicle_registration, rating,
                 trips_completed, commission_per_trip):
        super().__init__(name, vehicle_registration, rating)
        self.trips_completed = trips_completed
        self.commission_per_trip = commission_per_trip

    # Method overriding
    def calculate_earnings(self):
        return self.trips_completed * self.commission_per_trip


# Delivery Driver Class
class DeliveryDriver(Driver):
    def __init__(self, name, vehicle_registration, rating,
                 deliveries_completed, commission_per_delivery):
        super().__init__(name, vehicle_registration, rating)
        self.deliveries_completed = deliveries_completed
        self.commission_per_delivery = commission_per_delivery

    # Method overriding
    def calculate_earnings(self):
        return self.deliveries_completed * self.commission_per_delivery


# ==========================================
# MAIN PROGRAM
# ==========================================

# Create driver objects
driver1 = TaxiDriver(
    "Musa Mali Derick",
    "UBK 123A",
    4.8,
    120,        # trips completed
    5000        # commission per trip
)

driver2 = DeliveryDriver(
    "Sarah Namusoke",
    "UBA 456B",
    4.6,
    150,        # deliveries completed
    3000        # commission per delivery
)

# Polymorphism
drivers = [driver1, driver2]

print("===== DRIVER EARNINGS REPORT =====")

for driver in drivers:
    driver.display_info()
    print("Total Earnings: UGX {:,}".format(driver.calculate_earnings()))
    print("-" * 40)