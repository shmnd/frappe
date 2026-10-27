import frappe
from frappe.model.document import Document

class FlightPassenger(Document):
    def before_save(self):
        # Strip whitespace and safely combine first & last name
        first = (self.first_name or "").strip()
        last = (self.last_name or "").strip()

        if first and last:
            self.full_name = f"{first} {last}"
        elif first:
            self.full_name = first
        elif last:
            self.full_name = last
        else:
            self.full_name = ""