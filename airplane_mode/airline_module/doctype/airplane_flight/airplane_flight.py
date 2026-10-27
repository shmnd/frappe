# # Copyright (c) 2026, shamnad and contributors
# # For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator



class AirplaneFlight(WebsiteGenerator):
    def on_submit(self):
        # Set the status field to 'Completed' upon submission
        self.db_set("status", "Completed")
