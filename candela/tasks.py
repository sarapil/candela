# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""Candela scheduled tasks."""

import frappe
from frappe.utils import today, add_to_date, now_datetime, get_datetime


def mark_past_reservations_completed():
	"""Mark reservations from past dates as Completed (daily)."""
	past_reservations = frappe.get_all(
		"Table Reservation",
		filters={
			"reservation_date": ["<", today()],
			"status": ["in", ["Confirmed", "Seated"]],
		},
		pluck="name",
	)
	for name in past_reservations:
		frappe.db.set_value("Table Reservation", name, "status", "Completed")

	if past_reservations:
		frappe.db.commit()
		frappe.logger("candela").info(
			f"Marked {len(past_reservations)} past reservations as Completed"
		)


def mark_no_show_reservations():
	"""Mark reservations as No-Show if unconfirmed and past time (hourly)."""
	# Reservations that are Pending, date is today, and time is > 1 hour past
	threshold = add_to_date(now_datetime(), hours=-1)
	pending = frappe.get_all(
		"Table Reservation",
		filters={
			"status": "Pending",
			"reservation_date": today(),
		},
		fields=["name", "reservation_time"],
	)
	count = 0
	for r in pending:
		# Compare reservation time with threshold
		try:
			res_dt = get_datetime(f"{today()} {r.reservation_time}")
			if res_dt < threshold:
				frappe.db.set_value("Table Reservation", r.name, "status", "No-Show")
				count += 1
		except Exception:
			pass

	if count:
		frappe.db.commit()
		frappe.logger("candela").info(f"Marked {count} reservations as No-Show")


def deactivate_expired_promos():
	"""Deactivate promo codes past their valid_until date (daily)."""
	expired = frappe.get_all(
		"Promo Code",
		filters={
			"is_active": 1,
			"valid_until": ["<", today()],
		},
		pluck="name",
	)
	for name in expired:
		frappe.db.set_value("Promo Code", name, "is_active", 0)

	if expired:
		frappe.db.commit()
		frappe.logger("candela").info(
			f"Deactivated {len(expired)} expired promo codes"
		)


def check_low_stock_alerts():
	"""Daily: auto-create purchase requests for low-stock ingredients."""
	from candela.governance import check_low_stock_alerts as _check
	_check()


def check_preventive_maintenance():
	"""Daily: auto-create preventive maintenance requests for overdue assets."""
	from candela.governance import check_preventive_maintenance as _check
	_check()


def auto_populate_daily_closing():
	"""Daily (end of day): Pre-populate today's Daily Closing from POS Shifts + Orders."""
	closing_date = today()

	# Skip if already exists
	if frappe.db.exists("Daily Closing", {"closing_date": closing_date}):
		return

	from frappe.utils import flt as _flt

	# Aggregate POS Invoices
	pos_data = frappe.db.sql("""
		SELECT
			SUM(CASE WHEN order_type='Dine-in' THEN grand_total ELSE 0 END) as dine_in,
			SUM(CASE WHEN order_type='Takeaway' THEN grand_total ELSE 0 END) as takeaway,
			SUM(CASE WHEN payment_method='Cash' THEN grand_total ELSE 0 END) as cash,
			SUM(CASE WHEN payment_method='Card' THEN grand_total ELSE 0 END) as card,
			COUNT(*) as cnt
		FROM `tabPOS Invoice`
		WHERE DATE(creation) = %s AND status != 'Cancelled'
	""", closing_date, as_dict=True)

	# Aggregate Online Orders
	online_data = frappe.db.sql("""
		SELECT
			SUM(total) as delivery_total,
			SUM(CASE WHEN payment_method IN ('Paymob','Fawry') THEN total ELSE 0 END) as online_pay,
			COUNT(*) as cnt
		FROM `tabOnline Order`
		WHERE DATE(creation) = %s AND status NOT IN ('Cancelled','Pending')
	""", closing_date, as_dict=True)

	pos = pos_data[0] if pos_data else {}
	online = online_data[0] if online_data else {}

	dc = frappe.new_doc("Daily Closing")
	dc.closing_date = closing_date
	dc.total_dine_in_revenue = _flt(pos.get("dine_in"))
	dc.total_takeaway_revenue = _flt(pos.get("takeaway"))
	dc.total_delivery_revenue = _flt(online.get("delivery_total"))
	dc.cash_collected = _flt(pos.get("cash"))
	dc.card_collected = _flt(pos.get("card"))
	dc.online_payments = _flt(online.get("online_pay"))
	dc.total_orders = int(pos.get("cnt") or 0) + int(online.get("cnt") or 0)
	dc.insert(ignore_permissions=True)
	frappe.db.commit()

