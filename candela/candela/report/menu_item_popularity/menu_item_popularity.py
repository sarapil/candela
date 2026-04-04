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
	return columns, data, None, chart


def get_columns():
	return [
		{"fieldname": "item_name", "label": "Menu Item", "fieldtype": "Data", "width": 200},
		{"fieldname": "category", "label": "Category", "fieldtype": "Link", "options": "Menu Category", "width": 140},
		{"fieldname": "pos_qty", "label": "POS Qty", "fieldtype": "Int", "width": 90},
		{"fieldname": "online_qty", "label": "Online Qty", "fieldtype": "Int", "width": 100},
		{"fieldname": "total_qty", "label": "Total Qty", "fieldtype": "Int", "width": 100},
		{"fieldname": "total_revenue", "label": "Revenue", "fieldtype": "Currency", "width": 130},
		{"fieldname": "avg_price", "label": "Avg Price", "fieldtype": "Currency", "width": 110},
	]


def get_data(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	category = filters.get("category")

	# POS items
	pos_cond = ""
	pos_params = [from_date, to_date]
	if category:
		pos_cond = "AND mi.category = %s"
		pos_params.append(category)

	pos_data = frappe.db.sql("""
		SELECT pi.menu_item,
			COALESCE(pi.item_name, mi.item_name_en) as item_name,
			mi.category,
			SUM(pi.quantity) as qty,
			SUM(pi.amount) as revenue
		FROM `tabPOS Invoice Item` pi
		JOIN `tabPOS Invoice` p ON p.name = pi.parent
		LEFT JOIN `tabMenu Item` mi ON mi.name = pi.menu_item
		WHERE p.status != 'Cancelled'
			AND DATE(p.creation) BETWEEN %s AND %s
			{cond}
		GROUP BY pi.menu_item
	""".format(cond=pos_cond), pos_params, as_dict=True)

	pos_map = {r.menu_item: r for r in pos_data}

	# Online items
	online_cond = ""
	online_params = [from_date, to_date]
	if category:
		online_cond = "AND mi.category = %s"
		online_params.append(category)

	online_data = frappe.db.sql("""
		SELECT oi.menu_item,
			COALESCE(oi.item_name, mi.item_name_en) as item_name,
			mi.category,
			SUM(oi.quantity) as qty,
			SUM(oi.amount) as revenue
		FROM `tabOrder Item` oi
		JOIN `tabOnline Order` o ON o.name = oi.parent
		LEFT JOIN `tabMenu Item` mi ON mi.name = oi.menu_item
		WHERE o.status NOT IN ('Cancelled', 'Rejected')
			AND DATE(o.creation) BETWEEN %s AND %s
			{cond}
		GROUP BY oi.menu_item
	""".format(cond=online_cond), online_params, as_dict=True)

	online_map = {r.menu_item: r for r in online_data}

	# Merge
	all_items = sorted(set(list(pos_map.keys()) + list(online_map.keys())))

	data = []
	for item in all_items:
		pos = pos_map.get(item, {})
		online = online_map.get(item, {})
		pos_qty = (pos.get("qty") or 0)
		online_qty = (online.get("qty") or 0)
		total_qty = pos_qty + online_qty
		total_rev = flt(pos.get("revenue", 0)) + flt(online.get("revenue", 0))
		avg_price = total_rev / total_qty if total_qty else 0

		data.append({
			"item_name": pos.get("item_name") or online.get("item_name") or item,
			"category": pos.get("category") or online.get("category"),
			"pos_qty": pos_qty,
			"online_qty": online_qty,
			"total_qty": total_qty,
			"total_revenue": total_rev,
			"avg_price": avg_price,
		})

	data.sort(key=lambda x: x["total_qty"], reverse=True)
	return data


def get_chart(data):
	top = data[:10]
	return {
		"data": {
			"labels": [r["item_name"][:20] for r in top],
			"datasets": [
				{"name": "Quantity Sold", "values": [r["total_qty"] for r in top]},
			],
		},
		"type": "bar",
		"colors": ["#C9A96E"],
	}
