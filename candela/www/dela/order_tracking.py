# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from candela.utils import get_candela_settings, get_lang, is_rtl

no_cache = 1

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False
	context.title = "Order Tracking – Candela"
	context.candela = get_candela_settings()
	context.candela_lang = get_lang()
	context.candela_rtl = is_rtl()
	context.get_candela_settings = get_candela_settings
