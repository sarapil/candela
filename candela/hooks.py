"""Candela – Italian Café & Restaurant · Frappe v16 App Hooks"""

app_name = "candela"
app_title = "Candela Restaurant"
app_publisher = "Arkan Labs"
app_description = "Italian Café & Restaurant Website + Operations Backend"
app_email = "dev@arkanlabs.com"
app_license = "mit"
app_icon = "/assets/candela/images/candela-topbar.svg"
app_color = "#F59E0B"
app_logo_url = "/assets/candela/images/candela-logo.svg"

# ─── Required Apps ───────────────────────────────────────────────────
required_apps = ["frappe", "caps"]

# ─── App Launcher ────────────────────────────────────────────────────
add_to_apps_screen = [
	{
		"name": "candela",
		"logo": "/assets/candela/images/candela-logo.svg",
		"title": "Candela Restaurant",
		"route": "/desk/candela",
	}
]

# ─── Includes ────────────────────────────────────────────────────────
# Desk (admin) assets
app_include_css = [
	"/assets/candela/css/candela-variables.css",
	"/assets/candela/css/candela_desk.css",
]
app_include_js = [
	"/assets/candela/js/candela_workspace.js",
	"/assets/candela/js/candela_onboarding.js",
]

# Public website assets
web_include_css = [
	"/assets/candela/css/candela-variables.css",
	"/assets/candela/css/candela_theme.css",
	"/assets/candela/css/candela_animations.css",
	"/assets/candela/css/candela_responsive.css",
	"/assets/candela/css/candela_rtl.css",
]
web_include_js = [
	"/assets/candela/js/candela_website.js",
]

# ─── Desktop Icons ───────────────────────────────────────────────────
app_include_icons = [
	"/assets/candela/icons/desktop_icons/solid/candela.svg",
]

# ─── Website Context ─────────────────────────────────────────────────
website_context = {
	"favicon": "/assets/candela/images/favicon.svg",
	"splash_image": "/assets/candela/images/candela-splash.svg",
}

# ─── Website Route Rules ─────────────────────────────────────────────
website_route_rules = [
	# Public website pages
	{"from_route": "/dela", "to_route": "dela/index"},
	{"from_route": "/dela/menu", "to_route": "dela/menu"},
	{"from_route": "/dela/about", "to_route": "dela/about"},
	{"from_route": "/dela/gallery", "to_route": "dela/gallery"},
	{"from_route": "/dela/reservation", "to_route": "dela/reservation"},
	{"from_route": "/dela/events", "to_route": "dela/events"},
	{"from_route": "/dela/order", "to_route": "dela/order"},
	{"from_route": "/dela/order-tracking", "to_route": "dela/order_tracking"},
	{"from_route": "/dela/contact", "to_route": "dela/contact"},
	# Admin dashboard pages
	{"from_route": "/deladmin", "to_route": "deladmin/index"},
	{"from_route": "/deladmin/settings", "to_route": "deladmin/settings"},
	{"from_route": "/deladmin/overview", "to_route": "deladmin/overview"},
	{"from_route": "/deladmin/pos", "to_route": "deladmin/pos"},
	{"from_route": "/deladmin/kitchen", "to_route": "deladmin/kitchen"},
	{"from_route": "/deladmin/tables", "to_route": "deladmin/tables"},
	{"from_route": "/deladmin/reports", "to_route": "deladmin/reports"},
	{"from_route": "/deladmin/inventory", "to_route": "deladmin/inventory"},
	{"from_route": "/deladmin/staff", "to_route": "deladmin/staff"},
	# Operations admin pages (Supplementary Prompt)
	{"from_route": "/deladmin/procurement", "to_route": "deladmin/procurement"},
	{"from_route": "/deladmin/warehouses", "to_route": "deladmin/warehouses"},
	{"from_route": "/deladmin/production", "to_route": "deladmin/production"},
	{"from_route": "/deladmin/shifts", "to_route": "deladmin/shifts"},
	{"from_route": "/deladmin/closing", "to_route": "deladmin/closing"},
	{"from_route": "/deladmin/assets", "to_route": "deladmin/assets"},
	{"from_route": "/deladmin/marketing", "to_route": "deladmin/marketing"},
	{"from_route": "/deladmin/users", "to_route": "deladmin/users"},
	# App info & onboarding pages
	{"from_route": "/candela-about", "to_route": "candela-about"},
	{"from_route": "/candela-onboarding", "to_route": "candela-onboarding"},
]

# ─── Jinja ────────────────────────────────────────────────────────────
jinja = {
	"methods": [
		"candela.utils.get_candela_settings",
		"candela.utils.get_menu_categories",
		"candela.utils.get_featured_items",
		"candela.utils.get_opening_hours_display",
		"candela.utils.get_approved_reviews",
		"candela.utils.get_active_events",
		"candela.utils.get_gallery_images",
		"candela.utils.candela_url",
	],
}

# ─── Installation ─────────────────────────────────────────────────────
after_install = "candela.install.after_install"

after_migrate = ["candela.candela.seed.seed_data"]

# ─── Guest Methods (public API — no login required) ──────────────────
guest_methods = [
	"candela.api.get_menu",
	"candela.api.get_menu_item",
	"candela.api.submit_reservation",
	"candela.api.subscribe_newsletter",
	"candela.api.submit_review",
	"candela.api.get_order_status",
	"candela.api.get_delivery_zones",
	"candela.api.validate_promo_code",
	"candela.api.submit_order",
]

# ─── Whitelisted Methods (login required) ────────────────────────────
whitelisted_methods = [
	# POS & Kitchen
	"candela.api.create_pos_invoice",
	"candela.api.get_kitchen_orders",
	"candela.api.update_kitchen_status",
	"candela.api.update_table_status",
	# Procurement
	"candela.operations_api.create_purchase_request",
	"candela.operations_api.approve_purchase_request",
	"candela.operations_api.receive_grn",
	# Stock & Inventory
	"candela.operations_api.get_stock_levels",
	"candela.operations_api.do_stock_transfer",
	"candela.operations_api.start_reconciliation",
	# POS Shift
	"candela.operations_api.open_pos_shift",
	"candela.operations_api.close_pos_shift",
	# Production / Kitchen
	"candela.operations_api.create_production_log",
	"candela.operations_api.complete_production_log",
	# Daily Closing
	"candela.operations_api.generate_daily_closing",
	# Reports
	"candela.operations_api.get_operations_dashboard",
	"candela.operations_api.get_food_cost_report",
]

# ─── Document Events ─────────────────────────────────────────────────
doc_events = {
	"Table Reservation": {
		"after_insert": "candela.notifications.notify_new_reservation",
	},
	"Online Order": {
		"after_insert": "candela.notifications.notify_new_order",
		"on_update": [
			"candela.notifications.notify_order_status_change",
			"candela.governance.deduct_ingredients_on_confirm",
		],
	},
	"Customer Review": {
		"after_insert": "candela.notifications.notify_new_review",
	},
	"POS Invoice": {
		"after_insert": [
			"candela.notifications.notify_new_pos_order",
			"candela.governance.deduct_ingredients_on_pos",
		],
	},
	# Governance: Price Change Logging
	"Menu Item": {
		"on_update": "candela.governance.log_price_change",
	},
	# Governance: Stock consumption audit
	"Stock Entry": {
		"before_insert": "candela.governance.enforce_recipe_on_dispensing",
	},
	# GRN → auto-stock
	"Goods Receipt Note": {
		"on_update": "candela.governance.stock_grn_items",
	},
	# Stock Reconciliation → adjust
	"Stock Reconciliation": {
		"on_update": "candela.governance.reconcile_stock",
	},
}

# ─── Scheduled Tasks ─────────────────────────────────────────────────
scheduler_events = {
	"daily": [
		"candela.tasks.mark_past_reservations_completed",
		"candela.tasks.deactivate_expired_promos",
		"candela.tasks.check_low_stock_alerts",
		"candela.tasks.check_preventive_maintenance",
		"candela.tasks.auto_populate_daily_closing",
	],
	"hourly": [
		"candela.tasks.mark_no_show_reservations",
	],
}

# ─── Notification Config ─────────────────────────────────────────────
notification_config = "candela.notifications.get_notification_config"

# ─── Fixtures ─────────────────────────────────────────────────────────
fixtures = [
	{
		"dt": "Role",
		"filters": [["name", "in", [
			"Candela Manager",
			"Candela Staff",
			"Candela Chef",
			"Candela Cashier",
			"Candela Waiter",
			"Candela Procurement",
			"Candela Marketing",
		]]],
	},
	# CAPS fixtures
	{"dt": "CAPS Capability", "filters": [["name", "like", "CD_%"]]},
	{"dt": "CAPS Capability Bundle", "filters": [["name", "like", "CD_%"]]},
	{"dt": "CAPS Role Capability Map", "filters": [["role", "like", "Candela%"]]},
	{"dt": "CAPS Field Capability Map", "filters": [["capability", "like", "CD_%"]]},
	# Desktop Icon
	{"dt": "Desktop Icon", "filters": [["app", "=", "candela"]]},
]

# ─── Website Context ─────────────────────────────────────────────────
update_website_context = "candela.overrides.update_website_context"

# ─── User Data Protection ────────────────────────────────────────────
user_data_fields = [
	{
		"doctype": "Table Reservation",
		"filter_by": "email",
		"redact_fields": ["guest_name", "phone"],
	},
	{
		"doctype": "Online Order",
		"filter_by": "email",
		"redact_fields": ["customer_name", "phone", "delivery_address"],
	},
	{
		"doctype": "Newsletter Subscriber",
		"filter_by": "email",
		"redact_fields": ["name_field"],
	},
]

