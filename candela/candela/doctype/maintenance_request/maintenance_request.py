# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

import frappe
from frappe.utils import flt, time_diff_in_hours, add_days
from frappe.model.document import Document


class MaintenanceRequest(Document):
	def validate(self):
		if self.started_at and self.completed_at:
			self.downtime_hours = round(
				time_diff_in_hours(self.completed_at, self.started_at), 1
			)

	def on_update(self):
		if self.status == "Completed" and self.asset:
			asset = frappe.get_doc("Restaurant Asset", self.asset)
			interval = asset.maintenance_interval_days or 90
			asset.next_maintenance_date = add_days(frappe.utils.today(), interval)
			asset.status = "Active"
			asset.save(ignore_permissions=True)
