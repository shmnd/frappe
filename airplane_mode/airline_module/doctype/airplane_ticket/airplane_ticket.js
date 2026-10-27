frappe.ui.form.on('Airplane Ticket', {
    refresh(frm) {
        // Add custom button "Assign Seat" under the Actions menu or as a top button
        frm.add_custom_button(__('Assign Seat'), function() {
            // Create a dialog with a seat number input field
            let d = new frappe.ui.Dialog({
                title: __('Select Seat'),
                fields: [
                    {
                        label: __('Seat Number'),
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1
                    }
                ],
                primary_action_label: __('Assign'),
                primary_action(values) {
                    // Set the entered value to the Seat field in the form
                    frm.set_value('seat', values.seat_number);
                    // Close the dialog
                    d.hide();
                }
            });

            // Show the dialog
            d.show();
        }, __('Actions')); // Grouped under 'Actions' as shown in the GIF
    }
});