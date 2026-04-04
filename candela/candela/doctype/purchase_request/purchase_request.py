# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
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
