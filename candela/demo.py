# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""Candela demo data — load and purge sample data for demonstration."""

import frappe
from frappe import _
from frappe.utils import today, add_days, add_months


@frappe.whitelist()
def load_demo_data():
	"""Install demo menu items, reviews, events, and gallery images."""
	frappe.only_for(["Candela User", "Candela Manager", "System Manager"])


	settings = frappe.get_doc("Candela Settings")
	if settings.demo_data_installed:
		return {"success": False, "message": _("Demo data is already installed.")}

	count = {"items": 0, "reviews": 0, "events": 0, "gallery": 0}

	# ── Demo Menu Items ──────────────────────────────────────────
	demo_items = [
		{"item_name_en": "Bruschetta Classica", "item_name_ar": "بروشيتا كلاسيك", "category": "Appetizers", "price": 85, "is_featured": 1, "is_bestseller": 1, "description_en": "Toasted bread topped with fresh tomatoes, basil, and garlic"},
		{"item_name_en": "Caprese Salad", "item_name_ar": "سلطة كابريزي", "category": "Appetizers", "price": 95, "is_new": 1, "description_en": "Fresh mozzarella, tomatoes, and basil drizzled with olive oil"},
		{"item_name_en": "Margherita Pizza", "item_name_ar": "بيتزا مارجريتا", "category": "Pizza", "price": 120, "is_featured": 1, "is_bestseller": 1, "description_en": "Classic pizza with San Marzano tomatoes, mozzarella, and fresh basil"},
		{"item_name_en": "Quattro Formaggi", "item_name_ar": "كواترو فورماجي", "category": "Pizza", "price": 145, "description_en": "Four cheese pizza: mozzarella, gorgonzola, fontina, and parmesan"},
		{"item_name_en": "Spaghetti Carbonara", "item_name_ar": "سباجيتي كاربونارا", "category": "Pasta", "price": 130, "is_featured": 1, "description_en": "Traditional Roman pasta with eggs, pecorino, guanciale"},
		{"item_name_en": "Fettuccine Alfredo", "item_name_ar": "فيتوتشيني ألفريدو", "category": "Pasta", "price": 125, "description_en": "Creamy parmesan sauce with fresh fettuccine"},
		{"item_name_en": "Penne Arrabbiata", "item_name_ar": "بيني أرابياتا", "category": "Pasta", "price": 110, "description_en": "Spicy tomato sauce with garlic and red chili flakes"},
		{"item_name_en": "Osso Buco", "item_name_ar": "أوسو بوكو", "category": "Main Course", "price": 280, "is_featured": 1, "description_en": "Braised veal shanks in a rich vegetable and wine sauce"},
		{"item_name_en": "Grilled Salmon", "item_name_ar": "سلمون مشوي", "category": "Main Course", "price": 240, "is_new": 1, "description_en": "Atlantic salmon with lemon butter sauce and seasonal vegetables"},
		{"item_name_en": "Tiramisu", "item_name_ar": "تيراميسو", "category": "Desserts", "price": 75, "is_featured": 1, "is_bestseller": 1, "description_en": "Classic Italian dessert with espresso-soaked ladyfingers and mascarpone"},
		{"item_name_en": "Panna Cotta", "item_name_ar": "بانا كوتا", "category": "Desserts", "price": 65, "description_en": "Vanilla bean cream with berry compote"},
		{"item_name_en": "Italian Espresso", "item_name_ar": "إسبريسو إيطالي", "category": "Beverages", "price": 35, "description_en": "Rich and bold Italian espresso"},
		{"item_name_en": "Fresh Lemonade", "item_name_ar": "ليمونادة طازجة", "category": "Beverages", "price": 40, "description_en": "Freshly squeezed lemon with mint"},
	]

	for i, item_data in enumerate(demo_items, 1):
		name = item_data["item_name_en"]
		if not frappe.db.exists("Menu Item", name):
			doc = frappe.new_doc("Menu Item")
			doc.update(item_data)
			doc.is_available = 1
			doc.available_for_delivery = 1
			doc.is_demo_data = 1
			doc.sort_order = i
			doc.insert(ignore_permissions=True)
			count["items"] += 1

	# ── Demo Reviews ─────────────────────────────────────────────
	demo_reviews = [
		{"customer_name": "أحمد محمد", "rating": 1.0, "review_text_ar": "طعام رائع وخدمة ممتازة! أفضل مطعم إيطالي في المدينة", "is_featured": 1},
		{"customer_name": "Sarah Williams", "rating": 0.9, "review_text_en": "Amazing pasta! The carbonara was absolutely authentic. Will definitely come back.", "is_featured": 1},
		{"customer_name": "فاطمة علي", "rating": 1.0, "review_text_ar": "الأجواء ساحرة والطعام لذيذ جداً. تجربة لا تُنسى", "is_featured": 1},
		{"customer_name": "Marco Rossi", "rating": 0.8, "review_text_en": "As an Italian, I can confirm this is the real deal. Bravo!", "is_featured": 0},
	]

	for review_data in demo_reviews:
		doc = frappe.new_doc("Customer Review")
		doc.update(review_data)
		doc.is_approved = 1
		doc.is_demo_data = 1
		doc.source = "Website"
		doc.visit_date = add_days(today(), -10)
		doc.insert(ignore_permissions=True)
		count["reviews"] += 1

	# ── Demo Events ──────────────────────────────────────────────
	demo_events = [
		{"event_name_en": "Italian Wine Night", "event_name_ar": "ليلة النبيذ الإيطالي", "event_date": add_days(today(), 14), "event_time": "19:00", "end_time": "22:00", "price": 350, "max_capacity": 40, "is_featured": 1},
		{"event_name_en": "Live Jazz & Dinner", "event_name_ar": "عشاء مع موسيقى الجاز", "event_date": add_days(today(), 21), "event_time": "20:00", "end_time": "23:00", "price": 250, "max_capacity": 60, "is_featured": 1},
		{"event_name_en": "Cooking Masterclass", "event_name_ar": "ورشة الطبخ الإيطالي", "event_date": add_days(today(), 28), "event_time": "15:00", "end_time": "18:00", "price": 500, "max_capacity": 15, "is_featured": 0},
	]

	for event_data in demo_events:
		name = event_data["event_name_en"]
		if not frappe.db.exists("Restaurant Event", name):
			doc = frappe.new_doc("Restaurant Event")
			doc.update(event_data)
			doc.is_active = 1
			doc.is_demo_data = 1
			doc.insert(ignore_permissions=True)
			count["events"] += 1

	# Mark demo as installed
	settings.demo_data_installed = 1
	settings.demo_installed_on = frappe.utils.now_datetime()
	settings.save(ignore_permissions=True)
	frappe.db.commit()

	msg = _(
		"Demo data installed: {0} menu items, {1} reviews, {2} events"
	).format(count["items"], count["reviews"], count["events"])

	return {"success": True, "message": msg}


@frappe.whitelist()
def purge_demo_data():
	"""Remove all demo data (records with is_demo_data=1)."""
	frappe.only_for(["Candela Manager", "System Manager"])


	settings = frappe.get_doc("Candela Settings")
	if not settings.demo_data_installed:
		return {"success": False, "message": _("No demo data to remove.")}

	doctypes_with_demo = [
		"Menu Item", "Menu Category", "Restaurant Event",
		"Customer Review", "Gallery Image", "Delivery Zone",
		"Promo Code", "Newsletter Subscriber",
	]

	total = 0
	for dt in doctypes_with_demo:
		names = frappe.get_all(dt, filters={"is_demo_data": 1}, pluck="name")
		for name in names:
			frappe.delete_doc(dt, name, ignore_permissions=True, force=True)
			total += 1

	settings.demo_data_installed = 0
	settings.demo_installed_on = None
	settings.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"success": True,
		"message": _("{0} demo records removed").format(total),
	}
