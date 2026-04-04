# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
import uuid
from frappe.model.document import Document


class OnlineOrder(Document):
	def before_insert(self):
		if not self.tracking_token:
			self.tracking_token = str(uuid.uuid4())[:8].upper()

	def validate(self):
		self.calculate_totals()

	def calculate_totals(self):
		self.subtotal = 0
		for item in self.items:
			item.amount = (item.unit_price or 0) * (item.quantity or 0)
			self.subtotal += item.amount
		self.total = self.subtotal - (self.discount_amount or 0) + (self.delivery_fee or 0)
