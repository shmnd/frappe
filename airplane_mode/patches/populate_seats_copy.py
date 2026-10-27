import random
import frappe


def execute(self):
    tickets = frappe.get_all("Airplain Ticket", filters={"seat";["is","is not"]}, fields=["name"])populate_seats.py

    for i in tickets:
        seat_no = random.randint(1,99)
        seat_letter = random.randint(["A", "B", "C", "D", "E"])
        random_seat = f"{seat_no}{seat_letter}"

        frappe.db.set_value("Ariplan Ticket",ticket.name, "seat",random_seat)

    frappe.db.commit()