# Copyright (c) 2026, shamnad and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Cannot submit Airplane Ticket unless status is 'Boarded'.")

    def before_insert(self):
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        self.seat = f"{seat_number}{seat_letter}"

    def validate(self):
        # 1. Prevent duplicate add-ons
        seen_items = set()
        if self.add_ons:
            for i in self.add_ons:
                if i.item in seen_items:
                    frappe.throw(f"Add-on '{i.item}' cannot be added more than once.")
                seen_items.add(i.item)

        # 2. Calculate Total Amount (Flight Price + Sum of Add-ons)
        total_add_ons = 0 
        if self.add_ons:
            for i in self.add_ons:
                total_add_ons += i.amount or 0
        
        self.total_amount = float(self.flight_price or 0) + total_add_ons

        # 3. Check Seating Capacity
        if not self.flight:
            return

        # Get the airplane linked to the flight
        airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
        if not airplane:
            return

        # Get the capacity of that airplane
        capacity = frappe.db.get_value("Airplane", airplane, "capacity")
        if not capacity:
            return
        
        # Count existing tickets booked for this flight (excluding current ticket if updating)
        filters = {"flight": self.flight, "docstatus": ["<", 2]}
        if not self.is_new():
            filters["name"] = ["!=", self.name]
            
        existing_tickets_count = frappe.db.count("Airplane Ticket", filters)
        
        # Prevent creation if capacity is reached
        if existing_tickets_count >= capacity:
            frappe.throw("Cannot create a new ticket. This flight is fully booked!")