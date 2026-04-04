# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access POS", frappe.PermissionError)

	settings = get_candela_settings()
	lang = get_lang()

	context.candela = settings
	context.page_type = "admin"
	context.title = "نقطة البيع" if lang == "ar" else "Point of Sale"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Menu categories
	context.categories = frappe.get_all(
		"Menu Category",
		filters={"is_active": 1},
		fields=["name", "category_name_ar", "category_name_en", "icon_emoji"],
		order_by="sort_order asc",
	)

	# All available menu items
	context.menu_items = frappe.get_all(
		"Menu Item",
		filters={"is_available": 1},
		fields=[
			"name", "item_name_ar", "item_name_en", "category",
			"price", "discounted_price", "image", "preparation_time_min",
		],
		order_by="sort_order asc",
	)

	# Tables
	context.tables = frappe.get_all(
		"Restaurant Table",
		filters={"is_available": 1},
		fields=["name", "table_number", "section", "capacity"],
		order_by="table_number asc",
	)
