import frappe
from frappe.utils import flt, today
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Shifts", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "الورديات" if lang == "ar" else "POS Shifts"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# POS Shifts
	context.shifts = frappe.get_all(
		"POS Shift",
		fields=["name", "cashier", "shift_date", "shift_type", "opening_time", "closing_time",
		        "status", "opening_cash", "closing_cash", "total_sales",
		        "total_cash_sales", "total_card_sales", "expected_cash", "cash_variance"],
		order_by="creation desc",
		limit=25,
	)

	# Today's active shift
	context.active_shift = frappe.db.get_value(
		"POS Shift",
		{"status": "Open", "shift_date": today()},
		["name", "cashier", "opening_time", "opening_cash", "total_sales"],
		as_dict=True,
	)

	# Stats
	today_sales = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(total_sales), 0) FROM `tabPOS Shift`
		WHERE shift_date = CURDATE() AND status = 'Closed'
	""")[0][0])

	month_sales = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(total_sales), 0) FROM `tabPOS Shift`
		WHERE MONTH(shift_date) = MONTH(CURDATE()) AND YEAR(shift_date) = YEAR(CURDATE())
		AND status = 'Closed'
	""")[0][0])

	total_variance = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(cash_variance), 0) FROM `tabPOS Shift`
		WHERE MONTH(shift_date) = MONTH(CURDATE()) AND YEAR(shift_date) = YEAR(CURDATE())
		AND status = 'Closed'
	""")[0][0])

	context.stats = {
		"today_sales": today_sales,
		"month_sales": month_sales,
		"total_variance": total_variance,
		"shifts_today": frappe.db.count("POS Shift", {"shift_date": today()}),
	}
