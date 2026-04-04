# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""Candela website context overrides."""

import frappe


def update_website_context(context):
	"""Add Candela-specific context to all website pages."""
	try:
		settings = frappe.get_cached_doc("Candela Settings")
	except Exception:
		return

	# Determine if current page is a Candela page
	path = frappe.local.request.path if hasattr(frappe.local, "request") and frappe.local.request else ""
	is_candela_page = path.startswith("/dela") or path.startswith("/deladmin")

	if is_candela_page:
		context.candela = settings
		context.is_candela_page = True

		# Set direction for RTL
		lang = settings.default_language or "ar"
		context.candela_lang = lang
		context.candela_dir = "rtl" if lang in ("ar", "he", "fa") else "ltr"

		# SEO defaults
		if not context.get("title"):
			context.title = settings.restaurant_name or "Candela"
		if settings.meta_description and not context.get("description"):
			context.description = settings.meta_description
