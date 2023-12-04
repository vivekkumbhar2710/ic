// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt



frappe.ui.form.on('Interest Amount Calculation', {
	to_date: function (frm) {
		frm.call({
			method:'get_BalanceDetails',
			doc: frm.doc,
		});
	}
});

frappe.ui.form.on('Interest Amount Calculation', {
	get_details: function (frm) {
		frm.call({
			method:'get_Details',
			doc: frm.doc,
		});
	}
});