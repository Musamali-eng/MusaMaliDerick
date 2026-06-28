# HOSPITAL INFORMATION SYSTEM

class Employee:
    def __init__(self, employee_id, name, contact_information):
        self.employee_id = employee_id
        self.name = name
        self.contact_information = contact_information

    def display_details(self):
        print(f"Employee ID: {self.employee_id}")
        print(f"Name: {self.name}")
        print(f"Contact Information: {self.contact_information}")


class Doctor(Employee):
    def __init__(self, employee_id, name, contact_information,
                 specialization, consultation_fee):

        super().__init__(employee_id, name, contact_information)

        self.specialization = specialization
        self.consultation_fee = consultation_fee

    def display_details(self):
        super().display_details()
        print(f"Specialization: {self.specialization}")
        print(f"Consultation Fee: UGX {self.consultation_fee:,}")


class Researcher(Employee):
    def __init__(self, employee_id, name, contact_information,
                 research_area, publications):

        super().__init__(employee_id, name, contact_information)

        self.research_area = research_area
        self.publications = publications

    def display_details(self):
        super().display_details()
        print(f"Research Area: {self.research_area}")
        print(f"Publications: {self.publications}")


class DoctorResearcher(Doctor, Researcher):
    def __init__(self, employee_id, name, contact_information,
                 specialization, consultation_fee,
                 research_area, publications):

        Employee.__init__(self, employee_id, name, contact_information)

        self.specialization = specialization
        self.consultation_fee = consultation_fee
        self.research_area = research_area
        self.publications = publications

    def display_details(self):
        print("\nDOCTOR RESEARCHER DETAILS")
        print("-" * 40)

        Employee.display_details(self)

        print(f"Specialization: {self.specialization}")
        print(f"Consultation Fee: UGX {self.consultation_fee:,}")
        print(f"Research Area: {self.research_area}")
        print(f"Publications: {self.publications}")


def main():

    doctor = Doctor(
        "D001",
        "Dr. Sarah Namusoke",
        "0771234567",
        "Cardiology",
        150000
    )

    researcher = Researcher(
        "R001",
        "John Okello",
        "0787654321",
        "Malaria Research",
        12
    )

    doctor_researcher = DoctorResearcher(
        "DR001",
        "Dr. Grace Nankya",
        "0700112233",
        "Neurology",
        200000,
        "Brain Disorders",
        25
    )

    print("\nDOCTOR DETAILS")
    print("-" * 40)
    doctor.display_details()

    print("\nRESEARCHER DETAILS")
    print("-" * 40)
    researcher.display_details()

    doctor_researcher.display_details()

    print("\nMRO")
    print("-" * 40)
    for cls in DoctorResearcher.__mro__:
        print(cls.__name__)


if __name__ == "__main__":
    main()