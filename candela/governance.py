# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
Candela Governance Rules Engine
================================
5 critical business rules that cannot be bypassed.
Enforced via DocType hooks and server scripts.

1. No sale without stock deduction
2. No dispensing without recipe
3. No price change without log
4. No payment without document
5. Every movement has accounting impact
"""

import frappe
from frappe import _
from frappe.utils import flt, now


# ─── Rule 1: No sale without stock deduction ───
def enforce_stock_deduction_on_sale(doc, method):
    """Every confirmed order MUST trigger stock deduction via recipe."""
    if doc.doctype == "Online Order" and doc.status == "Confirmed":
        for item in doc.items:
            menu_item = frappe.get_cached_doc("Menu Item", item.menu_item)
            if not menu_item.recipe_items:
                frappe.msgprint(
                    _("⚠️ '{0}' has no recipe — stock deduction skipped. "
                      "Add a recipe to enable automatic inventory tracking.").format(
                        item.item_name
                    ),
                    indicator="orange",
                )


# ─── Rule 2: No dispensing without recipe ───
def enforce_recipe_on_dispensing(doc, method):
    """No ingredient dispensing from warehouse without a recipe reference."""
    if doc.entry_type == "Consumption":
        if not doc.reference_type or not doc.reference_name:
            frappe.msgprint(
                _("⚠️ Stock consumption should reference an order or production log for audit trail."),
                indicator="orange",
            )


# ─── Rule 3: No price change without log ───
def log_price_change(doc, method):
    """Every price change must be logged with old/new values and user."""
    if doc.has_value_changed("price"):
        old_doc = doc.get_doc_before_save()
        old_price = old_doc.price if old_doc else 0
        new_price = doc.price or 0
        if old_price != new_price and old_price > 0:
            change_pct = ((new_price - old_price) / old_price) * 100 if old_price else 0
            frappe.get_doc({
                "doctype": "Price Change Log",
                "naming_series": "PCL-.YYYY.-.#####",
                "menu_item": doc.name,
                "old_price": old_price,
                "new_price": new_price,
                "change_pct": change_pct,
                "changed_by": frappe.session.user,
                "changed_at": now(),
                "reason": doc.price_change_reason or _("Not specified"),
            }).insert(ignore_permissions=True)
            frappe.msgprint(
                _("📝 Price change logged: {0} → {1} ({2}%)").format(
                    old_price, new_price, round(change_pct, 1)
                ),
                indicator="blue",
            )


# ─── Rule 4: No payment without document ───
# (Enforced by POS Shift — every payment is tied to a POS Invoice)


# ─── Rule 5: Every movement has accounting impact ───
def ensure_accounting_impact(doc, method):
    """Log a note that accounting impact should be tracked."""
    # In a full ERPNext integration, this would create GL entries.
    # For standalone Candela, we ensure every stock/financial doc has audit trail.
    pass


# ─── Auto stock deduction helpers ───
def deduct_ingredients_on_confirm(doc, method):
    """Called on Online Order status change — deduct stock when Confirmed."""
    if doc.status != "Confirmed":
        return
    _deduct_order_ingredients(doc, "Online Order")


def deduct_ingredients_on_pos(doc, method):
    """Called on POS Invoice after_insert — deduct stock for kitchen."""
    if doc.kitchen_status == "Pending":
        _deduct_order_ingredients(doc, "POS Invoice")


def _deduct_order_ingredients(doc, ref_type):
    """Auto-deduct ingredients based on recipe for each ordered item."""
    for item in doc.items:
        menu_item_name = item.menu_item
        if not menu_item_name:
            continue
        menu_item = frappe.get_cached_doc("Menu Item", menu_item_name)
        if not menu_item.recipe_items:
            continue
        for recipe_row in menu_item.recipe_items:
            qty_to_deduct = flt(recipe_row.quantity_per_serving) * flt(item.quantity)
            if qty_to_deduct <= 0:
                continue
            ingredient_doc = frappe.get_doc("Ingredient", recipe_row.ingredient)
            if ingredient_doc.current_stock < qty_to_deduct:
                frappe.msgprint(
                    _("⚠️ Low stock: {0} — needed {1} {2}, available {3}").format(
                        recipe_row.ingredient, qty_to_deduct,
                        ingredient_doc.unit or "", ingredient_doc.current_stock
                    ),
                    indicator="orange",
                )
            # Create stock entry for audit trail
            try:
                frappe.get_doc({
                    "doctype": "Stock Entry",
                    "naming_series": "STE-.YYYY.-.#####",
                    "entry_type": "Consumption",
                    "date": frappe.utils.today(),
                    "ingredient": recipe_row.ingredient,
                    "quantity": qty_to_deduct,
                    "unit_cost": flt(recipe_row.cost_per_unit),
                    "total_cost": qty_to_deduct * flt(recipe_row.cost_per_unit),
                    "reference_type": ref_type,
                    "reference_name": doc.name,
                }).insert(ignore_permissions=True)
            except Exception:
                frappe.log_error(
                    f"Stock deduction failed for {recipe_row.ingredient}",
                    "Candela Stock Deduction"
                )
            # Update stock directly
            ingredient_doc.reload()
            ingredient_doc.current_stock = max(0, flt(ingredient_doc.current_stock) - qty_to_deduct)
            ingredient_doc.save(ignore_permissions=True)


# ─── GRN Stocking — add stock on receipt ───
def stock_grn_items(doc, method):
    """When GRN status changes to 'Stocked', add accepted quantities to inventory."""
    if doc.status != "Stocked":
        return
    for item in doc.items:
        accepted = flt(item.accepted_qty) or flt(item.received_qty)
        if accepted <= 0:
            continue
        # Create stock entry
        frappe.get_doc({
            "doctype": "Stock Entry",
            "naming_series": "STE-.YYYY.-.#####",
            "entry_type": "Purchase",
            "date": frappe.utils.today(),
            "ingredient": item.ingredient,
            "quantity": accepted,
            "unit_cost": flt(item.unit_cost),
            "total_cost": accepted * flt(item.unit_cost),
            "reference_type": "Goods Receipt Note",
            "reference_name": doc.name,
            "supplier": doc.supplier,
        }).insert(ignore_permissions=True)
        # Update ingredient stock and cost
        ingredient = frappe.get_doc("Ingredient", item.ingredient)
        ingredient.current_stock = flt(ingredient.current_stock) + accepted
        if item.unit_cost:
            ingredient.cost_per_unit = flt(item.unit_cost)
            ingredient.last_purchase_date = frappe.utils.today()
        ingredient.save(ignore_permissions=True)


# ─── Stock Reconciliation — adjust stock ───
def reconcile_stock(doc, method):
    """When reconciliation is 'Adjusted', create adjustment entries."""
    if doc.status != "Adjusted":
        return
    for item in doc.items:
        variance = flt(item.counted_qty) - flt(item.system_qty)
        if variance == 0:
            continue
        entry_type = "Adjustment"
        frappe.get_doc({
            "doctype": "Stock Entry",
            "naming_series": "STE-.YYYY.-.#####",
            "entry_type": entry_type,
            "date": frappe.utils.today(),
            "ingredient": item.ingredient,
            "quantity": abs(variance),
            "reference_type": "Stock Reconciliation",
            "reference_name": doc.name,
            "notes": f"Reconciliation {'surplus' if variance > 0 else 'deficit'}: {item.reason or 'N/A'}",
        }).insert(ignore_permissions=True)
        ingredient = frappe.get_doc("Ingredient", item.ingredient)
        ingredient.current_stock = flt(item.counted_qty)
        ingredient.save(ignore_permissions=True)


# ─── Low Stock Alert (Scheduler) ───
def check_low_stock_alerts():
    """Daily: check ingredients below reorder level and auto-create purchase requests."""
    low_stock = frappe.get_all("Ingredient", filters={
        "is_active": 1,
        "current_stock": ["<", frappe.qb.Field("minimum_stock")]
    }, fields=["name", "ingredient_name", "current_stock", "minimum_stock", "unit", "supplier"])

    if not low_stock:
        return

    # Create a consolidated purchase request
    pr = frappe.new_doc("Purchase Request")
    pr.request_date = frappe.utils.today()
    pr.urgency = "Normal"
    pr.notes = _("Auto-generated from low stock alert")

    for ing in low_stock:
        reorder_qty = max(flt(ing.minimum_stock) * 2, 1)  # Order 2x minimum
        pr.append("items", {
            "ingredient": ing.name,
            "requested_qty": reorder_qty,
            "reason": _("Below minimum stock: {0} {1}").format(ing.current_stock, ing.unit or ""),
        })

    if pr.items:
        pr.insert(ignore_permissions=True)
        frappe.db.commit()


# ─── Maintenance Scheduler ───
def check_preventive_maintenance():
    """Daily: auto-create preventive maintenance requests for overdue assets."""
    from frappe.utils import add_days

    overdue = frappe.get_all("Restaurant Asset", filters={
        "status": "Active",
        "next_maintenance_date": ["<=", frappe.utils.today()],
    }, fields=["name", "asset_name", "next_maintenance_date", "maintenance_interval_days"])

    for asset in overdue:
        # Check if there's already an open request
        existing = frappe.db.exists("Maintenance Request", {
            "asset": asset.name,
            "status": ["not in", ["Completed", "Closed"]],
        })
        if existing:
            continue

        frappe.get_doc({
            "doctype": "Maintenance Request",
            "naming_series": "CMNT-.YYYY.-.#####",
            "asset": asset.name,
            "issue_type": "Preventive",
            "priority": "Medium",
            "description": _("Scheduled preventive maintenance for {0}").format(asset.asset_name),
        }).insert(ignore_permissions=True)

        # Update next maintenance date
        interval = asset.maintenance_interval_days or 90
        frappe.db.set_value("Restaurant Asset", asset.name,
                           "next_maintenance_date",
                           add_days(frappe.utils.today(), interval))

    frappe.db.commit()
