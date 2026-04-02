import frappe

no_cache = 1
show_sidebar = False

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(frappe._("Login required"), frappe.AuthenticationError)
    if not frappe.has_permission("User", "write"):
        frappe.throw(frappe._("Not permitted"), frappe.PermissionError)
    context.title = frappe._("User Management — Candela")
