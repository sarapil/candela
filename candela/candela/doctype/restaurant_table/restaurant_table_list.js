// Copyright (c) 2026, Arkan Lab — License: MIT
frappe.listview_settings["Restaurant Table"] = {
	add_fields: ["status", "capacity", "section", "branch"],
	get_indicator(doc) {
		const map = {
			Available: [__("Available"), "green", "status,=,Available"],
			Occupied: [__("Occupied"), "red", "status,=,Occupied"],
			Reserved: [__("Reserved"), "blue", "status,=,Reserved"],
			Cleaning: [__("Cleaning"), "yellow", "status,=,Cleaning"],
			"Out of Service": [__("Out of Service"), "grey", "status,=,Out of Service"],
		};
		return map[doc.status] || [__(doc.status), "grey", `status,=,${doc.status}`];
	},
};
