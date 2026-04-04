# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Kitchen Display", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "شاشة المطبخ" if lang == "ar" else "Kitchen Display"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True
