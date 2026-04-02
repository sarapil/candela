import frappe
from candela.utils import (
	get_candela_settings, get_gallery_images,
	get_lang, is_rtl
)

no_cache = 1

def get_context(context):
	context.no_cache = 1
	context.show_sidebar = False
	context.title = "Gallery – Candela"
	context.candela = get_candela_settings()
	context.candela_lang = get_lang()
	context.candela_rtl = is_rtl()
	context.images = get_gallery_images()
	context.get_candela_settings = get_candela_settings
