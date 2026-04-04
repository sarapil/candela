# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	summary = get_summary(filters)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
		{"fieldname": "total", "label": "Total Reservations", "fieldtype": "Int", "width": 140},
		{"fieldname": "confirmed", "label": "Confirmed", "fieldtype": "Int", "width": 100},
		{"fieldname": "completed", "label": "Completed", "fieldtype": "Int", "width": 100},
		{"fieldname": "cancelled", "label": "Cancelled", "fieldtype": "Int", "width": 100},
		{"fieldname": "no_show", "label": "No-Show", "fieldtype": "Int", "width": 90},
		{"fieldname": "total_guests", "label": "Total Guests", "fieldtype": "Int", "width": 110},
		{"fieldname": "avg_party_size", "label": "Avg Party Size", "fieldtype": "Float", "precision": 1, "width": 120},
	]


def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	results = frappe.db.sql("""
		SELECT
			reservation_date as date,
			COUNT(*) as total,
			SUM(CASE WHEN status = 'Confirmed' THEN 1 ELSE 0 END) as confirmed,
			SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
			SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) as cancelled,
			SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) as no_show,
			SUM(number_of_guests) as total_guests,
			AVG(number_of_guests) as avg_party_size
		FROM `tabTable Reservation`
		WHERE reservation_date BETWEEN %s AND %s
		GROUP BY reservation_date
		ORDER BY reservation_date
	""", (from_date, to_date), as_dict=True)

	return results


def get_chart(data):
	labels = [str(r["date"]) for r in data]
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "Completed", "values": [r.get("completed", 0) or 0 for r in data]},
				{"name": "Cancelled", "values": [r.get("cancelled", 0) or 0 for r in data]},
				{"name": "No-Show", "values": [r.get("no_show", 0) or 0 for r in data]},
			],
		},
		"type": "bar",
		"colors": ["#5BB369", "#D4534B", "#888"],
	}


def get_summary(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	totals = frappe.db.sql("""
		SELECT
			COUNT(*) as total,
			SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed,
			SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) as no_show,
			SUM(number_of_guests) as guests
		FROM `tabTable Reservation`
		WHERE reservation_date BETWEEN %s AND %s
	""", (from_date, to_date), as_dict=True)[0]

	total = totals.get("total") or 0
	completed = totals.get("completed") or 0
	no_show = totals.get("no_show") or 0
	rate = (completed / total * 100) if total else 0
	no_show_rate = (no_show / total * 100) if total else 0

	return [
		{"value": total, "label": "Total Reservations", "datatype": "Int"},
		{"value": totals.get("guests") or 0, "label": "Total Guests", "datatype": "Int"},
		{"value": rate, "label": "Completion Rate %", "datatype": "Percent"},
		{"value": no_show_rate, "label": "No-Show Rate %", "datatype": "Percent", "indicator": "red" if no_show_rate > 15 else "green"},
	]
