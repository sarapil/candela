# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

from frappe.utils import flt
from frappe.model.document import Document


class MarketingCampaign(Document):
	def validate(self):
		self.spent = sum(flt(a.cost) for a in (self.activities or []))
		self.total_reach = sum(flt(a.reach) for a in (self.activities or []))
		self.total_engagement = sum(flt(a.engagement) for a in (self.activities or []))
		if self.spent and self.spent > 0 and self.revenue_attributed:
			self.roi_percentage = ((flt(self.revenue_attributed) - self.spent) / self.spent) * 100

