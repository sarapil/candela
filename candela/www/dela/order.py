import frappe
from candela.utils import (
	get_candela_settings, get_menu_categories,
	get_menu_items_by_category, get_lang, is_rtl
)

no_cache = 1

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False
	context.title = "Order Online – Candela"
	context.candela = get_candela_settings()
	context.candela_lang = get_lang()
	context.candela_rtl = is_rtl()

	context.categories = get_menu_categories()
	items = []
	for cat in context.categories:
		cat_items = get_menu_items_by_category(cat.name)
		items.extend(cat_items)
	context.items = items

	context.get_candela_settings = get_candela_settings
