import random
import frappe

def execute():
    # Fetch tickets where seat is empty, None, or whitespace
    tickets = frappe.get_all(
        "Airplane Ticket", 
        filters=[["seat", "in", [None, ""]]], 
        fields=["name"]
    )

    for ticket in tickets:
        seat_no = random.randint(1, 99)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])
        random_seat = f"{seat_no}{seat_letter}"

        frappe.db.set_value("Airplane Ticket", ticket.name, "seat", random_seat)

    frappe.db.commit()