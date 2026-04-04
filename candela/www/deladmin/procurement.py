# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt, today, add_days
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Procurement", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "المشتريات" if lang == "ar" else "Procurement"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Purchase Requests
	context.purchase_requests = frappe.get_all(
		"Purchase Request",
		fields=["name", "request_date", "requested_by", "status", "urgency",
		        "total_estimated_cost", "creation"],
		order_by="creation desc",
		limit=20,
	)

	# Purchase Orders
	context.purchase_orders = frappe.get_all(
		"Purchase Order",
		fields=["name", "supplier", "order_date", "status", "total_amount",
		        "expected_delivery", "creation"],
		order_by="creation desc",
		limit=20,
	)

	# GRNs
	context.grns = frappe.get_all(
		"Goods Receipt Note",
		fields=["name", "supplier", "receipt_date", "purchase_order", "status",
		        "total_cost", "creation"],
		order_by="creation desc",
		limit=20,
	)

	# Stats
	context.stats = {
		"pending_requests": frappe.db.count("Purchase Request", {"status": "Pending"}),
		"open_orders": frappe.db.count("Purchase Order", {"status": ["in", ["Draft", "Ordered"]]}),
		"pending_grns": frappe.db.count("Goods Receipt Note", {"status": "Pending"}),
		"total_spend_this_month": flt(frappe.db.sql("""
			SELECT COALESCE(SUM(total_cost), 0) FROM `tabGoods Receipt Note`
			WHERE status = 'Stocked' AND MONTH(receipt_date) = MONTH(CURDATE())
			AND YEAR(receipt_date) = YEAR(CURDATE())
		""")[0][0]),
	}

	# Suppliers
	context.suppliers = frappe.get_all(
		"Candela Supplier",
		fields=["name", "supplier_name", "phone", "category", "is_active"],
		filters={"is_active": 1},
		order_by="supplier_name asc",
	)
