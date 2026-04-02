import frappe
from frappe.utils import flt
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Warehouses", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "المستودعات" if lang == "ar" else "Warehouses"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Warehouses
	context.warehouses = frappe.get_all(
		"Candela Warehouse",
		fields=["name", "warehouse_name", "warehouse_type", "is_active", "manager"],
		order_by="warehouse_name asc",
	)

	# Stock Transfers
	context.transfers = frappe.get_all(
		"Stock Transfer",
		fields=["name", "transfer_date", "from_warehouse", "to_warehouse",
		        "status", "transferred_by", "creation"],
		order_by="creation desc",
		limit=20,
	)

	# Stock Reconciliations
	context.reconciliations = frappe.get_all(
		"Stock Reconciliation",
		fields=["name", "reconciliation_date", "warehouse", "status",
		        "total_variance_cost", "counted_by", "creation"],
		order_by="creation desc",
		limit=20,
	)

	# Stats
	context.stats = {
		"total_warehouses": len(context.warehouses),
		"active_warehouses": len([w for w in context.warehouses if w.is_active]),
		"pending_transfers": frappe.db.count("Stock Transfer", {"status": "Draft"}),
		"pending_reconciliations": frappe.db.count("Stock Reconciliation", {"status": "Draft"}),
	}

	# Stock levels by warehouse
	warehouse_stock = {}
	for w in context.warehouses:
		entries_in = frappe.db.sql("""
			SELECT COALESCE(SUM(quantity), 0) FROM `tabStock Entry`
			WHERE warehouse = %s AND entry_type IN ('Purchase','Adjustment','Transfer In')
		""", w.name)[0][0]
		entries_out = frappe.db.sql("""
			SELECT COALESCE(SUM(quantity), 0) FROM `tabStock Entry`
			WHERE warehouse = %s AND entry_type IN ('Consumption','Waste','Transfer Out')
		""", w.name)[0][0]
		warehouse_stock[w.name] = flt(entries_in) - flt(entries_out)
	context.warehouse_stock = warehouse_stock
