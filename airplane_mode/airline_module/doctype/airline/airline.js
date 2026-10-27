// Copyright (c) 2026, shamnad and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
    refresh(frm) {
        // Check if the website field has a value
        if (frm.doc.website) {
            // Add a sidebar link pointing to the official website
            frm.add_web_link(frm.doc.website, "Visit Website");
        }
    }
});