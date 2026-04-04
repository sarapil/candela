# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class MenuItem(Document):
	def before_save(self):
		if not self.slug and self.item_name_en:
			self.slug = self.item_name_en.lower().replace(" ", "-").replace("'", "")

	def validate(self):
		self._enforce_recipe_requirement()
		self._calculate_food_cost()

	def _enforce_recipe_requirement(self):
		"""GOVERNANCE: No item can be active for sale without a recipe."""
		if self.is_available and not self.recipe_items:
			frappe.msgprint(
				_("Warning: '{0}' has no recipe. Add ingredients in the Recipe tab for proper cost tracking.").format(
					self.item_name_en
				),
				indicator="orange",
			)

	def _calculate_food_cost(self):
		"""Auto-calculate food cost from recipe ingredients."""
		if not self.recipe_items:
			return
		total_cost = 0
		for row in self.recipe_items:
			row.total_cost = (row.quantity_per_serving or 0) * (row.cost_per_unit or 0)
			total_cost += row.total_cost
		self.food_cost = total_cost
		if self.price and self.price > 0:
			self.food_cost_percentage = (total_cost / self.price) * 100
		# Alert if food cost exceeds target
		if (
			self.target_food_cost_pct
			and self.food_cost_percentage
			and self.food_cost_percentage > self.target_food_cost_pct
		):
			frappe.msgprint(
				_("⚠️ Food cost {0}% exceeds target {1}%").format(
					round(self.food_cost_percentage, 1),
					round(self.target_food_cost_pct, 1),
				),
				indicator="orange",
			)
