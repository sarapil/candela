// Copyright (c) 2026, Arkan Lab — License: MIT
frappe.listview_settings["Table Reservation"] = {
	add_fields: ["status", "guest_name", "party_size", "reservation_date", "reservation_time"],
	get_indicator(doc) {
		const map = {
			Pending: [__("Pending"), "orange", "status,=,Pending"],
			Confirmed: [__("Confirmed"), "blue", "status,=,Confirmed"],
			Seated: [__("Seated"), "green", "status,=,Seated"],
			Completed: [__("Completed"), "grey", "status,=,Completed"],
			Cancelled: [__("Cancelled"), "red", "status,=,Cancelled"],
			"No Show": [__("No Show"), "red", "status,=,No Show"],
		};
		return map[doc.status] || [__(doc.status), "grey", `status,=,${doc.status}`];
	},
};
