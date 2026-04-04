# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class StockReconciliation(Document):
	def validate(self):
		for item in self.items:
			item.variance = flt(item.counted_qty) - flt(item.system_qty)
			item.variance_pct = (
				(item.variance / item.system_qty * 100) if item.system_qty else 0
			)
			ing_cost = flt(
				frappe.db.get_value("Ingredient", item.ingredient, "cost_per_unit")
			)
			item.variance_cost = abs(item.variance) * ing_cost
		self.total_variance_cost = sum(flt(i.variance_cost) for i in self.items)
