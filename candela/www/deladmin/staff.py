import frappe
from frappe.utils import today
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Staff Management", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "إدارة الموظفين" if lang == "ar" else "Staff Management"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Today's shifts
	context.today_shifts = frappe.get_all(
		"Staff Shift",
		filters={"shift_date": today()},
		fields=["name", "staff_name", "role", "start_time", "end_time", "section", "assigned_tables", "status"],
		order_by="start_time asc",
	)

	# Group by role
	roles = {}
	for s in context.today_shifts:
		r = s.get("role") or "Other"
		roles.setdefault(r, []).append(s)
	context.shift_roles = roles

	# Stats
	context.active_count = sum(1 for s in context.today_shifts if s.status == "Active")
	context.scheduled_count = sum(1 for s in context.today_shifts if s.status == "Scheduled")
