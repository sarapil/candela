"""
Generate all Candela supplement DocTypes.
Run: bench execute candela.generate_doctypes.generate_all
Or run directly with Python.
"""
import json
import os

BASE = "/workspace/development/frappe-bench/apps/candela/candela/candela/doctype"

PERMS_FULL = [
    {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "System Manager", "share": 1, "write": 1},
    {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "Candela Manager", "share": 1, "write": 1},
]

PERMS_STAFF = PERMS_FULL + [{"create": 1, "read": 1, "write": 1, "role": "Candela Staff"}]

PERMS_READONLY = PERMS_FULL + [{"read": 1, "role": "Candela Staff"}]


def make_doctype(name, fields, *, istable=False, issingle=False, naming=None, autoname=None,
                 permissions=None, sort_field="creation", sort_order="DESC",
                 naming_rule=None, track_changes=1):
    folder = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
    path = os.path.join(BASE, folder)
    os.makedirs(path, exist_ok=True)

    field_order = [f["fieldname"] for f in fields]
    dt = {
        "actions": [],
        "creation": "2026-03-19 12:00:00.000000",
        "doctype": "DocType",
        "engine": "InnoDB",
        "field_order": field_order,
        "fields": fields,
        "index_web_pages_for_search": 0,
        "issingle": 1 if issingle else 0,
        "istable": 1 if istable else 0,
        "links": [],
        "modified": "2026-03-19 12:00:00.000000",
        "modified_by": "Administrator",
        "module": "Candela",
        "name": name,
        "owner": "Administrator",
        "permissions": [] if istable else (permissions or PERMS_FULL),
        "sort_field": sort_field,
        "sort_order": sort_order,
        "states": [],
        "track_changes": track_changes,
    }
    if autoname:
        dt["autoname"] = autoname
    if naming_rule:
        dt["naming_rule"] = naming_rule
    elif autoname and "naming_series" in autoname:
        dt["naming_rule"] = 'By "Naming Series" field'
    elif autoname and "field:" in autoname:
        dt["naming_rule"] = "By fieldname"

    json_path = os.path.join(path, f"{folder}.json")
    with open(json_path, "w") as f:
        json.dump(dt, f, indent=2)

    py_path = os.path.join(path, f"{folder}.py")
    if not os.path.exists(py_path):
        cls_name = name.replace(" ", "").replace("(", "").replace(")", "")
        with open(py_path, "w") as f:
            f.write(f"""# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class {cls_name}(Document):
\tpass
""")

    init_path = os.path.join(path, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("")

    print(f"  ✅ {name} → {folder}/")


def ns(series):
    return {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": series, "default": series, "hidden": 1}


def generate_all():
    print("\n🕯️ Generating Candela Supplement DocTypes...\n")

    # ═══════════════════════════════════════════
    # A2: SUPPLIER
    # ═══════════════════════════════════════════
    make_doctype("Candela Supplier", [
        {"fieldname": "supplier_name", "fieldtype": "Data", "label": "Supplier Name", "reqd": 1, "unique": 1, "in_list_view": 1},
        {"fieldname": "supplier_name_ar", "fieldtype": "Data", "label": "Supplier Name (Arabic)"},
        {"fieldname": "contact_person", "fieldtype": "Data", "label": "Contact Person"},
        {"fieldname": "phone", "fieldtype": "Data", "label": "Phone", "in_list_view": 1},
        {"fieldname": "email", "fieldtype": "Data", "label": "Email", "options": "Email"},
        {"fieldname": "address", "fieldtype": "Small Text", "label": "Address"},
        {"fieldname": "sb_terms", "fieldtype": "Section Break", "label": "Terms"},
        {"fieldname": "payment_terms", "fieldtype": "Select", "label": "Payment Terms", "options": "Cash\nCredit 7 Days\nCredit 15 Days\nCredit 30 Days", "default": "Cash"},
        {"fieldname": "tax_id", "fieldtype": "Data", "label": "Tax ID"},
        {"fieldname": "cb_sup1", "fieldtype": "Column Break"},
        {"fieldname": "category", "fieldtype": "Select", "label": "Category", "options": "Produce\nMeat & Poultry\nSeafood\nDairy\nBakery\nBeverages\nDry Goods\nEquipment\nCleaning\nOther", "in_standard_filter": 1},
        {"fieldname": "rating", "fieldtype": "Rating", "label": "Rating"},
        {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
        {"fieldname": "sb_notes", "fieldtype": "Section Break"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="field:supplier_name")

    # ═══════════════════════════════════════════
    # A2: PURCHASE REQUEST + CHILD
    # ═══════════════════════════════════════════
    make_doctype("Purchase Request Item", [
        {"fieldname": "ingredient", "fieldtype": "Link", "label": "Ingredient", "options": "Ingredient", "reqd": 1, "in_list_view": 1},
        {"fieldname": "ingredient_name", "fieldtype": "Data", "label": "Name", "fetch_from": "ingredient.ingredient_name", "read_only": 1, "in_list_view": 1},
        {"fieldname": "requested_qty", "fieldtype": "Float", "label": "Requested Qty", "reqd": 1, "in_list_view": 1},
        {"fieldname": "unit", "fieldtype": "Data", "label": "Unit", "fetch_from": "ingredient.unit", "read_only": 1, "in_list_view": 1},
        {"fieldname": "current_stock", "fieldtype": "Float", "label": "Current Stock", "fetch_from": "ingredient.current_stock", "read_only": 1},
        {"fieldname": "reorder_level", "fieldtype": "Float", "label": "Reorder Level", "fetch_from": "ingredient.minimum_stock", "read_only": 1},
        {"fieldname": "estimated_cost", "fieldtype": "Currency", "label": "Est. Cost", "in_list_view": 1},
        {"fieldname": "reason", "fieldtype": "Data", "label": "Reason"},
    ], istable=True)

    make_doctype("Purchase Request", [
        ns("CPR-.YYYY.-.#####"),
        {"fieldname": "request_date", "fieldtype": "Date", "label": "Request Date", "reqd": 1, "default": "Today", "in_list_view": 1},
        {"fieldname": "requested_by", "fieldtype": "Link", "label": "Requested By", "options": "User", "default": "__user"},
        {"fieldname": "cb_pr1", "fieldtype": "Column Break"},
        {"fieldname": "urgency", "fieldtype": "Select", "label": "Urgency", "options": "Normal\nUrgent\nCritical", "default": "Normal", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nSubmitted\nApproved\nOrdered\nReceived\nRejected", "default": "Draft", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_items", "fieldtype": "Section Break", "label": "Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Request Items", "options": "Purchase Request Item", "reqd": 1},
        {"fieldname": "sb_totals", "fieldtype": "Section Break", "label": "Totals & Approval"},
        {"fieldname": "total_estimated_cost", "fieldtype": "Currency", "label": "Total Estimated Cost", "read_only": 1},
        {"fieldname": "cb_pr2", "fieldtype": "Column Break"},
        {"fieldname": "approved_by", "fieldtype": "Link", "label": "Approved By", "options": "User", "depends_on": "eval:doc.status=='Approved'"},
        {"fieldname": "approved_date", "fieldtype": "Datetime", "label": "Approved Date", "depends_on": "eval:doc.status=='Approved'"},
        {"fieldname": "sb_ref", "fieldtype": "Section Break"},
        {"fieldname": "supplier", "fieldtype": "Link", "label": "Supplier", "options": "Candela Supplier"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", permissions=PERMS_STAFF)

    # ═══════════════════════════════════════════
    # A2: PURCHASE ORDER + CHILD
    # ═══════════════════════════════════════════
    make_doctype("Purchase Order Item", [
        {"fieldname": "ingredient", "fieldtype": "Link", "label": "Ingredient", "options": "Ingredient", "reqd": 1, "in_list_view": 1},
        {"fieldname": "ingredient_name", "fieldtype": "Data", "label": "Name", "fetch_from": "ingredient.ingredient_name", "read_only": 1, "in_list_view": 1},
        {"fieldname": "ordered_qty", "fieldtype": "Float", "label": "Ordered Qty", "reqd": 1, "in_list_view": 1},
        {"fieldname": "unit", "fieldtype": "Data", "label": "Unit", "fetch_from": "ingredient.unit", "read_only": 1},
        {"fieldname": "unit_cost", "fieldtype": "Currency", "label": "Unit Cost", "reqd": 1, "in_list_view": 1},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "read_only": 1, "in_list_view": 1},
    ], istable=True)

    make_doctype("Purchase Order", [
        ns("CPO-.YYYY.-.#####"),
        {"fieldname": "purchase_request", "fieldtype": "Link", "label": "Purchase Request", "options": "Purchase Request"},
        {"fieldname": "supplier", "fieldtype": "Link", "label": "Supplier", "options": "Candela Supplier", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "order_date", "fieldtype": "Date", "label": "Order Date", "reqd": 1, "default": "Today", "in_list_view": 1},
        {"fieldname": "cb_po1", "fieldtype": "Column Break"},
        {"fieldname": "expected_delivery", "fieldtype": "Date", "label": "Expected Delivery"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nSent\nPartially Received\nReceived\nCancelled", "default": "Draft", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_items", "fieldtype": "Section Break", "label": "Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Order Items", "options": "Purchase Order Item", "reqd": 1},
        {"fieldname": "sb_totals", "fieldtype": "Section Break", "label": "Totals"},
        {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Total Amount", "read_only": 1, "in_list_view": 1},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:")

    # ═══════════════════════════════════════════
    # A2: GRN (GOODS RECEIPT NOTE) + CHILD
    # ═══════════════════════════════════════════
    make_doctype("GRN Item", [
        {"fieldname": "ingredient", "fieldtype": "Link", "label": "Ingredient", "options": "Ingredient", "reqd": 1, "in_list_view": 1},
        {"fieldname": "ingredient_name", "fieldtype": "Data", "label": "Name", "fetch_from": "ingredient.ingredient_name", "read_only": 1},
        {"fieldname": "ordered_qty", "fieldtype": "Float", "label": "Ordered Qty", "read_only": 1, "in_list_view": 1},
        {"fieldname": "received_qty", "fieldtype": "Float", "label": "Received Qty", "reqd": 1, "in_list_view": 1},
        {"fieldname": "accepted_qty", "fieldtype": "Float", "label": "Accepted Qty", "in_list_view": 1},
        {"fieldname": "rejected_qty", "fieldtype": "Float", "label": "Rejected Qty"},
        {"fieldname": "rejection_reason", "fieldtype": "Data", "label": "Rejection Reason", "depends_on": "eval:doc.rejected_qty > 0"},
        {"fieldname": "batch_no", "fieldtype": "Data", "label": "Batch No"},
        {"fieldname": "expiry_date", "fieldtype": "Date", "label": "Expiry Date"},
        {"fieldname": "unit_cost", "fieldtype": "Currency", "label": "Unit Cost", "in_list_view": 1},
    ], istable=True)

    make_doctype("Goods Receipt Note", [
        ns("CGRN-.YYYY.-.#####"),
        {"fieldname": "purchase_order", "fieldtype": "Link", "label": "Purchase Order", "options": "Purchase Order", "in_list_view": 1},
        {"fieldname": "supplier", "fieldtype": "Link", "label": "Supplier", "options": "Candela Supplier", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "receipt_date", "fieldtype": "Date", "label": "Receipt Date", "reqd": 1, "default": "Today", "in_list_view": 1},
        {"fieldname": "cb_grn1", "fieldtype": "Column Break"},
        {"fieldname": "received_by", "fieldtype": "Link", "label": "Received By", "options": "User", "default": "__user"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nReceived\nInspected\nStocked\nDisputed", "default": "Draft", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_items", "fieldtype": "Section Break", "label": "Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "GRN Items", "options": "GRN Item", "reqd": 1},
        {"fieldname": "sb_inspection", "fieldtype": "Section Break", "label": "Inspection"},
        {"fieldname": "inspection_status", "fieldtype": "Select", "label": "Inspection Status", "options": "Pending\nPassed\nPartial\nFailed", "default": "Pending"},
        {"fieldname": "inspector", "fieldtype": "Link", "label": "Inspector", "options": "User"},
        {"fieldname": "cb_grn2", "fieldtype": "Column Break"},
        {"fieldname": "inspection_date", "fieldtype": "Datetime", "label": "Inspection Date"},
        {"fieldname": "inspection_notes", "fieldtype": "Small Text", "label": "Inspection Notes"},
        {"fieldname": "sb_totals", "fieldtype": "Section Break", "label": "Totals"},
        {"fieldname": "total_cost", "fieldtype": "Currency", "label": "Total Cost", "read_only": 1},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", permissions=PERMS_STAFF)

    # ═══════════════════════════════════════════
    # A3: WAREHOUSE
    # ═══════════════════════════════════════════
    make_doctype("Candela Warehouse", [
        {"fieldname": "warehouse_name", "fieldtype": "Data", "label": "Warehouse Name", "reqd": 1, "unique": 1, "in_list_view": 1},
        {"fieldname": "warehouse_name_ar", "fieldtype": "Data", "label": "Warehouse Name (Arabic)"},
        {"fieldname": "warehouse_type", "fieldtype": "Select", "label": "Type", "options": "Main\nKitchen\nBar\nCold Storage\nDry Storage", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "cb_wh1", "fieldtype": "Column Break"},
        {"fieldname": "manager", "fieldtype": "Link", "label": "Manager", "options": "User"},
        {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="field:warehouse_name")

    # ═══════════════════════════════════════════
    # A3: STOCK TRANSFER + CHILD
    # ═══════════════════════════════════════════
    make_doctype("Stock Transfer Item", [
        {"fieldname": "ingredient", "fieldtype": "Link", "label": "Ingredient", "options": "Ingredient", "reqd": 1, "in_list_view": 1},
        {"fieldname": "ingredient_name", "fieldtype": "Data", "label": "Name", "fetch_from": "ingredient.ingredient_name", "read_only": 1, "in_list_view": 1},
        {"fieldname": "quantity", "fieldtype": "Float", "label": "Quantity", "reqd": 1, "in_list_view": 1},
        {"fieldname": "unit", "fieldtype": "Data", "label": "Unit", "fetch_from": "ingredient.unit", "read_only": 1, "in_list_view": 1},
        {"fieldname": "batch_no", "fieldtype": "Data", "label": "Batch No"},
    ], istable=True)

    make_doctype("Stock Transfer", [
        ns("CSTX-.YYYY.-.#####"),
        {"fieldname": "from_warehouse", "fieldtype": "Link", "label": "From Warehouse", "options": "Candela Warehouse", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "to_warehouse", "fieldtype": "Link", "label": "To Warehouse", "options": "Candela Warehouse", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "transfer_date", "fieldtype": "Datetime", "label": "Transfer Date", "reqd": 1, "default": "Now", "in_list_view": 1},
        {"fieldname": "cb_st1", "fieldtype": "Column Break"},
        {"fieldname": "transferred_by", "fieldtype": "Link", "label": "Transferred By", "options": "User", "default": "__user"},
        {"fieldname": "reason", "fieldtype": "Select", "label": "Reason", "options": "Daily Prep\nEvent Prep\nRestock\nEmergency", "default": "Daily Prep"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nSubmitted\nReceived\nCancelled", "default": "Draft", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_items", "fieldtype": "Section Break", "label": "Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Transfer Items", "options": "Stock Transfer Item", "reqd": 1},
        {"fieldname": "sb_recv", "fieldtype": "Section Break", "label": "Receipt"},
        {"fieldname": "received_by", "fieldtype": "Link", "label": "Received By", "options": "User"},
        {"fieldname": "received_at", "fieldtype": "Datetime", "label": "Received At"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="naming_series:", permissions=PERMS_STAFF)

    # ═══════════════════════════════════════════
    # A5: STOCK RECONCILIATION + CHILD
    # ═══════════════════════════════════════════
    make_doctype("Reconciliation Item", [
        {"fieldname": "ingredient", "fieldtype": "Link", "label": "Ingredient", "options": "Ingredient", "reqd": 1, "in_list_view": 1},
        {"fieldname": "ingredient_name", "fieldtype": "Data", "label": "Name", "fetch_from": "ingredient.ingredient_name", "read_only": 1},
        {"fieldname": "system_qty", "fieldtype": "Float", "label": "System Qty", "fetch_from": "ingredient.current_stock", "read_only": 1, "in_list_view": 1},
        {"fieldname": "counted_qty", "fieldtype": "Float", "label": "Counted Qty", "reqd": 1, "in_list_view": 1},
        {"fieldname": "variance", "fieldtype": "Float", "label": "Variance", "read_only": 1, "in_list_view": 1},
        {"fieldname": "variance_pct", "fieldtype": "Percent", "label": "Variance %", "read_only": 1},
        {"fieldname": "variance_cost", "fieldtype": "Currency", "label": "Variance Cost", "read_only": 1},
        {"fieldname": "reason", "fieldtype": "Select", "label": "Reason", "options": "\nTheft\nSpoilage\nMeasurement Error\nOther"},
        {"fieldname": "notes", "fieldtype": "Data", "label": "Notes"},
    ], istable=True)

    make_doctype("Stock Reconciliation", [
        ns("CREC-.YYYY.-.#####"),
        {"fieldname": "reconciliation_date", "fieldtype": "Date", "label": "Date", "reqd": 1, "default": "Today", "in_list_view": 1},
        {"fieldname": "warehouse", "fieldtype": "Link", "label": "Warehouse", "options": "Candela Warehouse", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "counted_by", "fieldtype": "Link", "label": "Counted By", "options": "User", "default": "__user"},
        {"fieldname": "cb_rec1", "fieldtype": "Column Break"},
        {"fieldname": "verified_by", "fieldtype": "Link", "label": "Verified By", "options": "User"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nCounting\nReviewed\nAdjusted\nClosed", "default": "Draft", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_items", "fieldtype": "Section Break", "label": "Items"},
        {"fieldname": "items", "fieldtype": "Table", "label": "Reconciliation Items", "options": "Reconciliation Item", "reqd": 1},
        {"fieldname": "sb_totals", "fieldtype": "Section Break", "label": "Totals"},
        {"fieldname": "total_variance_cost", "fieldtype": "Currency", "label": "Total Variance Cost", "read_only": 1},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:")

    # ═══════════════════════════════════════════
    # A6: KITCHEN STATION + PRODUCTION LOG + WASTE
    # ═══════════════════════════════════════════
    make_doctype("Kitchen Station", [
        {"fieldname": "station_name", "fieldtype": "Data", "label": "Station Name", "reqd": 1, "unique": 1, "in_list_view": 1},
        {"fieldname": "station_name_ar", "fieldtype": "Data", "label": "Station Name (Arabic)"},
        {"fieldname": "station_type", "fieldtype": "Select", "label": "Type", "options": "Hot Line\nCold Line\nPasta\nPizza\nGrill\nDessert\nBar\nPrep", "in_list_view": 1},
        {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
    ], autoname="field:station_name")

    make_doctype("Production Waste", [
        {"fieldname": "ingredient", "fieldtype": "Link", "label": "Ingredient", "options": "Ingredient", "reqd": 1, "in_list_view": 1},
        {"fieldname": "wasted_qty", "fieldtype": "Float", "label": "Wasted Qty", "reqd": 1, "in_list_view": 1},
        {"fieldname": "unit", "fieldtype": "Data", "label": "Unit", "fetch_from": "ingredient.unit", "read_only": 1},
        {"fieldname": "reason", "fieldtype": "Select", "label": "Reason", "options": "Over-prep\nBurnt\nDropped\nExpired\nQuality", "in_list_view": 1},
        {"fieldname": "cost", "fieldtype": "Currency", "label": "Cost", "read_only": 1, "in_list_view": 1},
    ], istable=True)

    make_doctype("Production Log", [
        ns("CPROD-.YYYY.-.#####"),
        {"fieldname": "order_reference_type", "fieldtype": "Select", "label": "Order Type", "options": "\nOnline Order\nPOS Invoice", "in_standard_filter": 1},
        {"fieldname": "order_reference", "fieldtype": "Dynamic Link", "label": "Order Reference", "options": "order_reference_type"},
        {"fieldname": "menu_item", "fieldtype": "Link", "label": "Menu Item", "options": "Menu Item", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "quantity", "fieldtype": "Int", "label": "Quantity", "reqd": 1, "in_list_view": 1},
        {"fieldname": "cb_pl1", "fieldtype": "Column Break"},
        {"fieldname": "kitchen_station", "fieldtype": "Link", "label": "Kitchen Station", "options": "Kitchen Station", "in_standard_filter": 1},
        {"fieldname": "assigned_to", "fieldtype": "Link", "label": "Assigned Chef", "options": "User"},
        {"fieldname": "shift", "fieldtype": "Select", "label": "Shift", "options": "Morning\nEvening"},
        {"fieldname": "sb_timing", "fieldtype": "Section Break", "label": "Timing"},
        {"fieldname": "started_at", "fieldtype": "Datetime", "label": "Started At"},
        {"fieldname": "completed_at", "fieldtype": "Datetime", "label": "Completed At"},
        {"fieldname": "prep_time_minutes", "fieldtype": "Float", "label": "Actual Prep Time (min)", "read_only": 1},
        {"fieldname": "cb_pl2", "fieldtype": "Column Break"},
        {"fieldname": "estimated_prep_time", "fieldtype": "Float", "label": "Estimated Prep Time (min)", "fetch_from": "menu_item.preparation_time_min"},
        {"fieldname": "time_variance_pct", "fieldtype": "Percent", "label": "Time Variance %", "read_only": 1},
        {"fieldname": "quality_check", "fieldtype": "Select", "label": "Quality", "options": "\nPass\nFail\nRework"},
        {"fieldname": "sb_waste", "fieldtype": "Section Break", "label": "Waste"},
        {"fieldname": "waste_items", "fieldtype": "Table", "label": "Waste Items", "options": "Production Waste"},
        {"fieldname": "total_waste_cost", "fieldtype": "Currency", "label": "Total Waste Cost", "read_only": 1},
        {"fieldname": "notes", "fieldtype": "Data", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", permissions=PERMS_STAFF)

    # ═══════════════════════════════════════════
    # A7: POS SHIFT
    # ═══════════════════════════════════════════
    make_doctype("POS Shift", [
        ns("CSHIFT-.YYYY.-.#####"),
        {"fieldname": "shift_date", "fieldtype": "Date", "label": "Date", "reqd": 1, "default": "Today", "in_list_view": 1},
        {"fieldname": "shift_type", "fieldtype": "Select", "label": "Shift", "options": "Morning\nEvening\nFull Day", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "cashier", "fieldtype": "Link", "label": "Cashier", "options": "User", "reqd": 1, "default": "__user", "in_list_view": 1},
        {"fieldname": "cb_sh1", "fieldtype": "Column Break"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Open\nClosing\nClosed\nAudited", "default": "Open", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_opening", "fieldtype": "Section Break", "label": "Opening"},
        {"fieldname": "opening_cash", "fieldtype": "Currency", "label": "Opening Cash"},
        {"fieldname": "opening_time", "fieldtype": "Datetime", "label": "Opening Time", "default": "Now"},
        {"fieldname": "sb_trans", "fieldtype": "Section Break", "label": "Transactions"},
        {"fieldname": "total_cash_sales", "fieldtype": "Currency", "label": "Total Cash Sales", "read_only": 1},
        {"fieldname": "total_card_sales", "fieldtype": "Currency", "label": "Total Card Sales", "read_only": 1},
        {"fieldname": "total_wallet_sales", "fieldtype": "Currency", "label": "Total Wallet Sales", "read_only": 1},
        {"fieldname": "cb_sh2", "fieldtype": "Column Break"},
        {"fieldname": "total_sales", "fieldtype": "Currency", "label": "Total Sales", "read_only": 1, "bold": 1},
        {"fieldname": "total_refunds", "fieldtype": "Currency", "label": "Total Refunds", "read_only": 1},
        {"fieldname": "total_discounts", "fieldtype": "Currency", "label": "Total Discounts", "read_only": 1},
        {"fieldname": "orders_count", "fieldtype": "Int", "label": "Orders Count", "read_only": 1},
        {"fieldname": "sb_closing", "fieldtype": "Section Break", "label": "Closing"},
        {"fieldname": "closing_cash", "fieldtype": "Currency", "label": "Closing Cash"},
        {"fieldname": "closing_time", "fieldtype": "Datetime", "label": "Closing Time"},
        {"fieldname": "cb_sh3", "fieldtype": "Column Break"},
        {"fieldname": "expected_cash", "fieldtype": "Currency", "label": "Expected Cash", "read_only": 1},
        {"fieldname": "cash_variance", "fieldtype": "Currency", "label": "Cash Variance", "read_only": 1},
        {"fieldname": "variance_reason", "fieldtype": "Small Text", "label": "Variance Reason", "depends_on": "eval:doc.cash_variance != 0"},
        {"fieldname": "sb_audit", "fieldtype": "Section Break", "label": "Audit"},
        {"fieldname": "audited_by", "fieldtype": "Link", "label": "Audited By", "options": "User"},
        {"fieldname": "audit_notes", "fieldtype": "Small Text", "label": "Audit Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", permissions=PERMS_STAFF)

    # ═══════════════════════════════════════════
    # A8: DAILY CLOSING + CHILD
    # ═══════════════════════════════════════════
    make_doctype("Daily Expense", [
        {"fieldname": "description", "fieldtype": "Data", "label": "Description", "reqd": 1, "in_list_view": 1},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "reqd": 1, "in_list_view": 1},
        {"fieldname": "category", "fieldtype": "Select", "label": "Category", "options": "Supplies\nMaintenance\nUtilities\nTransport\nOther", "in_list_view": 1},
        {"fieldname": "receipt_attached", "fieldtype": "Check", "label": "Receipt?", "in_list_view": 1},
    ], istable=True)

    make_doctype("Daily Closing", [
        ns("CDC-.YYYY.-.#####"),
        {"fieldname": "closing_date", "fieldtype": "Date", "label": "Date", "reqd": 1, "default": "Today", "in_list_view": 1, "unique": 1},
        {"fieldname": "prepared_by", "fieldtype": "Link", "label": "Prepared By", "options": "User", "default": "__user"},
        {"fieldname": "cb_dc1", "fieldtype": "Column Break"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nReviewed\nApproved\nLocked", "default": "Draft", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "approved_by", "fieldtype": "Link", "label": "Approved By", "options": "User"},
        {"fieldname": "sb_revenue", "fieldtype": "Section Break", "label": "Revenue"},
        {"fieldname": "total_dine_in_revenue", "fieldtype": "Currency", "label": "Dine-in Revenue", "read_only": 1},
        {"fieldname": "total_delivery_revenue", "fieldtype": "Currency", "label": "Delivery Revenue", "read_only": 1},
        {"fieldname": "total_takeaway_revenue", "fieldtype": "Currency", "label": "Takeaway Revenue", "read_only": 1},
        {"fieldname": "cb_dc2", "fieldtype": "Column Break"},
        {"fieldname": "other_income", "fieldtype": "Currency", "label": "Other Income"},
        {"fieldname": "gross_revenue", "fieldtype": "Currency", "label": "Gross Revenue", "read_only": 1, "bold": 1},
        {"fieldname": "sb_collections", "fieldtype": "Section Break", "label": "Collections"},
        {"fieldname": "cash_collected", "fieldtype": "Currency", "label": "Cash Collected", "read_only": 1},
        {"fieldname": "card_collected", "fieldtype": "Currency", "label": "Card Collected", "read_only": 1},
        {"fieldname": "cb_dc3", "fieldtype": "Column Break"},
        {"fieldname": "online_payments", "fieldtype": "Currency", "label": "Online Payments", "read_only": 1},
        {"fieldname": "total_collected", "fieldtype": "Currency", "label": "Total Collected", "read_only": 1, "bold": 1},
        {"fieldname": "collection_variance", "fieldtype": "Currency", "label": "Variance", "read_only": 1},
        {"fieldname": "sb_expenses", "fieldtype": "Section Break", "label": "Cash Expenses"},
        {"fieldname": "cash_expenses", "fieldtype": "Table", "label": "Expenses", "options": "Daily Expense"},
        {"fieldname": "total_expenses", "fieldtype": "Currency", "label": "Total Expenses", "read_only": 1},
        {"fieldname": "sb_cash", "fieldtype": "Section Break", "label": "Cash Position"},
        {"fieldname": "opening_cash", "fieldtype": "Currency", "label": "Opening Cash", "read_only": 1},
        {"fieldname": "closing_cash", "fieldtype": "Currency", "label": "Closing Cash", "read_only": 1},
        {"fieldname": "cb_dc4", "fieldtype": "Column Break"},
        {"fieldname": "net_cash_position", "fieldtype": "Currency", "label": "Net Cash Position", "read_only": 1},
        {"fieldname": "bank_deposit_amount", "fieldtype": "Currency", "label": "Bank Deposit"},
        {"fieldname": "sb_kpis", "fieldtype": "Section Break", "label": "KPIs"},
        {"fieldname": "total_orders", "fieldtype": "Int", "label": "Total Orders", "read_only": 1},
        {"fieldname": "average_order_value", "fieldtype": "Currency", "label": "Avg Order Value", "read_only": 1},
        {"fieldname": "cb_dc5", "fieldtype": "Column Break"},
        {"fieldname": "food_cost_today", "fieldtype": "Currency", "label": "Food Cost Today", "read_only": 1},
        {"fieldname": "food_cost_percentage", "fieldtype": "Percent", "label": "Food Cost %", "read_only": 1},
        {"fieldname": "covers_count", "fieldtype": "Int", "label": "Covers (Guests)"},
        {"fieldname": "revenue_per_cover", "fieldtype": "Currency", "label": "Revenue/Cover", "read_only": 1},
        {"fieldname": "sb_notes_dc", "fieldtype": "Section Break"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:")

    # ═══════════════════════════════════════════
    # A9: PRICE CHANGE LOG
    # ═══════════════════════════════════════════
    make_doctype("Price Change Log", [
        {"fieldname": "menu_item", "fieldtype": "Link", "label": "Menu Item", "options": "Menu Item", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "old_price", "fieldtype": "Currency", "label": "Old Price", "in_list_view": 1},
        {"fieldname": "new_price", "fieldtype": "Currency", "label": "New Price", "in_list_view": 1},
        {"fieldname": "cb_pcl1", "fieldtype": "Column Break"},
        {"fieldname": "change_pct", "fieldtype": "Percent", "label": "Change %", "read_only": 1},
        {"fieldname": "changed_by", "fieldtype": "Link", "label": "Changed By", "options": "User", "in_list_view": 1},
        {"fieldname": "changed_at", "fieldtype": "Datetime", "label": "Changed At", "in_list_view": 1},
        {"fieldname": "reason", "fieldtype": "Data", "label": "Reason"},
    ], autoname="naming_series:", naming_rule='By "Naming Series" field',
       permissions=[
           {"read": 1, "role": "System Manager"},
           {"read": 1, "role": "Candela Manager"},
       ])

    # ═══════════════════════════════════════════
    # A11: RESTAURANT ASSET + MAINTENANCE REQUEST
    # ═══════════════════════════════════════════
    make_doctype("Restaurant Asset", [
        {"fieldname": "asset_name", "fieldtype": "Data", "label": "Asset Name", "reqd": 1, "in_list_view": 1},
        {"fieldname": "asset_code", "fieldtype": "Data", "label": "Asset Code", "unique": 1},
        {"fieldname": "category", "fieldtype": "Select", "label": "Category", "options": "Kitchen Equipment\nRefrigeration\nFurniture\nHVAC\nPOS Hardware\nLighting\nPlumbing\nOther", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "cb_ra1", "fieldtype": "Column Break"},
        {"fieldname": "brand_model", "fieldtype": "Data", "label": "Brand / Model"},
        {"fieldname": "serial_number", "fieldtype": "Data", "label": "Serial Number"},
        {"fieldname": "location", "fieldtype": "Select", "label": "Location", "options": "Kitchen\nBar\nDining\nStorage\nOffice", "in_standard_filter": 1},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Active\nUnder Maintenance\nDecommissioned", "default": "Active", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_purchase", "fieldtype": "Section Break", "label": "Purchase & Warranty"},
        {"fieldname": "purchase_date", "fieldtype": "Date", "label": "Purchase Date"},
        {"fieldname": "purchase_cost", "fieldtype": "Currency", "label": "Purchase Cost"},
        {"fieldname": "warranty_until", "fieldtype": "Date", "label": "Warranty Until"},
        {"fieldname": "cb_ra2", "fieldtype": "Column Break"},
        {"fieldname": "useful_life_years", "fieldtype": "Int", "label": "Useful Life (Years)"},
        {"fieldname": "current_value", "fieldtype": "Currency", "label": "Current Value", "read_only": 1},
        {"fieldname": "sb_maintenance", "fieldtype": "Section Break", "label": "Maintenance"},
        {"fieldname": "maintenance_interval_days", "fieldtype": "Int", "label": "Maint. Interval (Days)", "default": "90"},
        {"fieldname": "next_maintenance_date", "fieldtype": "Date", "label": "Next Maintenance"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", naming_rule='By "Naming Series" field')

    make_doctype("Maintenance Request", [
        ns("CMNT-.YYYY.-.#####"),
        {"fieldname": "asset", "fieldtype": "Link", "label": "Asset", "options": "Restaurant Asset", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "reported_by", "fieldtype": "Link", "label": "Reported By", "options": "User", "default": "__user"},
        {"fieldname": "reported_at", "fieldtype": "Datetime", "label": "Reported At", "default": "Now"},
        {"fieldname": "cb_mr1", "fieldtype": "Column Break"},
        {"fieldname": "issue_type", "fieldtype": "Select", "label": "Issue Type", "options": "Breakdown\nPreventive\nInspection", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "priority", "fieldtype": "Select", "label": "Priority", "options": "Low\nMedium\nHigh\nCritical", "default": "Medium", "in_list_view": 1},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Reported\nAssigned\nIn Progress\nCompleted\nClosed", "default": "Reported", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_details", "fieldtype": "Section Break", "label": "Details"},
        {"fieldname": "description", "fieldtype": "Text", "label": "Description"},
        {"fieldname": "assigned_to", "fieldtype": "Data", "label": "Assigned To (Technician)"},
        {"fieldname": "sb_resolution", "fieldtype": "Section Break", "label": "Resolution"},
        {"fieldname": "started_at", "fieldtype": "Datetime", "label": "Started At"},
        {"fieldname": "completed_at", "fieldtype": "Datetime", "label": "Completed At"},
        {"fieldname": "downtime_hours", "fieldtype": "Float", "label": "Downtime (Hours)", "read_only": 1},
        {"fieldname": "cb_mr2", "fieldtype": "Column Break"},
        {"fieldname": "repair_cost", "fieldtype": "Currency", "label": "Repair Cost"},
        {"fieldname": "parts_used", "fieldtype": "Small Text", "label": "Parts Used"},
        {"fieldname": "resolution_notes", "fieldtype": "Small Text", "label": "Resolution Notes"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", permissions=PERMS_STAFF)

    # ═══════════════════════════════════════════
    # B1: CUSTOMER PERSONA
    # ═══════════════════════════════════════════
    make_doctype("Customer Persona", [
        {"fieldname": "persona_name_ar", "fieldtype": "Data", "label": "Persona Name (Arabic)", "reqd": 1, "in_list_view": 1},
        {"fieldname": "persona_name_en", "fieldtype": "Data", "label": "Persona Name (English)", "reqd": 1, "in_list_view": 1},
        {"fieldname": "persona_code", "fieldtype": "Data", "label": "Code", "unique": 1, "reqd": 1},
        {"fieldname": "avatar_image", "fieldtype": "Attach Image", "label": "Avatar"},
        {"fieldname": "sb_demo", "fieldtype": "Section Break", "label": "Demographics"},
        {"fieldname": "age_range", "fieldtype": "Data", "label": "Age Range"},
        {"fieldname": "occupation", "fieldtype": "Data", "label": "Occupation"},
        {"fieldname": "income_level", "fieldtype": "Select", "label": "Income Level", "options": "Low\nMedium\nMedium-High\nHigh", "in_list_view": 1},
        {"fieldname": "cb_cp1", "fieldtype": "Column Break"},
        {"fieldname": "location_notes", "fieldtype": "Data", "label": "Location Notes"},
        {"fieldname": "price_sensitivity", "fieldtype": "Select", "label": "Price Sensitivity", "options": "Low\nMedium\nHigh"},
        {"fieldname": "sb_behavior", "fieldtype": "Section Break", "label": "Behavior"},
        {"fieldname": "visit_pattern", "fieldtype": "Data", "label": "Visit Pattern"},
        {"fieldname": "preferred_channels", "fieldtype": "Small Text", "label": "Preferred Channels"},
        {"fieldname": "preferred_payment", "fieldtype": "Small Text", "label": "Preferred Payment"},
        {"fieldname": "decision_factors", "fieldtype": "Small Text", "label": "Decision Factors"},
        {"fieldname": "sb_marketing", "fieldtype": "Section Break", "label": "Marketing"},
        {"fieldname": "marketing_channels", "fieldtype": "Small Text", "label": "Marketing Channels"},
        {"fieldname": "content_tone", "fieldtype": "Data", "label": "Content Tone"},
        {"fieldname": "offer_types", "fieldtype": "Small Text", "label": "Offer Types"},
        {"fieldname": "sb_menu", "fieldtype": "Section Break", "label": "Menu Preferences"},
        {"fieldname": "preferred_categories", "fieldtype": "Small Text", "label": "Preferred Categories"},
        {"fieldname": "must_have_features", "fieldtype": "Small Text", "label": "Must-Have Features"},
        {"fieldname": "pain_points", "fieldtype": "Small Text", "label": "Pain Points"},
        {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
    ], autoname="field:persona_code")

    # ═══════════════════════════════════════════
    # B2: SERVICE MODE
    # ═══════════════════════════════════════════
    make_doctype("Service Mode", [
        {"fieldname": "mode_name_ar", "fieldtype": "Data", "label": "Mode Name (Arabic)", "reqd": 1, "in_list_view": 1},
        {"fieldname": "mode_name_en", "fieldtype": "Data", "label": "Mode Name (English)", "reqd": 1, "in_list_view": 1},
        {"fieldname": "mode_code", "fieldtype": "Data", "label": "Code", "unique": 1, "reqd": 1},
        {"fieldname": "cb_sm1", "fieldtype": "Column Break"},
        {"fieldname": "active_hours_start", "fieldtype": "Time", "label": "Start Time"},
        {"fieldname": "active_hours_end", "fieldtype": "Time", "label": "End Time"},
        {"fieldname": "active_days", "fieldtype": "Small Text", "label": "Active Days"},
        {"fieldname": "sb_config", "fieldtype": "Section Break", "label": "Configuration"},
        {"fieldname": "target_persona", "fieldtype": "Link", "label": "Target Persona", "options": "Customer Persona"},
        {"fieldname": "featured_categories", "fieldtype": "Small Text", "label": "Featured Categories"},
        {"fieldname": "staff_requirements", "fieldtype": "Small Text", "label": "Staff Requirements"},
        {"fieldname": "cb_sm2", "fieldtype": "Column Break"},
        {"fieldname": "ambiance_settings", "fieldtype": "Small Text", "label": "Ambiance Settings"},
        {"fieldname": "background_music_playlist", "fieldtype": "Data", "label": "Music Playlist URL"},
        {"fieldname": "lighting_preset", "fieldtype": "Select", "label": "Lighting", "options": "Bright\nWarm\nDim\nCandle"},
        {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
    ], autoname="field:mode_code")

    # ═══════════════════════════════════════════
    # B3: INFLUENCER + VISIT CHILD
    # ═══════════════════════════════════════════
    make_doctype("Influencer Visit", [
        {"fieldname": "visit_date", "fieldtype": "Date", "label": "Visit Date", "in_list_view": 1},
        {"fieldname": "purpose", "fieldtype": "Data", "label": "Purpose", "in_list_view": 1},
        {"fieldname": "items_offered", "fieldtype": "Small Text", "label": "Items Offered"},
        {"fieldname": "post_url", "fieldtype": "Data", "label": "Post URL"},
        {"fieldname": "post_date", "fieldtype": "Date", "label": "Post Date"},
        {"fieldname": "engagement", "fieldtype": "Int", "label": "Engagement (likes+comments)", "in_list_view": 1},
        {"fieldname": "estimated_reach", "fieldtype": "Int", "label": "Estimated Reach"},
        {"fieldname": "cost", "fieldtype": "Currency", "label": "Cost", "in_list_view": 1},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Invited\nConfirmed\nVisited\nPosted\nPaid", "in_list_view": 1},
    ], istable=True)

    make_doctype("Influencer", [
        {"fieldname": "influencer_name", "fieldtype": "Data", "label": "Name", "reqd": 1, "in_list_view": 1},
        {"fieldname": "platform", "fieldtype": "Select", "label": "Platform", "options": "Instagram\nTikTok\nYouTube\nFacebook\nBlog", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "handle", "fieldtype": "Data", "label": "@Handle", "in_list_view": 1},
        {"fieldname": "followers_count", "fieldtype": "Int", "label": "Followers", "in_list_view": 1},
        {"fieldname": "cb_inf1", "fieldtype": "Column Break"},
        {"fieldname": "category", "fieldtype": "Select", "label": "Category", "options": "Food\nLifestyle\nLocal\nCelebrity", "in_standard_filter": 1},
        {"fieldname": "contact_phone", "fieldtype": "Data", "label": "Phone"},
        {"fieldname": "contact_email", "fieldtype": "Data", "label": "Email", "options": "Email"},
        {"fieldname": "sb_campaigns", "fieldtype": "Section Break", "label": "Visits & Campaigns"},
        {"fieldname": "invitations", "fieldtype": "Table", "label": "Visits", "options": "Influencer Visit"},
        {"fieldname": "sb_metrics", "fieldtype": "Section Break", "label": "Metrics"},
        {"fieldname": "total_reach", "fieldtype": "Int", "label": "Total Reach", "read_only": 1},
        {"fieldname": "total_cost", "fieldtype": "Currency", "label": "Total Cost", "read_only": 1},
        {"fieldname": "cb_inf2", "fieldtype": "Column Break"},
        {"fieldname": "roi_score", "fieldtype": "Float", "label": "ROI (Reach per EGP)", "read_only": 1},
        {"fieldname": "rating", "fieldtype": "Rating", "label": "Rating"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="field:influencer_name")

    # ═══════════════════════════════════════════
    # B4: (Delivery Platform Settings already in Candela Settings — just need order_channel)
    # ═══════════════════════════════════════════

    # ═══════════════════════════════════════════
    # B5: CORPORATE ACCOUNT + LUNCH PACKAGE
    # ═══════════════════════════════════════════
    make_doctype("Corporate Lunch Package", [
        {"fieldname": "package_name", "fieldtype": "Data", "label": "Package Name", "reqd": 1, "unique": 1, "in_list_view": 1},
        {"fieldname": "package_name_ar", "fieldtype": "Data", "label": "Package Name (Arabic)"},
        {"fieldname": "price_per_person", "fieldtype": "Currency", "label": "Price/Person", "reqd": 1, "in_list_view": 1},
        {"fieldname": "cb_clp1", "fieldtype": "Column Break"},
        {"fieldname": "minimum_orders", "fieldtype": "Int", "label": "Min Orders", "default": "10"},
        {"fieldname": "delivery_included", "fieldtype": "Check", "label": "Delivery Included"},
        {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
        {"fieldname": "sb_desc", "fieldtype": "Section Break"},
        {"fieldname": "description", "fieldtype": "Text", "label": "Package Description"},
    ], autoname="field:package_name")

    make_doctype("Corporate Account", [
        {"fieldname": "company_name", "fieldtype": "Data", "label": "Company Name", "reqd": 1, "in_list_view": 1},
        {"fieldname": "contact_person", "fieldtype": "Data", "label": "Contact Person", "in_list_view": 1},
        {"fieldname": "phone", "fieldtype": "Data", "label": "Phone"},
        {"fieldname": "email", "fieldtype": "Data", "label": "Email", "options": "Email"},
        {"fieldname": "cb_ca1", "fieldtype": "Column Break"},
        {"fieldname": "address", "fieldtype": "Small Text", "label": "Address"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Active\nSuspended\nClosed", "default": "Active", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "sb_terms", "fieldtype": "Section Break", "label": "Terms"},
        {"fieldname": "payment_terms", "fieldtype": "Select", "label": "Payment Terms", "options": "Prepaid\nWeekly Invoice\nMonthly Invoice", "default": "Monthly Invoice"},
        {"fieldname": "credit_limit", "fieldtype": "Currency", "label": "Credit Limit"},
        {"fieldname": "discount_percentage", "fieldtype": "Float", "label": "Discount %"},
        {"fieldname": "cb_ca2", "fieldtype": "Column Break"},
        {"fieldname": "subscribed_package", "fieldtype": "Link", "label": "Subscribed Package", "options": "Corporate Lunch Package"},
        {"fieldname": "employees_count", "fieldtype": "Int", "label": "Employees"},
        {"fieldname": "delivery_time", "fieldtype": "Time", "label": "Delivery Time"},
        {"fieldname": "sb_stats", "fieldtype": "Section Break", "label": "Stats"},
        {"fieldname": "total_orders", "fieldtype": "Int", "label": "Total Orders", "read_only": 1},
        {"fieldname": "total_revenue", "fieldtype": "Currency", "label": "Total Revenue", "read_only": 1},
        {"fieldname": "outstanding_balance", "fieldtype": "Currency", "label": "Outstanding Balance", "read_only": 1},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="naming_series:", naming_rule='By "Naming Series" field')

    # ═══════════════════════════════════════════
    # B6: MARKETING CAMPAIGN + CHILDREN
    # ═══════════════════════════════════════════
    make_doctype("Campaign Activity", [
        {"fieldname": "activity_type", "fieldtype": "Select", "label": "Type", "options": "Post\nAd\nEvent\nInfluencer\nPromo\nEmail Blast", "in_list_view": 1},
        {"fieldname": "description", "fieldtype": "Data", "label": "Description", "in_list_view": 1},
        {"fieldname": "scheduled_date", "fieldtype": "Date", "label": "Date", "in_list_view": 1},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Planned\nIn Progress\nCompleted\nCancelled", "in_list_view": 1},
        {"fieldname": "cost", "fieldtype": "Currency", "label": "Cost", "in_list_view": 1},
        {"fieldname": "reach", "fieldtype": "Int", "label": "Reach"},
        {"fieldname": "engagement", "fieldtype": "Int", "label": "Engagement"},
        {"fieldname": "conversions", "fieldtype": "Int", "label": "Conversions"},
    ], istable=True)

    make_doctype("Content Calendar Entry", [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "reqd": 1, "in_list_view": 1},
        {"fieldname": "platform", "fieldtype": "Select", "label": "Platform", "options": "Instagram\nFacebook\nTikTok\nWhatsApp\nEmail\nSMS", "in_list_view": 1},
        {"fieldname": "content_type", "fieldtype": "Select", "label": "Type", "options": "Photo\nVideo\nStory\nReel\nCarousel\nText", "in_list_view": 1},
        {"fieldname": "caption", "fieldtype": "Small Text", "label": "Caption"},
        {"fieldname": "hashtags", "fieldtype": "Data", "label": "Hashtags"},
        {"fieldname": "image", "fieldtype": "Attach Image", "label": "Image"},
        {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Planned\nCreated\nPosted", "in_list_view": 1},
    ], istable=True)

    make_doctype("Marketing Campaign", [
        {"fieldname": "campaign_name", "fieldtype": "Data", "label": "Campaign Name", "reqd": 1, "in_list_view": 1},
        {"fieldname": "campaign_type", "fieldtype": "Select", "label": "Type", "options": "Pre-Launch\nGrand Opening\nSeasonal\nOngoing\nEvent-Specific", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "phase", "fieldtype": "Select", "label": "Phase", "options": "Planning\nActive\nCompleted\nPaused", "default": "Planning", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "cb_mc1", "fieldtype": "Column Break"},
        {"fieldname": "start_date", "fieldtype": "Date", "label": "Start Date"},
        {"fieldname": "end_date", "fieldtype": "Date", "label": "End Date"},
        {"fieldname": "target_persona", "fieldtype": "Link", "label": "Target Persona", "options": "Customer Persona"},
        {"fieldname": "sb_budget", "fieldtype": "Section Break", "label": "Budget"},
        {"fieldname": "budget", "fieldtype": "Currency", "label": "Budget"},
        {"fieldname": "spent", "fieldtype": "Currency", "label": "Spent", "read_only": 1},
        {"fieldname": "cb_mc2", "fieldtype": "Column Break"},
        {"fieldname": "channels", "fieldtype": "Small Text", "label": "Channels"},
        {"fieldname": "sb_activities", "fieldtype": "Section Break", "label": "Activities"},
        {"fieldname": "activities", "fieldtype": "Table", "label": "Activities", "options": "Campaign Activity"},
        {"fieldname": "sb_content", "fieldtype": "Section Break", "label": "Content Calendar"},
        {"fieldname": "content_calendar", "fieldtype": "Table", "label": "Content Calendar", "options": "Content Calendar Entry"},
        {"fieldname": "sb_results", "fieldtype": "Section Break", "label": "Results"},
        {"fieldname": "total_reach", "fieldtype": "Int", "label": "Total Reach", "read_only": 1},
        {"fieldname": "total_engagement", "fieldtype": "Int", "label": "Total Engagement", "read_only": 1},
        {"fieldname": "cb_mc3", "fieldtype": "Column Break"},
        {"fieldname": "new_customers_acquired", "fieldtype": "Int", "label": "New Customers"},
        {"fieldname": "revenue_attributed", "fieldtype": "Currency", "label": "Revenue Attributed"},
        {"fieldname": "roi_percentage", "fieldtype": "Percent", "label": "ROI %", "read_only": 1},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="naming_series:", naming_rule='By "Naming Series" field')

    # ═══════════════════════════════════════════
    # B7: ONLINE REVIEW (Reputation Management)
    # ═══════════════════════════════════════════
    make_doctype("Online Review", [
        {"fieldname": "platform", "fieldtype": "Select", "label": "Platform", "options": "Google Maps\nFacebook\nTripAdvisor\nInstagram\nTalabat\nInstashop", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "reviewer_name", "fieldtype": "Data", "label": "Reviewer Name", "in_list_view": 1},
        {"fieldname": "review_date", "fieldtype": "Date", "label": "Review Date", "default": "Today", "in_list_view": 1},
        {"fieldname": "rating", "fieldtype": "Rating", "label": "Rating", "in_list_view": 1},
        {"fieldname": "cb_or1", "fieldtype": "Column Break"},
        {"fieldname": "sentiment", "fieldtype": "Select", "label": "Sentiment", "options": "Positive\nNeutral\nNegative\nCritical", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "review_url", "fieldtype": "Data", "label": "Review URL"},
        {"fieldname": "sb_content", "fieldtype": "Section Break", "label": "Content"},
        {"fieldname": "review_text", "fieldtype": "Text", "label": "Review Text"},
        {"fieldname": "sb_response", "fieldtype": "Section Break", "label": "Response"},
        {"fieldname": "response_text", "fieldtype": "Text", "label": "Response Text"},
        {"fieldname": "responded_by", "fieldtype": "Link", "label": "Responded By", "options": "User"},
        {"fieldname": "responded_at", "fieldtype": "Datetime", "label": "Responded At"},
        {"fieldname": "response_posted", "fieldtype": "Check", "label": "Response Posted"},
        {"fieldname": "sb_action", "fieldtype": "Section Break", "label": "Action"},
        {"fieldname": "requires_action", "fieldtype": "Check", "label": "Requires Action"},
        {"fieldname": "action_taken", "fieldtype": "Small Text", "label": "Action Taken"},
        {"fieldname": "resolved", "fieldtype": "Check", "label": "Resolved"},
        {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
    ], autoname="naming_series:", naming_rule='By "Naming Series" field')

    # ═══════════════════════════════════════════
    # B8: CAFÉ AMENITY
    # ═══════════════════════════════════════════
    make_doctype("Cafe Amenity", [
        {"fieldname": "amenity_name", "fieldtype": "Data", "label": "Amenity Name", "reqd": 1, "unique": 1, "in_list_view": 1},
        {"fieldname": "amenity_name_ar", "fieldtype": "Data", "label": "Amenity Name (Arabic)"},
        {"fieldname": "amenity_type", "fieldtype": "Select", "label": "Type", "options": "WiFi\nPower\nSeating\nNoise\nOther", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "icon", "fieldtype": "Data", "label": "Icon (Lucide name)"},
        {"fieldname": "cb_ca1", "fieldtype": "Column Break"},
        {"fieldname": "wifi_ssid", "fieldtype": "Data", "label": "WiFi SSID", "depends_on": "eval:doc.amenity_type=='WiFi'"},
        {"fieldname": "wifi_password_display", "fieldtype": "Data", "label": "WiFi Password", "depends_on": "eval:doc.amenity_type=='WiFi'"},
        {"fieldname": "wifi_speed_mbps", "fieldtype": "Float", "label": "WiFi Speed (Mbps)", "depends_on": "eval:doc.amenity_type=='WiFi'"},
        {"fieldname": "power_outlets_count", "fieldtype": "Int", "label": "Power Outlets", "depends_on": "eval:doc.amenity_type=='Power'"},
        {"fieldname": "noise_level", "fieldtype": "Select", "label": "Noise Level", "options": "\nSilent\nQuiet\nModerate\nLively", "depends_on": "eval:doc.amenity_type=='Noise'"},
        {"fieldname": "sb_display", "fieldtype": "Section Break", "label": "Display"},
        {"fieldname": "description_ar", "fieldtype": "Small Text", "label": "Description (Arabic)"},
        {"fieldname": "description_en", "fieldtype": "Small Text", "label": "Description (English)"},
        {"fieldname": "zone", "fieldtype": "Data", "label": "Zone"},
        {"fieldname": "show_on_website", "fieldtype": "Check", "label": "Show on Website", "default": "1"},
    ], autoname="field:amenity_name")

    # ═══════════════════════════════════════════
    # B9: COMPETITOR
    # ═══════════════════════════════════════════
    make_doctype("Competitor", [
        {"fieldname": "competitor_name", "fieldtype": "Data", "label": "Competitor Name", "reqd": 1, "in_list_view": 1},
        {"fieldname": "location", "fieldtype": "Data", "label": "Location", "in_list_view": 1},
        {"fieldname": "competitor_type", "fieldtype": "Select", "label": "Type", "options": "Direct\nIndirect\nChain", "in_list_view": 1, "in_standard_filter": 1},
        {"fieldname": "cb_comp1", "fieldtype": "Column Break"},
        {"fieldname": "cuisine", "fieldtype": "Data", "label": "Cuisine"},
        {"fieldname": "price_range", "fieldtype": "Select", "label": "Price Range", "options": "$\n$$\n$$$"},
        {"fieldname": "google_rating", "fieldtype": "Float", "label": "Google Rating"},
        {"fieldname": "last_checked", "fieldtype": "Date", "label": "Last Checked"},
        {"fieldname": "sb_analysis", "fieldtype": "Section Break", "label": "Analysis"},
        {"fieldname": "menu_highlights", "fieldtype": "Small Text", "label": "Menu Highlights"},
        {"fieldname": "strengths", "fieldtype": "Small Text", "label": "Strengths"},
        {"fieldname": "cb_comp2", "fieldtype": "Column Break"},
        {"fieldname": "weaknesses", "fieldtype": "Small Text", "label": "Weaknesses"},
        {"fieldname": "our_advantage", "fieldtype": "Small Text", "label": "Our Advantage"},
        {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    ], autoname="field:competitor_name")

    print("\n✅ All 30 DocTypes generated successfully!\n")


if __name__ == "__main__":
    generate_all()
