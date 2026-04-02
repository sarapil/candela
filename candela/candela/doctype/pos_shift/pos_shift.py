# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class POSShift(Document):
	def validate(self):
		self.total_sales = (
			flt(self.total_cash_sales)
			+ flt(self.total_card_sales)
			+ flt(self.total_wallet_sales)
		)
		self.expected_cash = (
			flt(self.opening_cash)
			+ flt(self.total_cash_sales)
			- flt(self.total_refunds)
		)
		if self.closing_cash is not None:
			self.cash_variance = flt(self.closing_cash) - flt(self.expected_cash)
