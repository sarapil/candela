# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class Ingredient(Document):
	def validate(self):
		if flt(self.current_stock) < 0:
			self.current_stock = 0

	@property
	def is_low_stock(self):
		return flt(self.current_stock) <= flt(self.minimum_stock) and flt(self.minimum_stock) > 0
