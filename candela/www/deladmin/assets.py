# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt, today, add_days
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Assets", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "الأصول" if lang == "ar" else "Assets"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Restaurant Assets
	context.assets = frappe.get_all(
		"Restaurant Asset",
		fields=["name", "asset_name", "category", "location", "status",
		        "purchase_date", "purchase_cost", "warranty_until",
		        "next_maintenance_date"],
		order_by="asset_name asc",
	)

	# Maintenance Requests
	context.maintenance_requests = frappe.get_all(
		"Maintenance Request",
		fields=["name", "asset", "reported_at", "priority", "status",
		        "assigned_to", "issue_type", "repair_cost",
		        "completed_at", "downtime_hours", "creation"],
		order_by="creation desc",
		limit=25,
	)

	# Upcoming maintenance
	context.upcoming_maintenance = [
		a for a in context.assets
		if a.next_maintenance_date and str(a.next_maintenance_date) <= str(add_days(today(), 14))
		and a.status == "Active"
	]

	# Stats
	context.stats = {
		"total_assets": len(context.assets),
		"active_assets": len([a for a in context.assets if a.status == "Active"]),
		"pending_maintenance": frappe.db.count("Maintenance Request", {"status": ["in", ["Open", "In Progress"]]}),
		"overdue_maintenance": len([
			a for a in context.assets
			if a.next_maintenance_date and str(a.next_maintenance_date) < str(today())
			and a.status == "Active"
		]),
		"total_asset_value": sum(flt(a.purchase_cost) for a in context.assets),
	}
