# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MenuCategory(Document):
	def before_save(self):
		if not self.slug and self.category_name_en:
			self.slug = self.category_name_en.lower().replace(" ", "-")
