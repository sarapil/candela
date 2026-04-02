# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from frappe.model.document import Document


class PurchaseRequest(Document):
	def validate(self):
		self.calculate_totals()

	def calculate_totals(self):
		self.total_estimated_cost = sum(flt(item.estimated_cost) for item in self.items)

