# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt, today
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Daily Closing", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "الإقفال اليومي" if lang == "ar" else "Daily Closing"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Daily Closings
	context.closings = frappe.get_all(
		"Daily Closing",
		fields=["name", "closing_date", "prepared_by", "status",
		        "gross_revenue", "cash_collected", "card_collected",
		        "total_expenses", "net_cash_position", "food_cost_percentage",
		        "average_order_value", "creation"],
		order_by="closing_date desc",
		limit=30,
	)

	# Today's closing
	context.today_closing = frappe.db.get_value(
		"Daily Closing",
		{"closing_date": today()},
		["name", "status", "gross_revenue", "net_cash_position", "food_cost_percentage"],
		as_dict=True,
	)

	# Stats
	month_revenue = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(gross_revenue), 0) FROM `tabDaily Closing`
		WHERE MONTH(closing_date) = MONTH(CURDATE()) AND YEAR(closing_date) = YEAR(CURDATE())
		AND status = 'Closed'
	""")[0][0])

	month_expenses = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(total_expenses), 0) FROM `tabDaily Closing`
		WHERE MONTH(closing_date) = MONTH(CURDATE()) AND YEAR(closing_date) = YEAR(CURDATE())
		AND status = 'Closed'
	""")[0][0])

	avg_food_cost = flt(frappe.db.sql("""
		SELECT COALESCE(AVG(food_cost_percentage), 0) FROM `tabDaily Closing`
		WHERE MONTH(closing_date) = MONTH(CURDATE()) AND YEAR(closing_date) = YEAR(CURDATE())
		AND status = 'Closed' AND food_cost_percentage > 0
	""")[0][0])

	context.stats = {
		"month_revenue": month_revenue,
		"month_expenses": month_expenses,
		"month_net": month_revenue - month_expenses,
		"avg_food_cost_pct": avg_food_cost,
		"closings_this_month": frappe.db.count("Daily Closing", {
			"closing_date": [">=", frappe.utils.get_first_day(today())],
			"status": "Closed",
		}),
	}
