# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

from frappe.utils import flt
from frappe.model.document import Document


class Influencer(Document):
	def validate(self):
		self.total_reach = sum(flt(v.estimated_reach) for v in (self.invitations or []))
		self.total_cost = sum(flt(v.cost) for v in (self.invitations or []))
		if self.total_cost and self.total_cost > 0:
			self.roi_score = round(self.total_reach / self.total_cost, 2)
