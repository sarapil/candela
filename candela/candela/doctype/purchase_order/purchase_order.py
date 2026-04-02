# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

from frappe.utils import flt
from frappe.model.document import Document


class PurchaseOrder(Document):
	def validate(self):
		for item in self.items:
			item.amount = flt(item.ordered_qty) * flt(item.unit_cost)
		self.total_amount = sum(flt(item.amount) for item in self.items)
