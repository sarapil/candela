# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Inventory", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "المخزون" if lang == "ar" else "Inventory"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# All ingredients
	ingredients = frappe.get_all(
		"Ingredient",
		filters={"is_active": 1},
		fields=["name", "ingredient_name", "ingredient_name_ar", "category", "unit",
		        "current_stock", "minimum_stock", "cost_per_unit", "supplier"],
		order_by="category asc, ingredient_name asc",
	)

	low_stock = []
	for ing in ingredients:
		ing["is_low"] = flt(ing.current_stock) <= flt(ing.minimum_stock) and flt(ing.minimum_stock) > 0
		if ing["is_low"]:
			low_stock.append(ing)

	context.ingredients = ingredients
	context.low_stock = low_stock

	# Group by category
	cats = {}
	for ing in ingredients:
		cat = ing.get("category") or "Other"
		cats.setdefault(cat, []).append(ing)
	context.categories = cats

	# Recent stock entries
	context.recent_entries = frappe.get_all(
		"Stock Entry",
		fields=["name", "entry_type", "ingredient", "quantity", "date", "supplier"],
		order_by="creation desc",
		limit=10,
	)
