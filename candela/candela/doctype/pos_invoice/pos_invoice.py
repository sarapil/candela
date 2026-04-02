# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class POSInvoice(Document):
	def validate(self):
		self.calculate_totals()
		self.cashier = self.cashier or frappe.session.user

	def calculate_totals(self):
		self.subtotal = 0
		for item in self.items:
			item.amount = flt(item.unit_price or 0) * flt(item.quantity or 0)
			self.subtotal += item.amount

		# Apply percentage discount
		if flt(self.discount_percentage) > 0:
			self.discount_amount = flt(self.subtotal) * flt(self.discount_percentage) / 100

		taxable = flt(self.subtotal) - flt(self.discount_amount)
		self.tax_amount = taxable * flt(self.tax_rate or 0) / 100
		self.grand_total = taxable + flt(self.tax_amount)

		# Calculate change
		if flt(self.cash_received) > 0:
			self.change_amount = flt(self.cash_received) - flt(self.grand_total)
			if self.change_amount < 0:
				self.change_amount = 0

	def on_update(self):
		"""Send kitchen status updates via realtime."""
		frappe.publish_realtime(
			"pos_invoice_updated",
			{"name": self.name, "status": self.status, "kitchen_status": self.kitchen_status},
			doctype="POS Invoice",
			docname=self.name,
		)
