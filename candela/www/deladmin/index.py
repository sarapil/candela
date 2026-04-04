# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
    # Require login for admin pages
    if frappe.session.user == "Guest":
        frappe.throw("Please login to access the admin panel", frappe.PermissionError)

    settings = get_candela_settings()
    lang = get_lang()

    context.candela = settings
    context.page_type = "admin"
    context.title = "لوحة إدارة كانديلا" if lang == "ar" else "Candela Admin"
    context.candela_lang = lang
    context.candela_dir = "rtl" if is_rtl() else "ltr"
    context.no_breadcrumbs = True

    # Quick stats
    context.stats = {
        "pending_reservations": frappe.db.count(
            "Table Reservation", {"status": "Pending"}
        ),
        "active_orders": frappe.db.count(
            "Online Order",
            {"status": ["in", ["Pending", "Confirmed", "Preparing", "Ready", "Out for Delivery"]]},
        ),
        "menu_items": frappe.db.count("Menu Item", {"is_available": 1}),
        "unapproved_reviews": frappe.db.count(
            "Customer Review", {"is_approved": 0}
        ),
    }

    # Recent reservations (latest 5)
    try:
        context.recent_reservations = frappe.get_all(
            "Table Reservation",
            fields=["guest_name", "customer_name", "reservation_date", "number_of_guests", "status"],
            order_by="creation desc",
            limit_page_length=5,
        )
    except Exception:
        context.recent_reservations = []

    # Recent orders (latest 5)
    try:
        context.recent_orders = frappe.get_all(
            "Online Order",
            fields=["name", "customer_name", "total_amount", "status"],
            order_by="creation desc",
            limit_page_length=5,
        )
    except Exception:
        context.recent_orders = []
