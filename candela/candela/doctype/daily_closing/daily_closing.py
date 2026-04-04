# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class DailyClosing(Document):
	def validate(self):
		self._calc_revenue()
		self._calc_collections()
		self._calc_expenses()
		self._calc_kpis()

	def _calc_revenue(self):
		self.gross_revenue = (
			flt(self.total_dine_in_revenue)
			+ flt(self.total_delivery_revenue)
			+ flt(self.total_takeaway_revenue)
			+ flt(self.other_income)
		)

	def _calc_collections(self):
		self.total_collected = (
			flt(self.cash_collected)
			+ flt(self.card_collected)
			+ flt(self.online_payments)
		)
		self.collection_variance = flt(self.total_collected) - flt(self.gross_revenue)

	def _calc_expenses(self):
		self.total_expenses = sum(flt(e.amount) for e in (self.cash_expenses or []))
		self.net_cash_position = (
			flt(self.opening_cash)
			+ flt(self.cash_collected)
			- flt(self.total_expenses)
			- flt(self.bank_deposit_amount)
		)

	def _calc_kpis(self):
		if self.total_orders and self.total_orders > 0:
			self.average_order_value = flt(self.gross_revenue) / self.total_orders
		if self.gross_revenue and self.gross_revenue > 0:
			self.food_cost_percentage = (flt(self.food_cost_today) / self.gross_revenue) * 100
		if self.covers_count and self.covers_count > 0:
			self.revenue_per_cover = flt(self.gross_revenue) / self.covers_count
