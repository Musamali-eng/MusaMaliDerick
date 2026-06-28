# E-COMMERCE PLATFORM

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def display_product(self):
        print(f"Product ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: UGX {self.price:,.2f}")


class Discountable:
    def __init__(self, discount_percentage):
        self.discount_percentage = discount_percentage

    def calculate_discount(self, price):
        discount_amount = price * (self.discount_percentage / 100)
        return price - discount_amount


class Taxable:
    def __init__(self, tax_rate):
        self.tax_rate = tax_rate

    def calculate_tax(self, price):
        return price * (self.tax_rate / 100)


class DiscountedTaxableProduct(Product, Discountable, Taxable):
    def __init__(self, product_id, name, price,
                 discount_percentage, tax_rate):

        Product.__init__(self, product_id, name, price)
        Discountable.__init__(self, discount_percentage)
        Taxable.__init__(self, tax_rate)

    def final_price(self):

        discounted_price = self.calculate_discount(self.price)

        tax_amount = self.calculate_tax(discounted_price)

        final_amount = discounted_price + tax_amount

        return discounted_price, tax_amount, final_amount

    def display_product(self):
        super().display_product()

        discounted_price, tax_amount, final_amount = self.final_price()

        print(f"Discount: {self.discount_percentage}%")
        print(f"Tax Rate: {self.tax_rate}%")
        print(f"Price After Discount: UGX {discounted_price:,.2f}")
        print(f"Tax Amount: UGX {tax_amount:,.2f}")
        print(f"Final Selling Price: UGX {final_amount:,.2f}")


def main():

    laptop = DiscountedTaxableProduct(
        "P001",
        "Laptop",
        2500000,
        10,
        18
    )

    phone = DiscountedTaxableProduct(
        "P002",
        "Smartphone",
        1200000,
        5,
        18
    )

    print("\nPRODUCT 1")
    print("-" * 40)
    laptop.display_product()

    print("\nPRODUCT 2")
    print("-" * 40)
    phone.display_product()

    print("\nMRO")
    print("-" * 40)
    for cls in DiscountedTaxableProduct.__mro__:
        print(cls.__name__)


if __name__ == "__main__":
    main()