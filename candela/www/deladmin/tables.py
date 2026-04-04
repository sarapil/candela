# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from candela.utils import get_candela_settings, get_lang, is_rtl
from frappe.utils import today, nowtime


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Table Management", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "إدارة الطاولات" if lang == "ar" else "Table Management"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Get all tables with their status
	tables = frappe.get_all(
		"Restaurant Table",
		fields=["name", "table_number", "section", "capacity", "is_available", "is_combinable", "notes"],
		order_by="table_number asc",
	)

	# Determine occupancy from active POS invoices and reservations
	now_time = nowtime()[:5]
	for table in tables:
		table["status"] = "available"
		table["current_order"] = None
		table["current_reservation"] = None

		# Check if there's an active POS invoice for this table
		active_pos = frappe.get_all(
			"POS Invoice",
			filters={"restaurant_table": table.name, "status": "Draft"},
			fields=["name", "customer_name", "grand_total", "kitchen_status", "creation"],
			order_by="creation desc",
			limit=1,
		)
		if active_pos:
			table["status"] = "occupied"
			table["current_order"] = active_pos[0]

		# Check if there's a confirmed reservation for today
		if table["status"] == "available":
			reservation = frappe.get_all(
				"Table Reservation",
				filters={
					"assigned_table": table.name,
					"reservation_date": today(),
					"status": ["in", ["Confirmed", "Pending"]],
				},
				fields=["name", "guest_name", "reservation_time", "number_of_guests"],
				order_by="reservation_time asc",
				limit=1,
			)
			if reservation:
				table["status"] = "reserved"
				table["current_reservation"] = reservation[0]

		if not table.get("is_available"):
			table["status"] = "unavailable"

	context.tables = tables

	# Group by section
	sections = {}
	for t in tables:
		sec = t.get("section") or "Other"
		sections.setdefault(sec, []).append(t)
	context.sections = sections

	# Today's reservations
	context.today_reservations = frappe.get_all(
		"Table Reservation",
		filters={"reservation_date": today(), "status": ["in", ["Pending", "Confirmed", "Seated"]]},
		fields=["name", "guest_name", "reservation_time", "number_of_guests", "status", "assigned_table", "seating_preference"],
		order_by="reservation_time asc",
	)
