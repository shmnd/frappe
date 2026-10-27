frappe.ready(function() {
    const urlParams = new URLSearchParams(window.location.search);
    const passenger = urlParams.get('passenger');
    const flight = urlParams.get('flight');
    const flight_price = urlParams.get('flight_price');

	if (passenger) {
        frappe.web_form.set_value('passenger', passenger);
    }

    if (flight) {
        frappe.web_form.set_value('flight', flight);
    }
    
    if (flight_price) {
        frappe.web_form.set_value('flight_price', flight_price);
    }
});