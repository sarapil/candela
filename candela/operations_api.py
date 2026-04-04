# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
Candela Operations API — authenticated endpoints for back-office operations.
Supplements the main api.py with procurement, inventory, POS shift, and reporting endpoints.
"""

import frappe
from frappe import _
from frappe.utils import today, now_datetime, flt, cint, add_days, getdate


# ═══════════════════════════════════════════
# PROCUREMENT
# ═══════════════════════════════════════════

@frappe.whitelist()
def create_purchase_request(items, urgency="Normal", supplier=None, notes=None):
    """Create a purchase request from admin panel."""
    frappe.only_for(["Candela Manager", "System Manager"])

    import json
    if isinstance(items, str):
        items = json.loads(items)

    pr = frappe.new_doc("Purchase Request")
    pr.urgency = urgency
    pr.supplier = supplier
    pr.notes = notes
    for item in items:
        pr.append("items", {
            "ingredient": item.get("ingredient"),
            "requested_qty": flt(item.get("qty")),
            "estimated_cost": flt(item.get("cost")),
            "reason": item.get("reason", ""),
        })
    pr.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "name": pr.name}


@frappe.whitelist()
def approve_purchase_request(name):
    """Approve a purchase request."""
    frappe.only_for(["Candela Manager", "System Manager"])

    pr = frappe.get_doc("Purchase Request", name)
    pr.status = "Approved"
    pr.approved_by = frappe.session.user
    pr.approved_date = now_datetime()
    pr.save(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True}


@frappe.whitelist()
def receive_grn(name):
    """Mark GRN as Stocked — triggers auto-stock addition via governance hooks."""
    frappe.only_for(["Candela Manager", "System Manager"])

    grn = frappe.get_doc("Goods Receipt Note", name)
    grn.status = "Stocked"
    grn.save(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "total_cost": grn.total_cost}


# ═══════════════════════════════════════════
# STOCK & INVENTORY
# ═══════════════════════════════════════════

@frappe.whitelist()
def get_stock_levels(category=None, low_stock_only=0):
    """Get current stock levels with optional filters."""
    frappe.only_for(["Candela User", "Candela Manager", "System Manager"])

    filters = {"is_active": 1}
    if category:
        filters["category"] = category

    ingredients = frappe.get_all("Ingredient", filters=filters, fields=[
        "name", "ingredient_name", "ingredient_name_ar", "category", "unit",
        "current_stock", "minimum_stock", "reorder_level", "cost_per_unit", "supplier"
    ], order_by="ingredient_name asc")

    if cint(low_stock_only):
        ingredients = [i for i in ingredients if i.current_stock <= i.minimum_stock]

    return ingredients


@frappe.whitelist()
def do_stock_transfer(from_warehouse, to_warehouse, items, reason="Daily Prep"):
    """Create and submit a stock transfer."""
    frappe.only_for(["Candela Manager", "System Manager"])

    import json
    if isinstance(items, str):
        items = json.loads(items)

    st = frappe.new_doc("Stock Transfer")
    st.from_warehouse = from_warehouse
    st.to_warehouse = to_warehouse
    st.reason = reason
    for item in items:
        st.append("items", {
            "ingredient": item.get("ingredient"),
            "quantity": flt(item.get("quantity")),
        })
    st.status = "Submitted"
    st.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "name": st.name}


@frappe.whitelist()
def start_reconciliation(warehouse=None):
    """Create a reconciliation document pre-populated with all active ingredients."""
    frappe.only_for(["Candela Manager", "System Manager"])

    rec = frappe.new_doc("Stock Reconciliation")
    if warehouse:
        rec.warehouse = warehouse

    ingredients = frappe.get_all("Ingredient", filters={"is_active": 1},
                                 fields=["name", "current_stock"])
    for ing in ingredients:
        rec.append("items", {
            "ingredient": ing.name,
            "system_qty": ing.current_stock,
            "counted_qty": 0,
        })
    rec.status = "Counting"
    rec.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "name": rec.name}


# ═══════════════════════════════════════════
# POS SHIFT MANAGEMENT
# ═══════════════════════════════════════════

@frappe.whitelist()
def open_pos_shift(opening_cash=0, shift_type="Full Day"):
    """Open a new POS shift."""
    frappe.only_for(["Candela User", "Candela Manager", "System Manager"])

    # Check if there's an open shift
    open_shift = frappe.db.exists("POS Shift", {
        "cashier": frappe.session.user,
        "status": "Open"
    })
    if open_shift:
        frappe.throw(_("You already have an open shift: {0}. Close it first.").format(open_shift))

    shift = frappe.new_doc("POS Shift")
    shift.shift_type = shift_type
    shift.opening_cash = flt(opening_cash)
    shift.opening_time = now_datetime()
    shift.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "shift": shift.name}


@frappe.whitelist()
def close_pos_shift(shift_name, closing_cash=0):
    """Close a POS shift and calculate totals."""
    frappe.only_for(["Candela Manager", "System Manager"])

    shift = frappe.get_doc("POS Shift", shift_name)
    if shift.status != "Open":
        frappe.throw(_("Shift is not open"))

    # Calculate sales from POS Invoices during this shift
    invoices = frappe.get_all("POS Invoice", filters={
        "cashier": shift.cashier,
        "creation": [">=", shift.opening_time],
        "status": "Paid",
    }, fields=["grand_total", "payment_method", "discount_amount"])

    shift.total_cash_sales = sum(
        flt(i.grand_total) for i in invoices if i.payment_method == "Cash"
    )
    shift.total_card_sales = sum(
        flt(i.grand_total) for i in invoices if i.payment_method == "Card"
    )
    shift.total_wallet_sales = sum(
        flt(i.grand_total) for i in invoices if i.payment_method not in ("Cash", "Card")
    )
    shift.total_discounts = sum(flt(i.discount_amount) for i in invoices)
    shift.orders_count = len(invoices)
    shift.closing_cash = flt(closing_cash)
    shift.closing_time = now_datetime()
    shift.status = "Closed"
    shift.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "success": True,
        "total_sales": shift.total_sales,
        "cash_variance": shift.cash_variance,
        "orders_count": shift.orders_count,
    }


# ═══════════════════════════════════════════
# PRODUCTION / KITCHEN
# ═══════════════════════════════════════════

@frappe.whitelist()
def create_production_log(menu_item, quantity, order_type=None, order_ref=None,
                          station=None, shift=None):
    """Create a production log entry when kitchen starts preparing."""
    frappe.only_for(["Candela Manager", "System Manager"])

    log = frappe.new_doc("Production Log")
    log.menu_item = menu_item
    log.quantity = cint(quantity)
    log.order_reference_type = order_type
    log.order_reference = order_ref
    log.kitchen_station = station
    log.shift = shift
    log.started_at = now_datetime()
    log.assigned_to = frappe.session.user
    log.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "name": log.name}


@frappe.whitelist()
def complete_production_log(name, quality="Pass", waste_items=None):
    """Mark production as complete, optionally record waste."""
    frappe.only_for(["Candela Manager", "System Manager"])

    import json
    log = frappe.get_doc("Production Log", name)
    log.completed_at = now_datetime()
    log.quality_check = quality

    if waste_items:
        if isinstance(waste_items, str):
            waste_items = json.loads(waste_items)
        for w in waste_items:
            log.append("waste_items", {
                "ingredient": w.get("ingredient"),
                "wasted_qty": flt(w.get("qty")),
                "reason": w.get("reason", "Other"),
            })

    log.save(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "prep_time": log.prep_time_minutes, "waste_cost": log.total_waste_cost}


# ═══════════════════════════════════════════
# DAILY CLOSING
# ═══════════════════════════════════════════

@frappe.whitelist()
def generate_daily_closing(closing_date=None):
    """Generate or refresh a daily closing report."""
    frappe.only_for(["Candela Manager", "System Manager"])

    closing_date = closing_date or today()

    existing = frappe.db.get_value("Daily Closing", {"closing_date": closing_date})
    if existing:
        dc = frappe.get_doc("Daily Closing", existing)
    else:
        dc = frappe.new_doc("Daily Closing")
        dc.closing_date = closing_date

    # Aggregate POS
    pos_data = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN order_type='Dine-in' THEN grand_total ELSE 0 END) as dine_in,
            SUM(CASE WHEN order_type='Takeaway' THEN grand_total ELSE 0 END) as takeaway,
            SUM(CASE WHEN payment_method='Cash' THEN grand_total ELSE 0 END) as cash_sales,
            SUM(CASE WHEN payment_method='Card' THEN grand_total ELSE 0 END) as card_sales,
            SUM(discount_amount) as discounts,
            COUNT(*) as cnt
        FROM `tabPOS Invoice`
        WHERE DATE(creation) = %s AND status = 'Paid'
    """, closing_date, as_dict=True)[0]

    # Aggregate Online Orders
    online_data = frappe.db.sql("""
        SELECT
            SUM(total) as delivery_total,
            SUM(CASE WHEN payment_method IN ('Paymob','Fawry') THEN total ELSE 0 END) as online_pay,
            COUNT(*) as cnt
        FROM `tabOnline Order`
        WHERE DATE(creation) = %s AND status NOT IN ('Cancelled','Pending')
    """, closing_date, as_dict=True)[0]

    # Stock consumption cost
    consumption_cost = frappe.db.sql("""
        SELECT IFNULL(SUM(total_cost), 0) as cost
        FROM `tabStock Entry`
        WHERE date = %s AND entry_type = 'Consumption'
    """, closing_date, as_dict=True)[0]

    dc.total_dine_in_revenue = flt(pos_data.dine_in)
    dc.total_takeaway_revenue = flt(pos_data.takeaway)
    dc.total_delivery_revenue = flt(online_data.delivery_total)
    dc.cash_collected = flt(pos_data.cash_sales)
    dc.card_collected = flt(pos_data.card_sales)
    dc.online_payments = flt(online_data.online_pay)
    dc.total_orders = cint(pos_data.cnt) + cint(online_data.cnt)
    dc.food_cost_today = flt(consumption_cost.cost)

    dc.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "success": True,
        "name": dc.name,
        "gross_revenue": dc.gross_revenue,
        "total_orders": dc.total_orders,
        "food_cost_pct": dc.food_cost_percentage,
    }


# ═══════════════════════════════════════════
# REPORTS DATA API
# ═══════════════════════════════════════════

@frappe.whitelist()
def get_operations_dashboard():
    """Get comprehensive dashboard data for operations overview."""
    frappe.only_for(["Candela User", "Candela Manager", "System Manager"])

    from frappe.utils import add_days

    date = today()

    # Today's numbers
    pos_today = frappe.db.sql("""
        SELECT COUNT(*) as cnt, IFNULL(SUM(grand_total), 0) as total
        FROM `tabPOS Invoice`
        WHERE DATE(creation) = %s AND status = 'Paid'
    """, date, as_dict=True)[0]

    online_today = frappe.db.sql("""
        SELECT COUNT(*) as cnt, IFNULL(SUM(total), 0) as total
        FROM `tabOnline Order`
        WHERE DATE(creation) = %s AND status NOT IN ('Cancelled','Pending')
    """, date, as_dict=True)[0]

    reservations_today = frappe.db.count("Table Reservation", {
        "reservation_date": date,
        "status": ["not in", ["Cancelled", "No-Show"]],
    })

    # Low stock count
    low_stock = frappe.db.sql("""
        SELECT COUNT(*) as cnt FROM `tabIngredient`
        WHERE is_active=1 AND current_stock < minimum_stock AND minimum_stock > 0
    """, as_dict=True)[0].cnt

    # Pending kitchen orders
    pending_kitchen = frappe.db.count("POS Invoice", {
        "kitchen_status": ["in", ["Pending", "Preparing"]],
        "status": ["!=", "Cancelled"],
    })

    # Open maintenance requests
    open_maintenance = frappe.db.count("Maintenance Request", {
        "status": ["not in", ["Completed", "Closed"]],
    })

    # Weekly revenue (last 7 days)
    weekly = frappe.db.sql("""
        SELECT DATE(creation) as day, SUM(grand_total) as revenue
        FROM `tabPOS Invoice`
        WHERE DATE(creation) >= %s AND status = 'Paid'
        GROUP BY DATE(creation) ORDER BY day
    """, add_days(date, -6), as_dict=True)

    # Top items today
    top_items = frappe.db.sql("""
        SELECT item_name, SUM(quantity) as qty, SUM(amount) as revenue
        FROM `tabPOS Invoice Item`
        WHERE DATE(creation) = %s
        GROUP BY item_name ORDER BY qty DESC LIMIT 5
    """, date, as_dict=True)

    # Channel breakdown
    channel_data = frappe.db.sql("""
        SELECT IFNULL(order_channel, 'Dine-in') as channel, COUNT(*) as cnt, SUM(grand_total) as revenue
        FROM `tabPOS Invoice`
        WHERE DATE(creation) = %s AND status = 'Paid'
        GROUP BY order_channel
    """, date, as_dict=True)

    return {
        "today": {
            "revenue": flt(pos_today.total) + flt(online_today.total),
            "pos_orders": pos_today.cnt,
            "online_orders": online_today.cnt,
            "reservations": reservations_today,
        },
        "alerts": {
            "low_stock": low_stock,
            "pending_kitchen": pending_kitchen,
            "open_maintenance": open_maintenance,
        },
        "weekly_revenue": weekly,
        "top_items": top_items,
        "channels": channel_data,
    }


@frappe.whitelist()
def get_food_cost_report(from_date=None, to_date=None):
    """Food cost variance report."""
    frappe.only_for(["Candela User", "Candela Manager", "System Manager"])

    from_date = from_date or add_days(today(), -30)
    to_date = to_date or today()

    # Expected cost (from orders × recipes)
    expected = frappe.db.sql("""
        SELECT
            mi.name as menu_item,
            mi.item_name_en,
            SUM(oi.quantity) as total_qty,
            mi.food_cost as recipe_cost,
            SUM(oi.quantity) * mi.food_cost as expected_cost,
            SUM(oi.amount) as revenue
        FROM `tabPOS Invoice Item` oi
        JOIN `tabMenu Item` mi ON mi.name = oi.menu_item
        JOIN `tabPOS Invoice` pi ON pi.name = oi.parent
        WHERE DATE(pi.creation) BETWEEN %s AND %s AND pi.status = 'Paid'
        GROUP BY mi.name
        ORDER BY expected_cost DESC
    """, (from_date, to_date), as_dict=True)

    # Actual consumption from stock entries
    actual_total = frappe.db.sql("""
        SELECT IFNULL(SUM(total_cost), 0) as total
        FROM `tabStock Entry`
        WHERE date BETWEEN %s AND %s AND entry_type = 'Consumption'
    """, (from_date, to_date), as_dict=True)[0].total

    total_expected = sum(flt(r.expected_cost) for r in expected)
    total_revenue = sum(flt(r.revenue) for r in expected)

    return {
        "items": expected,
        "totals": {
            "expected_food_cost": total_expected,
            "actual_food_cost": flt(actual_total),
            "variance": flt(actual_total) - total_expected,
            "total_revenue": total_revenue,
            "food_cost_pct": (flt(actual_total) / total_revenue * 100) if total_revenue else 0,
        },
        "period": {"from": from_date, "to": to_date},
    }
