# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from candela.utils import (
	get_candela_settings, get_featured_items, get_approved_reviews,
	get_active_events, get_lang, is_rtl
)

no_cache = 1

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False
	context.title = "Candela – Italian Restaurant"
	context.candela = get_candela_settings()
	context.candela_lang = get_lang()
	context.candela_rtl = is_rtl()

	# Jinja helpers
	context.get_candela_settings = get_candela_settings
	context.get_featured_items = get_featured_items
	context.get_approved_reviews = get_approved_reviews
	context.get_active_events = get_active_events
