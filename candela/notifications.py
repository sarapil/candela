# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""Candela notification hooks and config."""

import frappe
from frappe import _


def get_notification_config():
	"""Return notification config for Desk sidebar badges."""
	return {
		"for_doctype": {
			"Table Reservation": {"status": "Pending"},
			"Online Order": {"status": ["in", ["Pending", "Confirmed", "Preparing"]]},
			"Customer Review": {"is_approved": 0},
			"POS Invoice": {"status": "Draft"},
		},
	}


def notify_new_reservation(doc, method=None):
	"""Send notification when a new reservation is created."""
	settings = _get_settings()
	if not settings or not settings.notify_new_reservation:
		return

	# Desk notification
	frappe.publish_realtime(
		"candela_new_reservation",
		{
			"name": doc.name,
			"guest_name": doc.guest_name,
			"date": str(doc.reservation_date),
			"time": str(doc.reservation_time),
			"guests": doc.number_of_guests,
		},
		after_commit=True,
	)


def notify_new_order(doc, method=None):
	"""Send notification when a new order is placed."""
	settings = _get_settings()
	if not settings or not settings.notify_new_order:
		return

	frappe.publish_realtime(
		"candela_new_order",
		{
			"name": doc.name,
			"customer": doc.customer_name,
			"type": doc.order_type,
			"total": doc.total,
		},
		after_commit=True,
	)


def notify_order_status_change(doc, method=None):
	"""Notify customer when order status changes."""
	if not doc.has_value_changed("status"):
		return

	frappe.publish_realtime(
		"candela_order_update",
		{
			"name": doc.name,
			"tracking_token": doc.tracking_token,
			"status": doc.status,
			"customer": doc.customer_name,
		},
		after_commit=True,
	)


def notify_new_review(doc, method=None):
	"""Send notification when a new review is submitted."""
	settings = _get_settings()
	if not settings or not settings.notify_new_review:
		return

	frappe.publish_realtime(
		"candela_new_review",
		{
			"name": doc.name,
			"customer": doc.customer_name,
			"rating": doc.rating,
		},
		after_commit=True,
	)


def _get_settings():
	"""Get Candela Settings safely."""
	try:
		return frappe.get_cached_doc("Candela Settings")
	except Exception:
		return None


def notify_new_pos_order(doc, method=None):
	"""Send real-time notification when a new POS order is created for kitchen."""
	frappe.publish_realtime(
		"new_kitchen_order",
		{
			"name": doc.name,
			"order_type": doc.order_type,
			"table": doc.restaurant_table,
			"kitchen_status": doc.kitchen_status,
		},
		after_commit=True,
	)
