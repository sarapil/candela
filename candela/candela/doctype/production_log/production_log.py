# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, time_diff_in_seconds
from frappe.model.document import Document


class ProductionLog(Document):
	def validate(self):
		self._calc_prep_time()
		self._calc_waste_cost()

	def _calc_prep_time(self):
		if self.started_at and self.completed_at:
			diff = time_diff_in_seconds(self.completed_at, self.started_at)
			self.prep_time_minutes = round(diff / 60, 1)
			if self.estimated_prep_time and self.estimated_prep_time > 0:
				self.time_variance_pct = (
					(self.prep_time_minutes - self.estimated_prep_time)
					/ self.estimated_prep_time
				) * 100

	def _calc_waste_cost(self):
		for w in (self.waste_items or []):
			cost_per_unit = flt(
				frappe.db.get_value("Ingredient", w.ingredient, "cost_per_unit")
			)
			w.cost = flt(w.wasted_qty) * cost_per_unit
		self.total_waste_cost = sum(flt(w.cost) for w in (self.waste_items or []))
