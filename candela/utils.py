# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""Candela utility / Jinja helper functions."""

import frappe
from frappe.utils import today, now_datetime, cstr


# ═══════════════════════════════════════════════════════════════
# Jinja Methods (registered in hooks.py → jinja.methods)
# ═══════════════════════════════════════════════════════════════

_settings_cache = {}


def get_candela_settings():
	"""Return Candela Settings singleton as a dict. Cached per request."""
	if "settings" not in _settings_cache:
		try:
			_settings_cache["settings"] = frappe.get_cached_doc("Candela Settings")
		except Exception:
			_settings_cache["settings"] = frappe._dict()
	return _settings_cache["settings"]


def get_menu_categories(active_only=True):
	"""Return menu categories ordered by sort_order."""
	filters = {}
	if active_only:
		filters["is_active"] = 1
	return frappe.get_all(
		"Menu Category",
		filters=filters,
		fields=["name", "category_name_ar", "category_name_en", "icon_emoji", "image", "slug", "sort_order"],
		order_by="sort_order asc",
	)


def get_featured_items(limit=6):
	"""Return featured menu items for homepage highlight."""
	return frappe.get_all(
		"Menu Item",
		filters={"is_featured": 1, "is_available": 1},
		fields=[
			"name", "item_name_ar", "item_name_en", "slug", "category",
			"price", "discounted_price", "image", "image_alt_text",
			"is_new", "is_bestseller", "spice_level",
		],
		order_by="sort_order asc",
		limit_page_length=limit,
	)


def get_opening_hours_display():
	"""Return opening hours from settings as a structured list."""
	settings = get_candela_settings()
	if not settings or not hasattr(settings, "opening_hours"):
		return []
	hours = []
	day_ar = {
		"Saturday": "السبت", "Sunday": "الأحد", "Monday": "الاثنين",
		"Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
		"Thursday": "الخميس", "Friday": "الجمعة",
	}
	for row in settings.opening_hours:
		hours.append({
			"day": row.day,
			"day_ar": day_ar.get(row.day, row.day),
			"open_time": cstr(row.open_time)[:5] if row.open_time else "",
			"close_time": cstr(row.close_time)[:5] if row.close_time else "",
			"is_closed": row.is_closed,
		})
	return hours


def get_approved_reviews(limit=6):
	"""Return approved customer reviews."""
	return frappe.get_all(
		"Customer Review",
		filters={"is_approved": 1},
		fields=[
			"customer_name", "rating", "review_text_ar", "review_text_en",
			"source", "customer_photo", "is_featured",
		],
		order_by="is_featured desc, creation desc",
		limit_page_length=limit,
	)


def get_active_events(limit=4):
	"""Return upcoming active events."""
	return frappe.get_all(
		"Restaurant Event",
		filters={"is_active": 1, "event_date": [">=", today()]},
		fields=[
			"name", "event_name_ar", "event_name_en", "slug", "event_date",
			"event_time", "end_time", "image", "price", "max_capacity",
			"current_bookings", "is_featured",
		],
		order_by="event_date asc",
		limit_page_length=limit,
	)


def get_gallery_images(category=None, limit=12):
	"""Return gallery images, optionally filtered by category."""
	filters = {"is_active": 1}
	if category:
		filters["category"] = category
	return frappe.get_all(
		"Gallery Image",
		filters=filters,
		fields=["name", "image", "title_ar", "title_en", "category", "sort_order"],
		order_by="sort_order asc",
		limit_page_length=limit,
	)


def candela_url(path=""):
	"""Generate a /dela/ prefixed URL."""
	if path and not path.startswith("/"):
		path = "/" + path
	return f"/dela{path}"


# ═══════════════════════════════════════════════════════════════
# General Utilities
# ═══════════════════════════════════════════════════════════════

def get_lang():
	"""Get the current language for the Candela website."""
	return frappe.local.lang or "ar"


def is_rtl():
	"""Check if the current language is RTL."""
	return get_lang() in ("ar", "he", "fa", "ur")


def format_currency(amount, symbol=None):
	"""Format a currency amount with the Candela currency symbol."""
	if not symbol:
		settings = get_candela_settings()
		symbol = settings.currency_symbol if settings else "ج.م"
	if amount is None:
		return ""
	return f"{amount:,.0f} {symbol}"


def get_menu_items_by_category(category, available_only=True):
	"""Return menu items filtered by category."""
	filters = {"category": category}
	if available_only:
		filters["is_available"] = 1
	return frappe.get_all(
		"Menu Item",
		filters=filters,
		fields=[
			"name", "item_name_ar", "item_name_en", "slug", "category",
			"description_ar", "description_en", "price", "discounted_price",
			"image", "image_alt_text", "is_new", "is_bestseller",
			"spice_level", "preparation_time_min", "calories",
			"is_available", "is_featured", "available_for_delivery",
		],
		order_by="sort_order asc",
	)
