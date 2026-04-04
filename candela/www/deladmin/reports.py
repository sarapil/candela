# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import today, add_days, getdate, flt
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Reports", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "التقارير" if lang == "ar" else "Reports"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# ── Today's summary ──
	context.today_stats = get_today_stats()

	# ── 7-day revenue ──
	context.weekly_data = get_weekly_revenue()

	# ── Top items ──
	context.top_items = get_top_items(days=30, limit=10)

	# ── Hourly distribution ──
	context.hourly_data = get_hourly_distribution()

	# ── Reservation stats ──
	context.reservation_stats = get_reservation_stats()


def get_today_stats():
	"""Get today's sales and order summary."""
	today_date = today()

	# POS invoices today
	pos_data = frappe.db.sql("""
		SELECT COUNT(*) as count, COALESCE(SUM(grand_total), 0) as total
		FROM `tabPOS Invoice`
		WHERE DATE(creation) = %s AND status = 'Paid'
	""", today_date, as_dict=True)[0]

	# Online orders today
	online_data = frappe.db.sql("""
		SELECT COUNT(*) as count, COALESCE(SUM(total), 0) as total
		FROM `tabOnline Order`
		WHERE DATE(creation) = %s AND status NOT IN ('Cancelled')
	""", today_date, as_dict=True)[0]

	# Reservations today
	res_count = frappe.db.count("Table Reservation", {"reservation_date": today_date})
	guests_count = frappe.db.sql("""
		SELECT COALESCE(SUM(number_of_guests), 0) as total
		FROM `tabTable Reservation`
		WHERE reservation_date = %s AND status IN ('Confirmed', 'Seated', 'Completed')
	""", today_date, as_dict=True)[0].get("total", 0)

	return {
		"pos_count": pos_data.get("count", 0),
		"pos_total": flt(pos_data.get("total", 0)),
		"online_count": online_data.get("count", 0),
		"online_total": flt(online_data.get("total", 0)),
		"total_revenue": flt(pos_data.get("total", 0)) + flt(online_data.get("total", 0)),
		"total_orders": (pos_data.get("count", 0) or 0) + (online_data.get("count", 0) or 0),
		"reservations": res_count,
		"guests": int(guests_count),
	}


def get_weekly_revenue():
	"""Get daily revenue for the past 7 days."""
	data = []
	for i in range(6, -1, -1):
		d = add_days(today(), -i)
		pos_total = frappe.db.sql("""
			SELECT COALESCE(SUM(grand_total), 0) as total FROM `tabPOS Invoice`
			WHERE DATE(creation) = %s AND status = 'Paid'
		""", d, as_dict=True)[0].get("total", 0)

		online_total = frappe.db.sql("""
			SELECT COALESCE(SUM(total), 0) as total FROM `tabOnline Order`
			WHERE DATE(creation) = %s AND status NOT IN ('Cancelled')
		""", d, as_dict=True)[0].get("total", 0)

		data.append({
			"date": d,
			"day": getdate(d).strftime("%a"),
			"pos": flt(pos_total),
			"online": flt(online_total),
			"total": flt(pos_total) + flt(online_total),
		})
	return data


def get_top_items(days=30, limit=10):
	"""Get most ordered items in the past N days."""
	from_date = add_days(today(), -days)

	# From POS
	pos_items = frappe.db.sql("""
		SELECT pi.menu_item, pi.item_name, SUM(pi.quantity) as qty, SUM(pi.amount) as revenue
		FROM `tabPOS Invoice Item` pi
		JOIN `tabPOS Invoice` p ON p.name = pi.parent
		WHERE DATE(p.creation) >= %s AND p.status = 'Paid'
		GROUP BY pi.menu_item
	""", from_date, as_dict=True)

	# From online orders
	online_items = frappe.db.sql("""
		SELECT oi.menu_item, oi.item_name, SUM(oi.quantity) as qty, SUM(oi.amount) as revenue
		FROM `tabOrder Item` oi
		JOIN `tabOnline Order` o ON o.name = oi.parent
		WHERE DATE(o.creation) >= %s AND o.status NOT IN ('Cancelled')
		GROUP BY oi.menu_item
	""", from_date, as_dict=True)

	# Merge
	merged = {}
	for items in [pos_items, online_items]:
		for item in items:
			key = item.get("menu_item")
			if key not in merged:
				merged[key] = {"menu_item": key, "item_name": item.get("item_name", key), "qty": 0, "revenue": 0}
			merged[key]["qty"] += int(item.get("qty", 0))
			merged[key]["revenue"] += flt(item.get("revenue", 0))

	items = sorted(merged.values(), key=lambda x: x["qty"], reverse=True)[:limit]
	return items


def get_hourly_distribution():
	"""Get order count by hour for today."""
	today_date = today()
	hours = []
	for h in range(24):
		count = frappe.db.sql("""
			SELECT COUNT(*) as c FROM (
				SELECT creation FROM `tabPOS Invoice` WHERE DATE(creation) = %s AND HOUR(creation) = %s AND status = 'Paid'
				UNION ALL
				SELECT creation FROM `tabOnline Order` WHERE DATE(creation) = %s AND HOUR(creation) = %s AND status NOT IN ('Cancelled')
			) combined
		""", (today_date, h, today_date, h), as_dict=True)[0].get("c", 0)
		hours.append({"hour": h, "label": f"{h:02d}:00", "count": count or 0})
	return hours


def get_reservation_stats():
	"""Get reservation statistics for the week."""
	stats = {}
	for i in range(6, -1, -1):
		d = add_days(today(), -i)
		total = frappe.db.count("Table Reservation", {"reservation_date": d})
		completed = frappe.db.count("Table Reservation", {"reservation_date": d, "status": "Completed"})
		no_show = frappe.db.count("Table Reservation", {"reservation_date": d, "status": "No-Show"})
		stats[str(d)] = {"total": total, "completed": completed, "no_show": no_show, "day": getdate(d).strftime("%a")}
	return stats
