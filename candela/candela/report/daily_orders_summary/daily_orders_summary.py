# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	summary = get_summary(data)
	return columns, data, None, chart, summary


def get_columns():
	return [
		{"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
		{"fieldname": "pos_orders", "label": "POS Orders", "fieldtype": "Int", "width": 110},
		{"fieldname": "pos_revenue", "label": "POS Revenue", "fieldtype": "Currency", "width": 130},
		{"fieldname": "online_orders", "label": "Online Orders", "fieldtype": "Int", "width": 120},
		{"fieldname": "online_revenue", "label": "Online Revenue", "fieldtype": "Currency", "width": 140},
		{"fieldname": "total_orders", "label": "Total Orders", "fieldtype": "Int", "width": 110},
		{"fieldname": "total_revenue", "label": "Total Revenue", "fieldtype": "Currency", "width": 140},
		{"fieldname": "avg_order_value", "label": "Avg Order Value", "fieldtype": "Currency", "width": 140},
	]


def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# POS data
	pos_data = frappe.db.sql("""
		SELECT DATE(creation) as date,
			COUNT(*) as orders,
			SUM(grand_total) as revenue
		FROM `tabPOS Invoice`
		WHERE status != 'Cancelled'
			AND DATE(creation) BETWEEN %s AND %s
		GROUP BY DATE(creation)
	""", (from_date, to_date), as_dict=True)

	pos_map = {str(r.date): r for r in pos_data}

	# Online data
	online_data = frappe.db.sql("""
		SELECT DATE(creation) as date,
			COUNT(*) as orders,
			SUM(total) as revenue
		FROM `tabOnline Order`
		WHERE status NOT IN ('Cancelled', 'Rejected')
			AND DATE(creation) BETWEEN %s AND %s
		GROUP BY DATE(creation)
	""", (from_date, to_date), as_dict=True)

	online_map = {str(r.date): r for r in online_data}

	# Merge dates
	all_dates = sorted(set(list(pos_map.keys()) + list(online_map.keys())))

	data = []
	for d in all_dates:
		pos = pos_map.get(d, {})
		online = online_map.get(d, {})
		pos_orders = pos.get("orders", 0) or 0
		pos_rev = flt(pos.get("revenue", 0))
		online_orders = online.get("orders", 0) or 0
		online_rev = flt(online.get("revenue", 0))
		total_orders = pos_orders + online_orders
		total_rev = pos_rev + online_rev
		avg = total_rev / total_orders if total_orders else 0

		data.append({
			"date": d,
			"pos_orders": pos_orders,
			"pos_revenue": pos_rev,
			"online_orders": online_orders,
			"online_revenue": online_rev,
			"total_orders": total_orders,
			"total_revenue": total_rev,
			"avg_order_value": avg,
		})

	return data


def get_chart(data):
	labels = [r["date"] for r in data]
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{"name": "POS Revenue", "values": [r["pos_revenue"] for r in data]},
				{"name": "Online Revenue", "values": [r["online_revenue"] for r in data]},
			],
		},
		"type": "bar",
		"colors": ["#C9A96E", "#5BB369"],
	}


def get_summary(data):
	total_orders = sum(r["total_orders"] for r in data)
	total_revenue = sum(r["total_revenue"] for r in data)
	avg = total_revenue / total_orders if total_orders else 0
	return [
		{"value": total_orders, "label": "Total Orders", "datatype": "Int"},
		{"value": total_revenue, "label": "Total Revenue", "datatype": "Currency"},
		{"value": avg, "label": "Avg Order Value", "datatype": "Currency"},
	]
