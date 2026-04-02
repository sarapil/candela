import frappe
from frappe.utils import flt
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Production", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "الإنتاج" if lang == "ar" else "Production"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Kitchen Stations
	context.stations = frappe.get_all(
		"Kitchen Station",
		fields=["name", "station_name", "station_type", "is_active"],
		order_by="station_name asc",
	)

	# Production Logs (recent)
	context.production_logs = frappe.get_all(
		"Production Log",
		fields=["name", "menu_item", "kitchen_station", "assigned_to", "quantity",
		        "quality_check", "started_at", "completed_at", "total_waste_cost", "creation"],
		order_by="creation desc",
		limit=25,
	)

	# Stats
	total_waste = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(total_waste_cost), 0) FROM `tabProduction Log`
		WHERE MONTH(creation) = MONTH(CURDATE()) AND YEAR(creation) = YEAR(CURDATE())
	""")[0][0])

	total_produced = frappe.db.sql("""
		SELECT COALESCE(SUM(quantity), 0) FROM `tabProduction Log`
		WHERE MONTH(creation) = MONTH(CURDATE()) AND YEAR(creation) = YEAR(CURDATE())
	""")[0][0] or 0

	context.stats = {
		"active_stations": len([s for s in context.stations if s.is_active]),
		"total_stations": len(context.stations),
		"today_logs": frappe.db.count("Production Log", {
			"creation": [">=", frappe.utils.today()]
		}),
		"month_waste_cost": total_waste,
		"month_produced": int(total_produced),
	}
