# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""Candela install hooks — run after bench install-app candela."""

import frappe


def after_install():
	"""Set up Candela roles, default settings, and initial data."""
	create_roles()
	create_default_settings()
	create_default_categories()
	create_default_tables()
	inject_desktop_icon()
	frappe.db.commit()
	frappe.msgprint("✅ Candela Restaurant app installed successfully!")


def create_roles():
	"""Create Candela roles for fine-grained access control."""
	roles = [
		"Candela Manager",
		"Candela Staff",
		"Candela Chef",
		"Candela Cashier",
		"Candela Waiter",
		"Candela Procurement",
		"Candela Marketing",
	]
	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			role = frappe.new_doc("Role")
			role.role_name = role_name
			role.desk_access = 1
			role.is_custom = 1
			role.insert(ignore_permissions=True)
			frappe.logger().info(f"Created role: {role_name}")


def create_default_settings():
	"""Initialize Candela Settings singleton with sane defaults."""
	if frappe.db.exists("Candela Settings"):
		return

	settings = frappe.new_doc("Candela Settings")
	settings.restaurant_name = "Candela"
	settings.restaurant_name_ar = "كانديلا"
	settings.tagline_ar = "فن المطبخ الإيطالي الأصيل"
	settings.tagline_en = "The Art of Authentic Italian Cuisine"
	settings.tagline_it = "L'arte della cucina italiana"

	# Default feature toggles
	settings.enable_reservations = 1
	settings.enable_reviews = 1
	settings.enable_newsletter = 1
	settings.enable_whatsapp_button = 1
	settings.enable_pickup = 1
	settings.enable_custom_login = 1

	# Default reservation settings
	settings.max_party_size = 20
	settings.reservation_slot_minutes = 30
	settings.advance_booking_days = 30

	# Default colors
	settings.color_primary = "#F59E0B"
	settings.color_dark = "#1C1917"
	settings.color_green = "#059669"
	settings.color_accent = "#FBBF24"

	# Default language
	settings.default_language = "ar"
	settings.enable_english = 1
	settings.currency_symbol = "ج.م"
	settings.currency_code = "EGP"

	# Default hero
	settings.show_hero_logo = 1
	settings.hero_cta_primary_text = "احجز طاولة"
	settings.hero_cta_primary_url = "/dela/reservation"
	settings.hero_cta_secondary_text = "استكشف المنيو"
	settings.hero_cta_secondary_url = "/dela/menu"

	# Homepage sections
	settings.show_about_section = 1
	settings.show_menu_highlights = 1
	settings.show_reservation_cta = 1
	settings.show_testimonials = 1
	settings.show_events = 1
	settings.show_gallery = 1
	settings.show_newsletter = 1

	# Notifications
	settings.notify_new_reservation = 1
	settings.notify_new_order = 1
	settings.notify_new_review = 1

	# Payment
	settings.enable_cash_on_delivery = 1

	# Opening hours
	days_ar = {
		"Saturday": "السبت",
		"Sunday": "الأحد",
		"Monday": "الاثنين",
		"Tuesday": "الثلاثاء",
		"Wednesday": "الأربعاء",
		"Thursday": "الخميس",
		"Friday": "الجمعة",
	}

	for day in days_ar:
		settings.append("opening_hours", {
			"day": day,
			"open_time": "10:00:00",
			"close_time": "23:00:00",
			"is_closed": 1 if day == "Friday" else 0,
		})

	settings.insert(ignore_permissions=True)
	frappe.logger().info("Created default Candela Settings")


def create_default_categories():
	"""Create starter menu categories."""
	categories = [
		{"category_name_en": "Appetizers", "category_name_ar": "المقبلات", "icon_emoji": "🥗", "sort_order": 1},
		{"category_name_en": "Pasta", "category_name_ar": "باستا", "icon_emoji": "🍝", "sort_order": 2},
		{"category_name_en": "Pizza", "category_name_ar": "بيتزا", "icon_emoji": "🍕", "sort_order": 3},
		{"category_name_en": "Main Course", "category_name_ar": "الأطباق الرئيسية", "icon_emoji": "🥩", "sort_order": 4},
		{"category_name_en": "Desserts", "category_name_ar": "الحلويات", "icon_emoji": "🍰", "sort_order": 5},
		{"category_name_en": "Beverages", "category_name_ar": "المشروبات", "icon_emoji": "☕", "sort_order": 6},
	]

	for cat_data in categories:
		if not frappe.db.exists("Menu Category", cat_data["category_name_en"]):
			cat = frappe.new_doc("Menu Category")
			cat.update(cat_data)
			cat.is_active = 1
			cat.insert(ignore_permissions=True)

	frappe.logger().info("Created default menu categories")


def create_default_tables():
	"""Create a few starter restaurant tables."""
	tables = [
		{"table_number": "T1", "section": "Indoor", "capacity": 2},
		{"table_number": "T2", "section": "Indoor", "capacity": 4},
		{"table_number": "T3", "section": "Indoor", "capacity": 4},
		{"table_number": "T4", "section": "Indoor", "capacity": 6},
		{"table_number": "T5", "section": "Outdoor", "capacity": 2},
		{"table_number": "T6", "section": "Outdoor", "capacity": 4},
		{"table_number": "P1", "section": "Private Room", "capacity": 8},
	]

	for tbl_data in tables:
		if not frappe.db.exists("Restaurant Table", tbl_data["table_number"]):
			tbl = frappe.new_doc("Restaurant Table")
			tbl.update(tbl_data)
			tbl.is_available = 1
			tbl.insert(ignore_permissions=True)

	frappe.logger().info("Created default restaurant tables")


def inject_desktop_icon():
	"""Add Candela icon to every user's Desktop Layout (Frappe v16)."""
	try:
		# Check if Desktop Icon doctype exists (Frappe v16+)
		if not frappe.db.exists("DocType", "Desktop Icon"):
			frappe.logger().info("Desktop Icon DocType not found — skipping icon injection")
			return

		icon_name = "Candela"
		if frappe.db.exists("Desktop Icon", {"label": icon_name, "icon_type": "App"}):
			frappe.logger().info(f"Desktop Icon '{icon_name}' already exists")
			return

		icon = frappe.new_doc("Desktop Icon")
		icon.label = "Candela"
		icon.icon_type = "App"
		icon.app = "candela"
		icon.link = "/desk/candela"
		icon.link_type = "External"
		icon.logo_url = "/assets/candela/images/candela-logo.svg"
		icon.bg_color = "amber"
		icon.standard = 1
		icon.insert(ignore_permissions=True)
		frappe.logger().info(f"✅ Injected Desktop Icon: {icon_name}")

		# Also inject into existing Desktop Layouts
		_inject_into_desktop_layouts()

	except Exception as e:
		frappe.logger().warning(f"Desktop Icon injection skipped: {e}")


def _inject_into_desktop_layouts():
	"""Add Candela to all saved Desktop Layout records so the icon is visible."""
	import json as _json

	if not frappe.db.exists("DocType", "Desktop Layout"):
		return

	candela_entry = {
		"label": "Candela",
		"bg_color": "blue",
		"link": "/desk/candela",
		"link_type": "External",
		"app": "candela",
		"icon_type": "App",
		"parent_icon": None,
		"icon": None,
		"link_to": None,
		"idx": 0,
		"standard": 1,
		"logo_url": "/assets/candela/images/candela-logo.svg",
		"hidden": 0,
		"name": "Candela",
		"restrict_removal": 0,
		"icon_image": None,
	}

	for layout in frappe.get_all("Desktop Layout", fields=["name", "layout"]):
		try:
			data = _json.loads(layout.layout or "[]")
			if any(item.get("label") == "Candela" for item in data):
				continue
			data.append(candela_entry)
			frappe.db.set_value("Desktop Layout", layout.name, "layout", _json.dumps(data))
		except Exception:
			pass

	frappe.db.commit()
	frappe.cache.delete_key("desktop_icons")
	frappe.cache.delete_key("bootinfo")
	frappe.logger().info("✅ Injected Candela into Desktop Layouts")
