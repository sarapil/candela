# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

from frappe.utils import flt
from frappe.model.document import Document


class GoodsReceiptNote(Document):
	def validate(self):
		for item in self.items:
			item.accepted_qty = flt(item.accepted_qty) or flt(item.received_qty)
			item.rejected_qty = flt(item.received_qty) - flt(item.accepted_qty)
		self.total_cost = sum(
			flt(item.accepted_qty) * flt(item.unit_cost) for item in self.items
		)
