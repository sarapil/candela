// Copyright (c) 2026, Arkan Lab — License: MIT
frappe.listview_settings["POS Invoice"] = {
	add_fields: ["status", "customer", "grand_total", "creation"],
	get_indicator(doc) {
		const map = {
			Draft: [__("Draft"), "orange", "status,=,Draft"],
			Submitted: [__("Submitted"), "green", "status,=,Submitted"],
			Cancelled: [__("Cancelled"), "red", "status,=,Cancelled"],
		};
		return map[doc.status] || [__(doc.status), "grey", `status,=,${doc.status}`];
	},
	formatters: {
		grand_total(val) {
			return val ? format_currency(val) : "";
		},
	},
};
