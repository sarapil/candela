# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class StockEntry(Document):
	def validate(self):
		self.total_cost = flt(self.unit_cost or 0) * flt(self.quantity or 0)

	def on_submit(self):
		self.update_ingredient_stock()

	def after_insert(self):
		self.update_ingredient_stock()

	def update_ingredient_stock(self):
		"""Update the ingredient's current stock based on entry type."""
		if not self.ingredient:
			return

		ingredient = frappe.get_doc("Ingredient", self.ingredient)
		qty = flt(self.quantity)

		if self.entry_type == "Purchase":
			ingredient.current_stock = flt(ingredient.current_stock) + qty
			ingredient.last_purchase_date = self.date
			if self.supplier:
				ingredient.supplier = self.supplier
			if self.unit_cost:
				ingredient.cost_per_unit = self.unit_cost
		elif self.entry_type in ("Consumption", "Waste"):
			ingredient.current_stock = max(0, flt(ingredient.current_stock) - qty)
		elif self.entry_type == "Return":
			ingredient.current_stock = max(0, flt(ingredient.current_stock) - qty)
		elif self.entry_type == "Adjustment":
			ingredient.current_stock = qty  # Set absolute value

		ingredient.save(ignore_permissions=True)

		# Alert if low stock
		if ingredient.is_low_stock:
			frappe.publish_realtime(
				"low_stock_alert",
				{"ingredient": ingredient.ingredient_name, "current": ingredient.current_stock, "minimum": ingredient.minimum_stock},
			)
