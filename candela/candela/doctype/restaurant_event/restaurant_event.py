# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RestaurantEvent(Document):
	def before_save(self):
		if not self.slug and self.event_name_en:
			self.slug = self.event_name_en.lower().replace(" ", "-").replace("&", "and")
