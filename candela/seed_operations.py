"""Seed fixture data for Candela operations, governance & marketing DocTypes.

Usage:
    bench --site dev.localhost execute candela.seed_operations.seed_all
"""
import frappe
from frappe.utils import today, add_days


def seed_all():
	"""One-shot idempotent seeder for all supplementary-prompt fixtures."""
	seed_customer_personas()
	seed_service_modes()
	seed_kitchen_stations()
	seed_warehouses()
	seed_cafe_amenities()
	seed_competitors()
	frappe.db.commit()
	print("✅  Candela operations seed data created.")


# ── B1: Customer Personas ─────────────────────────────────────────────
def seed_customer_personas():
	personas = [
		{
			"persona_name_ar": "عائلة الويك إند",
			"persona_name_en": "Weekend Family",
			"persona_code": "FAMILY",
			"age_range": "30-45",
			"income_level": "Medium-High",
			"visit_pattern": "Weekly",
			"preferred_channels": "Instagram, Facebook",
			"decision_factors": "Ambiance, Kid-friendly, Quality",
			"is_active": 1,
		},
		{
			"persona_name_ar": "رجل الأعمال",
			"persona_name_en": "Business Executive",
			"persona_code": "EXECUTIVE",
			"age_range": "35-55",
			"income_level": "High",
			"visit_pattern": "2-3 times/week",
			"preferred_channels": "WhatsApp, Direct",
			"decision_factors": "Speed, Privacy, Quality",
			"is_active": 1,
		},
		{
			"persona_name_ar": "الشباب المغامر",
			"persona_name_en": "Adventurous Youth",
			"persona_code": "YOUTH",
			"age_range": "22-32",
			"income_level": "Medium",
			"visit_pattern": "Monthly",
			"preferred_channels": "TikTok, Instagram",
			"decision_factors": "Uniqueness, Social Media worthy, Deals",
			"is_active": 1,
		},
	]
	for p in personas:
		if not frappe.db.exists("Customer Persona", p["persona_code"]):
			doc = frappe.new_doc("Customer Persona")
			doc.update(p)
			doc.insert(ignore_permissions=True)
	print("  → Customer Personas seeded")


# ── B2: Service Modes ─────────────────────────────────────────────────
def seed_service_modes():
	modes = [
		{"mode_name_ar": "أكل في المطعم", "mode_name_en": "Dine-in", "mode_code": "DINEIN", "lighting_preset": "Warm", "is_active": 1},
		{"mode_name_ar": "طلب سفري", "mode_name_en": "Takeaway", "mode_code": "TAKEAWAY", "is_active": 1},
		{"mode_name_ar": "توصيل للبيت", "mode_name_en": "Delivery", "mode_code": "DELIVERY", "is_active": 1},
		{"mode_name_ar": "خدمة تموين", "mode_name_en": "Catering", "mode_code": "CATERING", "is_active": 1},
		{"mode_name_ar": "طلب من السيارة", "mode_name_en": "Drive-through", "mode_code": "DRIVE", "is_active": 0},
	]
	for m in modes:
		if not frappe.db.exists("Service Mode", m["mode_code"]):
			doc = frappe.new_doc("Service Mode")
			doc.update(m)
			doc.insert(ignore_permissions=True)
	print("  → Service Modes seeded")


# ── A6: Kitchen Stations ──────────────────────────────────────────────
def seed_kitchen_stations():
	stations = [
		{"station_name": "Pasta Station", "station_type": "Pasta", "max_concurrent_orders": 8, "is_active": 1},
		{"station_name": "Pizza Oven", "station_type": "Pizza", "max_concurrent_orders": 6, "is_active": 1},
		{"station_name": "Grill Station", "station_type": "Grill", "max_concurrent_orders": 5, "is_active": 1},
		{"station_name": "Salad & Cold", "station_type": "Cold Line", "max_concurrent_orders": 10, "is_active": 1},
		{"station_name": "Dessert Station", "station_type": "Dessert", "max_concurrent_orders": 6, "is_active": 1},
		{"station_name": "Beverage Bar", "station_type": "Bar", "max_concurrent_orders": 12, "is_active": 1},
	]
	for s in stations:
		if not frappe.db.exists("Kitchen Station", {"station_name": s["station_name"]}):
			doc = frappe.new_doc("Kitchen Station")
			doc.update(s)
			doc.insert(ignore_permissions=True)
	print("  → Kitchen Stations seeded")


# ── A3: Warehouses ────────────────────────────────────────────────────
def seed_warehouses():
	warehouses = [
		{"warehouse_name": "Main Kitchen Store", "warehouse_type": "Kitchen", "location": "Ground Floor", "is_active": 1},
		{"warehouse_name": "Cold Storage", "warehouse_type": "Cold Storage", "location": "Basement", "is_active": 1},
		{"warehouse_name": "Dry Store", "warehouse_type": "Dry Storage", "location": "Ground Floor", "is_active": 1},
		{"warehouse_name": "Bar Storage", "warehouse_type": "Bar", "location": "Bar Area", "is_active": 1},
	]
	for w in warehouses:
		if not frappe.db.exists("Candela Warehouse", {"warehouse_name": w["warehouse_name"]}):
			doc = frappe.new_doc("Candela Warehouse")
			doc.update(w)
			doc.insert(ignore_permissions=True)
	print("  → Warehouses seeded")


# ── B8: Café Amenities ────────────────────────────────────────────────
def seed_cafe_amenities():
	amenities = [
		{"amenity_name": "Free WiFi", "amenity_name_ar": "واي فاي مجاني", "amenity_type": "WiFi", "wifi_ssid": "Candela_Guest", "wifi_speed_mbps": 100, "show_on_website": 1},
		{"amenity_name": "Live Music", "amenity_name_ar": "موسيقى حية", "amenity_type": "Other", "description_en": "Live music every Thursday & Friday", "show_on_website": 1},
		{"amenity_name": "Kids Corner", "amenity_name_ar": "ركن الأطفال", "amenity_type": "Other", "zone": "Indoor", "show_on_website": 1},
		{"amenity_name": "Outdoor Terrace", "amenity_name_ar": "تراس خارجي", "amenity_type": "Seating", "zone": "Outdoor", "show_on_website": 1},
		{"amenity_name": "Private Room", "amenity_name_ar": "غرفة خاصة", "amenity_type": "Seating", "zone": "Private", "show_on_website": 1},
		{"amenity_name": "Parking", "amenity_name_ar": "موقف سيارات", "amenity_type": "Other", "show_on_website": 1},
		{"amenity_name": "Power Outlets", "amenity_name_ar": "مقابس كهرباء", "amenity_type": "Power", "power_outlets_count": 12, "show_on_website": 1},
	]
	for a in amenities:
		if not frappe.db.exists("Cafe Amenity", a["amenity_name"]):
			doc = frappe.new_doc("Cafe Amenity")
			doc.update(a)
			doc.insert(ignore_permissions=True)
	print("  → Café Amenities seeded")


# ── B9: Competitors ───────────────────────────────────────────────────
def seed_competitors():
	competitors = [
		{
			"competitor_name": "La Dolce Vita",
			"cuisine_type": "Italian",
			"location": "Zamalek",
			"price_range": "$$$",
			"google_rating": 4.5,
			"threat_level": "High",
		},
		{
			"competitor_name": "Pasta House",
			"cuisine_type": "Italian",
			"location": "Maadi",
			"price_range": "$$$",
			"google_rating": 4.2,
			"threat_level": "Medium",
		},
		{
			"competitor_name": "Trattoria",
			"cuisine_type": "Italian",
			"location": "Heliopolis",
			"price_range": "$$$",
			"google_rating": 4.0,
			"threat_level": "Low",
		},
	]
	for c in competitors:
		if not frappe.db.exists("Competitor", {"competitor_name": c["competitor_name"]}):
			doc = frappe.new_doc("Competitor")
			doc.update(c)
			doc.insert(ignore_permissions=True)
	print("  → Competitors seeded")
