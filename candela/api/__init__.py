# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""Candela public API — guest-accessible endpoints (no login required)."""

import frappe
from frappe import _
from frappe.utils import today, now_datetime, cint, flt
from candela.utils.rate_limiter import check_rate_limit


# ═══════════════════════════════════════════════════════════════
# Menu
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist(allow_guest=True)
def get_menu(category=None):
	"""Get all available menu items, optionally filtered by category."""
	filters = {"is_available": 1}
	if category:
		filters["category"] = category

	items = frappe.get_all(
		"Menu Item",
		filters=filters,
		fields=[
			"name", "item_name_ar", "item_name_en", "slug", "category",
			"description_ar", "description_en", "price", "discounted_price",
			"image", "is_new", "is_bestseller", "spice_level",
			"preparation_time_min", "calories", "available_for_delivery",
		],
		order_by="sort_order asc",
	)

	categories = frappe.get_all(
		"Menu Category",
		filters={"is_active": 1},
		fields=["name", "category_name_ar", "category_name_en", "icon_emoji", "slug"],
		order_by="sort_order asc",
	)

	return {"items": items, "categories": categories}


@frappe.whitelist(allow_guest=True)
def get_menu_item(slug):
	"""Get a single menu item by slug."""
	items = frappe.get_all(
		"Menu Item",
		filters={"slug": slug, "is_available": 1},
		fields=["*"],
		limit=1,
	)
	if not items:
		frappe.throw(_("Menu item not found"), frappe.DoesNotExistError)
	item = items[0]

	# Get dietary tags
	item["dietary_tags"] = frappe.get_all(
		"Menu Item Dietary Tag",
		filters={"parent": item.name},
		fields=["dietary_tag"],
		order_by="idx asc",
	)
	return item


# ═══════════════════════════════════════════════════════════════
# Reservations
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist(allow_guest=True)
def submit_reservation(guest_name, phone, reservation_date, reservation_time,
                       number_of_guests, email=None, occasion=None,
                       seating_preference=None, special_requests=None):
	"""Create a new table reservation from the website."""
	check_rate_limit("reservation", limit=5, window=60)
	settings = frappe.get_cached_doc("Candela Settings")
	if not settings.enable_reservations:
		frappe.throw(_("Reservations are currently disabled"))

	# Validate party size
	max_party = cint(settings.max_party_size) or 20
	if cint(number_of_guests) > max_party:
		frappe.throw(_("Maximum party size is {0}").format(max_party))

	reservation = frappe.new_doc("Table Reservation")
	reservation.guest_name = guest_name
	reservation.phone = phone
	reservation.email = email
	reservation.reservation_date = reservation_date
	reservation.reservation_time = reservation_time
	reservation.number_of_guests = cint(number_of_guests)
	reservation.occasion = occasion or "None"
	reservation.seating_preference = seating_preference or "Any"
	reservation.special_requests = special_requests
	reservation.source = "Website"

	# Auto-confirm if enabled
	if settings.auto_confirm:
		reservation.status = "Confirmed"

	reservation.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"success": True,
		"message": _("Reservation submitted successfully!"),
		"reservation_id": reservation.name,
		"status": reservation.status,
	}


# ═══════════════════════════════════════════════════════════════
# Newsletter
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist(allow_guest=True)
def subscribe_newsletter(email, name=None):
	"""Subscribe an email to the newsletter."""
	check_rate_limit("newsletter", limit=3, window=60)
	settings = frappe.get_cached_doc("Candela Settings")
	if not settings.enable_newsletter:
		frappe.throw(_("Newsletter is currently disabled"))

	if frappe.db.exists("Newsletter Subscriber", {"email": email}):
		return {"success": True, "message": _("You are already subscribed!")}

	sub = frappe.new_doc("Newsletter Subscriber")
	sub.email = email
	sub.name_field = name
	sub.source = "Website"
	sub.insert(ignore_permissions=True)
	frappe.db.commit()

	return {"success": True, "message": _("Successfully subscribed!")}


# ═══════════════════════════════════════════════════════════════
# Reviews
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist(allow_guest=True)
def submit_review(customer_name, rating, review_text_ar=None,
                  review_text_en=None, visit_date=None):
	"""Submit a customer review (requires approval)."""
	check_rate_limit("review", limit=3, window=60)
	settings = frappe.get_cached_doc("Candela Settings")
	if not settings.enable_reviews:
		frappe.throw(_("Reviews are currently disabled"))

	review = frappe.new_doc("Customer Review")
	review.customer_name = customer_name
	review.rating = flt(rating)
	review.review_text_ar = review_text_ar
	review.review_text_en = review_text_en
	review.visit_date = visit_date or today()
	review.source = "Website"
	review.is_approved = 0  # Requires manual approval
	review.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"success": True,
		"message": _("Thank you for your review! It will be published after approval."),
	}


# ═══════════════════════════════════════════════════════════════
# Online Ordering
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist(allow_guest=True)
def submit_order(customer_name, phone, order_type, items,
                 email=None, delivery_address=None, delivery_zone=None,
                 delivery_notes=None, payment_method="Cash on Delivery",
                 promo_code=None):
	"""Submit a new online order from the website."""
	check_rate_limit("order", limit=10, window=60)
	import json
	settings = frappe.get_cached_doc("Candela Settings")
	if not settings.enable_online_ordering:
		frappe.throw(_("Online ordering is currently disabled"))

	if isinstance(items, str):
		items = json.loads(items)

	if not items:
		frappe.throw(_("Order must contain at least one item"))

	order = frappe.new_doc("Online Order")
	order.customer_name = customer_name
	order.phone = phone
	order.email = email
	order.order_type = order_type

	if order_type == "Delivery":
		order.delivery_address = delivery_address
		order.delivery_zone = delivery_zone
		order.delivery_notes = delivery_notes

		if delivery_zone:
			zone = frappe.get_doc("Delivery Zone", delivery_zone)
			order.delivery_fee = zone.delivery_fee

	# Add items
	for item_data in items:
		menu_item = frappe.get_doc("Menu Item", item_data.get("menu_item"))
		order.append("items", {
			"menu_item": menu_item.name,
			"item_name": menu_item.item_name_en,
			"quantity": cint(item_data.get("quantity", 1)),
			"unit_price": menu_item.discounted_price or menu_item.price,
			"special_instructions": item_data.get("special_instructions"),
		})

	# Apply promo code
	if promo_code:
		promo = validate_promo_code(promo_code)
		if promo.get("valid"):
			order.promo_code = promo_code

	order.payment_method = payment_method
	order.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"success": True,
		"message": _("Order placed successfully!"),
		"order_id": order.name,
		"tracking_token": order.tracking_token,
		"total": order.total,
	}


@frappe.whitelist(allow_guest=True)
def get_order_status(tracking_token):
	"""Get order status by tracking token."""
	orders = frappe.get_all(
		"Online Order",
		filters={"tracking_token": tracking_token},
		fields=[
			"name", "customer_name", "status", "order_type",
			"total", "payment_status", "estimated_time",
			"creation",
		],
		limit=1,
	)
	if not orders:
		frappe.throw(_("Order not found"), frappe.DoesNotExistError)

	order = orders[0]
	order["items"] = frappe.get_all(
		"Order Item",
		filters={"parent": order.name},
		fields=["item_name", "quantity", "amount"],
	)
	return order


@frappe.whitelist(allow_guest=True)
def get_delivery_zones():
	"""Get all active delivery zones."""
	return frappe.get_all(
		"Delivery Zone",
		filters={"is_active": 1},
		fields=["name", "zone_name", "delivery_fee", "estimated_minutes"],
		order_by="zone_name asc",
	)


@frappe.whitelist(allow_guest=True)
def validate_promo_code(code):
	"""Validate a promo code and return discount details."""
	if not frappe.db.exists("Promo Code", code):
		return {"valid": False, "message": _("Invalid promo code")}

	promo = frappe.get_doc("Promo Code", code)

	if not promo.is_active:
		return {"valid": False, "message": _("This promo code is no longer active")}

	if promo.valid_from and str(promo.valid_from) > today():
		return {"valid": False, "message": _("This promo code is not yet valid")}

	if promo.valid_until and str(promo.valid_until) < today():
		return {"valid": False, "message": _("This promo code has expired")}

	if promo.max_uses and promo.times_used >= promo.max_uses:
		return {"valid": False, "message": _("This promo code has reached its usage limit")}

	return {
		"valid": True,
		"code": promo.code,
		"discount_type": promo.discount_type,
		"discount_value": promo.discount_value,
		"minimum_order": promo.minimum_order,
		"message": _("Promo code applied!"),
	}


# ═══════════════════════════════════════════════════════════════
# POS
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist()
def create_pos_invoice(order_type, items, status="Draft", kitchen_status="Pending",
                       restaurant_table=None, customer_name=None, phone=None,
                       payment_method=None, cash_received=0, notes=None):
	"""Create a POS invoice from the POS terminal."""
	frappe.only_for(["Candela Manager", "System Manager"])

	import json
	if isinstance(items, str):
		items = json.loads(items)

	if not items:
		frappe.throw(_("Invoice must contain at least one item"))

	inv = frappe.new_doc("POS Invoice")
	inv.order_type = order_type
	inv.customer_name = customer_name
	inv.phone = phone
	inv.restaurant_table = restaurant_table if order_type == "Dine-in" else None
	inv.status = status
	inv.kitchen_status = kitchen_status
	inv.payment_method = payment_method or "Cash"
	inv.cash_received = flt(cash_received)
	inv.notes = notes
	inv.cashier = frappe.session.user

	# Get tax rate from settings
	try:
		settings = frappe.get_cached_doc("Candela Settings")
		inv.tax_rate = flt(settings.get("tax_rate")) or 0
	except Exception:
		inv.tax_rate = 0

	for item_data in items:
		menu_item_name = item_data.get("menu_item")
		if not menu_item_name:
			continue
		menu_item = frappe.get_doc("Menu Item", menu_item_name)
		price = flt(menu_item.discounted_price) or flt(menu_item.price)
		qty = cint(item_data.get("quantity", 1))
		inv.append("items", {
			"menu_item": menu_item.name,
			"item_name": menu_item.item_name_en or menu_item.item_name_ar,
			"quantity": qty,
			"unit_price": price,
			"amount": price * qty,
			"special_instructions": item_data.get("special_instructions"),
		})

	inv.insert(ignore_permissions=True)

	# If already paid, submit-like flag
	if status == "Paid":
		inv.db_set("status", "Paid")

	frappe.db.commit()

	# Publish real-time event for kitchen display
	if kitchen_status == "Pending":
		frappe.publish_realtime(
			"new_kitchen_order",
			{"invoice": inv.name, "order_type": order_type, "table": restaurant_table},
		)

	return {
		"success": True,
		"invoice": inv.name,
		"grand_total": inv.grand_total,
		"change_amount": inv.change_amount,
		"items_count": len(inv.items),
	}


# ═══════════════════════════════════════════════════════════════
# Kitchen Display
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist()
def get_kitchen_orders():
	"""Get all active orders for the kitchen display, grouped by status."""
	frappe.only_for(["Candela User", "Candela Manager", "System Manager"])

	result = {"pending": [], "preparing": [], "ready": []}

	# POS Invoice orders
	pos_orders = frappe.get_all(
		"POS Invoice",
		filters={"kitchen_status": ["in", ["Pending", "Preparing", "Ready"]], "status": ["!=", "Cancelled"]},
		fields=["name", "order_type", "restaurant_table", "kitchen_status",
		        "creation", "customer_name", "notes"],
		order_by="creation asc",
	)

	for order in pos_orders:
		order["source"] = "POS"
		order["items"] = frappe.get_all(
			"POS Invoice Item",
			filters={"parent": order.name},
			fields=["item_name", "quantity", "special_instructions"],
			order_by="idx asc",
		)
		order["elapsed"] = (now_datetime() - order.creation).total_seconds()
		key = order.kitchen_status.lower()
		if key in result:
			result[key].append(order)

	# Online orders that are still being prepared
	online_orders = frappe.get_all(
		"Online Order",
		filters={"status": ["in", ["Confirmed", "Preparing", "Ready"]]},
		fields=["name", "order_type", "status", "creation", "customer_name"],
		order_by="creation asc",
	)

	for order in online_orders:
		order["source"] = "Online"
		order["restaurant_table"] = None
		order["items"] = frappe.get_all(
			"Order Item",
			filters={"parent": order.name},
			fields=["item_name", "quantity", "special_instructions"],
			order_by="idx asc",
		)
		order["elapsed"] = (now_datetime() - order.creation).total_seconds()

		# Map online status to kitchen columns
		status_map = {"Confirmed": "pending", "Preparing": "preparing", "Ready": "ready"}
		key = status_map.get(order.status, "pending")
		order["kitchen_status"] = key.capitalize()
		result[key].append(order)

	return result


@frappe.whitelist()
def update_kitchen_status(order_name, source, new_status):
	"""Update the kitchen status of a POS or Online order."""
	frappe.only_for(["Candela Manager", "System Manager"])

	if source == "POS":
		if not frappe.db.exists("POS Invoice", order_name):
			frappe.throw(_("POS Invoice {0} not found").format(order_name))
		frappe.db.set_value("POS Invoice", order_name, "kitchen_status", new_status)

		# If served, it's done
		if new_status == "Served":
			frappe.db.set_value("POS Invoice", order_name, "kitchen_status", "Served")

	elif source == "Online":
		if not frappe.db.exists("Online Order", order_name):
			frappe.throw(_("Online Order {0} not found").format(order_name))

		# Map kitchen status to online order status
		status_map = {
			"Pending": "Confirmed",
			"Preparing": "Preparing",
			"Ready": "Ready",
			"Served": "Ready for Pickup",
		}
		online_status = status_map.get(new_status, new_status)
		frappe.db.set_value("Online Order", order_name, "status", online_status)

	frappe.db.commit()

	# Broadcast real-time update
	frappe.publish_realtime(
		"kitchen_status_changed",
		{"order": order_name, "source": source, "status": new_status},
	)

	return {"success": True}


# ═══════════════════════════════════════════════════════════════
# Table Management
# ═══════════════════════════════════════════════════════════════

@frappe.whitelist()
def update_table_status(table, action):
	"""Update a restaurant table status.

	Actions: free, unavailable, available, seat
	"""
	frappe.only_for(["Candela Manager", "System Manager"])

	if not frappe.db.exists("Restaurant Table", table):
		frappe.throw(_("Table {0} not found").format(table))

	tbl = frappe.get_doc("Restaurant Table", table)

	if action == "free":
		# Mark table as available and close any draft POS invoices
		tbl.is_available = 1
		tbl.save(ignore_permissions=True)
		# Close any draft POS invoices for this table
		open_invoices = frappe.get_all(
			"POS Invoice",
			filters={"restaurant_table": table, "status": "Draft"},
			pluck="name",
		)
		for inv_name in open_invoices:
			frappe.db.set_value("POS Invoice", inv_name, "status", "Cancelled")

	elif action == "unavailable":
		tbl.is_available = 0
		tbl.save(ignore_permissions=True)

	elif action == "available":
		tbl.is_available = 1
		tbl.save(ignore_permissions=True)

	elif action == "seat":
		# Mark table occupied (reserved guest being seated)
		tbl.is_available = 0
		tbl.save(ignore_permissions=True)
		# Seat confirmed reservations for today on this table
		today_res = frappe.get_all(
			"Table Reservation",
			filters={
				"assigned_table": table,
				"reservation_date": today(),
				"status": ["in", ["Confirmed", "Pending"]],
			},
			pluck="name",
			limit=1,
		)
		for res_name in today_res:
			frappe.db.set_value("Table Reservation", res_name, "status", "Seated")

	frappe.db.commit()

	frappe.publish_realtime(
		"table_status_changed",
		{"table": table, "action": action},
	)

	return {"success": True}
