"""
Script to generate all Candela DocType JSON and Python files.
Run from: /workspace/development/frappe-bench/apps/candela/
"""
import json
import os

BASE = "/workspace/development/frappe-bench/apps/candela/candela/candela/doctype"

def write_doctype(name, fields, **kwargs):
    """Write DocType JSON and Python files."""
    folder_name = name.lower().replace(" ", "_")
    folder_path = os.path.join(BASE, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Write __init__.py
    with open(os.path.join(folder_path, "__init__.py"), "w") as f:
        f.write("")

    # Build JSON
    doc = {
        "actions": [],
        "autoname": kwargs.get("autoname", ""),
        "creation": "2026-03-19 10:00:00.000000",
        "doctype": "DocType",
        "engine": "InnoDB",
        "field_order": [f["fieldname"] for f in fields],
        "fields": fields,
        "index_web_pages_for_search": 1 if kwargs.get("has_web_view") else 0,
        "issingle": 1 if kwargs.get("issingle") else 0,
        "istable": 1 if kwargs.get("istable") else 0,
        "links": [],
        "modified": "2026-03-19 10:00:00.000000",
        "modified_by": "Administrator",
        "module": "Candela",
        "name": name,
        "naming_rule": kwargs.get("naming_rule", "By fieldname"),
        "owner": "Administrator",
        "permissions": kwargs.get("permissions", [
            {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "System Manager", "share": 1, "write": 1},
            {"create": 1, "delete": 1, "email": 1, "export": 1, "print": 1, "read": 1, "report": 1, "role": "Candela Manager", "share": 1, "write": 1},
        ]),
        "sort_field": kwargs.get("sort_field", "creation"),
        "sort_order": "DESC",
        "states": [],
        "track_changes": 1,
    }

    if kwargs.get("issingle"):
        doc["naming_rule"] = ""
        doc["autoname"] = ""

    if kwargs.get("istable"):
        doc["permissions"] = []
        doc["naming_rule"] = ""
        doc["autoname"] = ""

    if kwargs.get("description"):
        doc["description"] = kwargs["description"]

    json_path = os.path.join(folder_path, f"{folder_name}.json")
    with open(json_path, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)

    # Write Python controller
    class_name = name.replace(" ", "")
    py_path = os.path.join(folder_path, f"{folder_name}.py")
    py_content = kwargs.get("py_content", f'''# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class {class_name}(Document):
\tpass
''')
    with open(py_path, "w") as f:
        f.write(py_content)

    # Write JS if needed
    if kwargs.get("js_content"):
        js_path = os.path.join(folder_path, f"{folder_name}.js")
        with open(js_path, "w") as f:
            f.write(kwargs["js_content"])

    print(f"  ✓ {name}")


def sb(label=""):
    return {"fieldname": f"sb_{label.lower().replace(' ', '_') if label else 'main'}", "fieldtype": "Section Break", "label": label}

def cb():
    return {"fieldname": f"cb_{id(object())}", "fieldtype": "Column Break"}

def tab(label):
    return {"fieldname": f"tab_{label.lower().replace(' ', '_').replace('&', 'and')}", "fieldtype": "Tab Break", "label": label}

# ═══════════════════════════════════════════════════
# CHILD TABLES
# ═══════════════════════════════════════════════════

print("Creating child tables...")

# Opening Hours (already created, skip)

# Menu Item Dietary Tag
write_doctype("Menu Item Dietary Tag", [
    {"fieldname": "dietary_tag", "fieldtype": "Select", "in_list_view": 1, "label": "Dietary Tag",
     "options": "Vegetarian\nVegan\nGluten-Free\nSpicy\nContains Nuts\nDairy-Free\nHalal", "reqd": 1},
], istable=True)

# Order Item
write_doctype("Order Item", [
    {"fieldname": "menu_item", "fieldtype": "Link", "in_list_view": 1, "label": "Menu Item", "options": "Menu Item", "reqd": 1},
    {"fieldname": "item_name", "fieldtype": "Data", "in_list_view": 1, "label": "Item Name", "fetch_from": "menu_item.item_name_en", "read_only": 1},
    {"fieldname": "quantity", "fieldtype": "Int", "in_list_view": 1, "label": "Quantity", "reqd": 1, "default": "1", "non_negative": 1},
    {"fieldname": "unit_price", "fieldtype": "Currency", "in_list_view": 1, "label": "Unit Price", "fetch_from": "menu_item.price", "read_only": 1},
    {"fieldname": "amount", "fieldtype": "Currency", "in_list_view": 1, "label": "Amount", "read_only": 1},
    {"fieldname": "special_instructions", "fieldtype": "Small Text", "label": "Special Instructions"},
], istable=True)

# ═══════════════════════════════════════════════════
# CANDELA SETTINGS (SINGLETON)
# ═══════════════════════════════════════════════════

print("Creating Candela Settings...")

settings_fields = [
    # TAB 1: BRANDING
    tab("Branding"),
    sb("Restaurant Identity"),
    {"fieldname": "restaurant_name", "fieldtype": "Data", "label": "Restaurant Name", "default": "Candela", "reqd": 1},
    {"fieldname": "restaurant_name_ar", "fieldtype": "Data", "label": "Restaurant Name (Arabic)", "default": "كانديلا"},
    cb(),
    {"fieldname": "tagline_ar", "fieldtype": "Data", "label": "Tagline (Arabic)", "default": "فن المطبخ الإيطالي الأصيل"},
    {"fieldname": "tagline_en", "fieldtype": "Data", "label": "Tagline (English)", "default": "The Art of Authentic Italian Cuisine"},
    {"fieldname": "tagline_it", "fieldtype": "Data", "label": "Tagline (Italian)", "default": "L'arte della cucina italiana"},

    sb("Logo & Icons"),
    {"fieldname": "logo_dark", "fieldtype": "Attach Image", "label": "Logo (Dark - for light backgrounds)"},
    {"fieldname": "logo_white", "fieldtype": "Attach Image", "label": "Logo (White - for dark backgrounds)"},
    {"fieldname": "logo_gold", "fieldtype": "Attach Image", "label": "Logo (Gold)"},
    cb(),
    {"fieldname": "logo_icon", "fieldtype": "Attach Image", "label": "Logo Icon (circular)"},
    {"fieldname": "favicon", "fieldtype": "Attach Image", "label": "Favicon"},

    sb("Brand Colors"),
    {"fieldname": "color_primary", "fieldtype": "Color", "label": "Primary Color (Amber)", "default": "#E8A521"},
    {"fieldname": "color_dark", "fieldtype": "Color", "label": "Dark Color", "default": "#2A2A2A"},
    cb(),
    {"fieldname": "color_green", "fieldtype": "Color", "label": "Green Color", "default": "#5BB369"},
    {"fieldname": "color_accent", "fieldtype": "Color", "label": "Accent Color", "default": "#EEC621"},

    # TAB 2: WEBSITE CONTENT
    tab("Website Content"),
    sb("Hero Section"),
    {"fieldname": "hero_image", "fieldtype": "Attach Image", "label": "Hero Background Image"},
    {"fieldname": "hero_image_mobile", "fieldtype": "Attach Image", "label": "Hero Image (Mobile)"},
    {"fieldname": "hero_overlay_opacity", "fieldtype": "Percent", "label": "Hero Overlay Opacity", "default": "70"},
    {"fieldname": "hero_video_url", "fieldtype": "Data", "label": "Hero Video URL"},
    cb(),
    {"fieldname": "show_hero_logo", "fieldtype": "Check", "label": "Show Animated Logo in Hero", "default": "1"},
    {"fieldname": "hero_cta_primary_text", "fieldtype": "Data", "label": "Primary CTA Text", "default": "احجز طاولة"},
    {"fieldname": "hero_cta_primary_url", "fieldtype": "Data", "label": "Primary CTA URL", "default": "/dela/reservation"},
    {"fieldname": "hero_cta_secondary_text", "fieldtype": "Data", "label": "Secondary CTA Text", "default": "استكشف المنيو"},
    {"fieldname": "hero_cta_secondary_url", "fieldtype": "Data", "label": "Secondary CTA URL", "default": "/dela/menu"},

    sb("About Section"),
    {"fieldname": "about_image", "fieldtype": "Attach Image", "label": "About Image"},
    {"fieldname": "about_title_ar", "fieldtype": "Data", "label": "About Title (Arabic)", "default": "قصتنا"},
    {"fieldname": "about_title_en", "fieldtype": "Data", "label": "About Title (English)", "default": "Our Story"},
    cb(),
    {"fieldname": "about_text_ar", "fieldtype": "Text Editor", "label": "About Text (Arabic)"},
    {"fieldname": "about_text_en", "fieldtype": "Text Editor", "label": "About Text (English)"},

    sb("Homepage Sections"),
    {"fieldname": "show_about_section", "fieldtype": "Check", "label": "Show About Section", "default": "1"},
    {"fieldname": "show_menu_highlights", "fieldtype": "Check", "label": "Show Menu Highlights", "default": "1"},
    {"fieldname": "show_reservation_cta", "fieldtype": "Check", "label": "Show Reservation CTA", "default": "1"},
    cb(),
    {"fieldname": "show_testimonials", "fieldtype": "Check", "label": "Show Testimonials", "default": "1"},
    {"fieldname": "show_events", "fieldtype": "Check", "label": "Show Events", "default": "1"},
    {"fieldname": "show_gallery", "fieldtype": "Check", "label": "Show Gallery", "default": "1"},
    {"fieldname": "show_newsletter", "fieldtype": "Check", "label": "Show Newsletter", "default": "1"},
    {"fieldname": "show_instagram_feed", "fieldtype": "Check", "label": "Show Instagram Feed", "default": "0"},

    sb("Custom Banner"),
    {"fieldname": "custom_banner_image", "fieldtype": "Attach Image", "label": "Banner Image"},
    {"fieldname": "custom_banner_text_ar", "fieldtype": "Data", "label": "Banner Text (Arabic)"},
    {"fieldname": "custom_banner_text_en", "fieldtype": "Data", "label": "Banner Text (English)"},

    # TAB 3: CONTACT & LOCATION
    tab("Contact & Location"),
    sb("Contact Info"),
    {"fieldname": "phone", "fieldtype": "Data", "label": "Phone"},
    {"fieldname": "phone_secondary", "fieldtype": "Data", "label": "Secondary Phone"},
    {"fieldname": "whatsapp_number", "fieldtype": "Data", "label": "WhatsApp Number"},
    cb(),
    {"fieldname": "whatsapp_default_message", "fieldtype": "Data", "label": "WhatsApp Default Message"},
    {"fieldname": "email", "fieldtype": "Data", "label": "Email", "options": "Email"},

    sb("Address"),
    {"fieldname": "address_ar", "fieldtype": "Small Text", "label": "Address (Arabic)"},
    {"fieldname": "address_en", "fieldtype": "Small Text", "label": "Address (English)"},
    cb(),
    {"fieldname": "google_maps_embed", "fieldtype": "Code", "label": "Google Maps Embed Code", "options": "HTML"},
    {"fieldname": "google_maps_url", "fieldtype": "Data", "label": "Google Maps URL"},
    {"fieldname": "latitude", "fieldtype": "Float", "label": "Latitude"},
    {"fieldname": "longitude", "fieldtype": "Float", "label": "Longitude"},

    sb("Social Media"),
    {"fieldname": "instagram_url", "fieldtype": "Data", "label": "Instagram"},
    {"fieldname": "facebook_url", "fieldtype": "Data", "label": "Facebook"},
    {"fieldname": "tiktok_url", "fieldtype": "Data", "label": "TikTok"},
    cb(),
    {"fieldname": "twitter_url", "fieldtype": "Data", "label": "Twitter / X"},
    {"fieldname": "youtube_url", "fieldtype": "Data", "label": "YouTube"},
    {"fieldname": "snapchat_url", "fieldtype": "Data", "label": "Snapchat"},

    sb("Opening Hours"),
    {"fieldname": "opening_hours", "fieldtype": "Table", "label": "Opening Hours", "options": "Opening Hours"},

    # TAB 4: FEATURES & ORDERING
    tab("Features & Ordering"),
    sb("Feature Toggles"),
    {"fieldname": "enable_online_ordering", "fieldtype": "Check", "label": "Enable Online Ordering", "default": "0"},
    {"fieldname": "enable_reservations", "fieldtype": "Check", "label": "Enable Reservations", "default": "1"},
    {"fieldname": "enable_reviews", "fieldtype": "Check", "label": "Enable Reviews", "default": "1"},
    {"fieldname": "enable_newsletter", "fieldtype": "Check", "label": "Enable Newsletter", "default": "1"},
    cb(),
    {"fieldname": "enable_whatsapp_button", "fieldtype": "Check", "label": "Enable WhatsApp Button", "default": "1"},
    {"fieldname": "enable_delivery", "fieldtype": "Check", "label": "Enable Delivery", "default": "0"},
    {"fieldname": "enable_pickup", "fieldtype": "Check", "label": "Enable Pickup", "default": "1"},
    {"fieldname": "enable_promo_codes", "fieldtype": "Check", "label": "Enable Promo Codes", "default": "0"},

    sb("Ordering Settings"),
    {"fieldname": "minimum_order_amount", "fieldtype": "Currency", "label": "Minimum Order Amount"},
    {"fieldname": "delivery_fee_default", "fieldtype": "Currency", "label": "Default Delivery Fee"},
    {"fieldname": "estimated_delivery_min", "fieldtype": "Int", "label": "Estimated Delivery (minutes)"},
    cb(),
    {"fieldname": "order_confirmation_msg", "fieldtype": "Small Text", "label": "Order Confirmation Message"},
    {"fieldname": "kitchen_notification_email", "fieldtype": "Data", "label": "Kitchen Notification Email", "options": "Email"},

    sb("Reservation Settings"),
    {"fieldname": "max_party_size", "fieldtype": "Int", "label": "Max Party Size", "default": "20"},
    {"fieldname": "reservation_slot_minutes", "fieldtype": "Int", "label": "Slot Duration (minutes)", "default": "30"},
    cb(),
    {"fieldname": "advance_booking_days", "fieldtype": "Int", "label": "Advance Booking (days)", "default": "30"},
    {"fieldname": "auto_confirm", "fieldtype": "Check", "label": "Auto-Confirm Reservations", "default": "0"},

    # TAB 5: PAYMENTS
    tab("Payments"),
    sb("Payment Methods"),
    {"fieldname": "enable_cash_on_delivery", "fieldtype": "Check", "label": "Cash on Delivery", "default": "1"},
    {"fieldname": "enable_paymob", "fieldtype": "Check", "label": "Enable Paymob", "default": "0"},
    {"fieldname": "enable_fawry", "fieldtype": "Check", "label": "Enable Fawry", "default": "0"},

    sb("Paymob Configuration"),
    {"fieldname": "paymob_api_key", "fieldtype": "Password", "label": "Paymob API Key", "depends_on": "enable_paymob"},
    {"fieldname": "paymob_integration_id", "fieldtype": "Data", "label": "Paymob Integration ID", "depends_on": "enable_paymob"},
    cb(),
    {"fieldname": "paymob_iframe_id", "fieldtype": "Data", "label": "Paymob iFrame ID", "depends_on": "enable_paymob"},
    {"fieldname": "paymob_hmac_secret", "fieldtype": "Password", "label": "Paymob HMAC Secret", "depends_on": "enable_paymob"},

    sb("Fawry Configuration"),
    {"fieldname": "fawry_merchant_code", "fieldtype": "Data", "label": "Fawry Merchant Code", "depends_on": "enable_fawry"},
    {"fieldname": "fawry_security_key", "fieldtype": "Password", "label": "Fawry Security Key", "depends_on": "enable_fawry"},

    # TAB 6: SEO & ANALYTICS
    tab("SEO & Analytics"),
    sb("SEO"),
    {"fieldname": "meta_title", "fieldtype": "Data", "label": "Meta Title"},
    {"fieldname": "meta_description", "fieldtype": "Small Text", "label": "Meta Description"},
    {"fieldname": "meta_keywords", "fieldtype": "Data", "label": "Meta Keywords"},
    cb(),
    {"fieldname": "og_image", "fieldtype": "Attach Image", "label": "OG Image (1200×630)"},
    {"fieldname": "structured_data_type", "fieldtype": "Select", "label": "Schema Type", "options": "\nRestaurant\nCafeOrCoffeeShop"},
    {"fieldname": "schema_price_range", "fieldtype": "Data", "label": "Price Range", "default": "$$"},

    sb("Analytics"),
    {"fieldname": "ga_tracking_id", "fieldtype": "Data", "label": "Google Analytics 4 ID"},
    {"fieldname": "meta_pixel_id", "fieldtype": "Data", "label": "Meta Pixel ID"},
    cb(),
    {"fieldname": "tiktok_pixel_id", "fieldtype": "Data", "label": "TikTok Pixel ID"},
    {"fieldname": "google_tag_manager_id", "fieldtype": "Data", "label": "GTM Container ID"},

    # TAB 7: ADVANCED
    tab("Advanced"),
    sb("Domain & Login"),
    {"fieldname": "candela_domain", "fieldtype": "Data", "label": "Candela Domain",
     "description": "Domain for custom login (e.g. candela.restaurant). Leave empty to disable custom login."},
    {"fieldname": "enable_custom_login", "fieldtype": "Check", "label": "Enable Custom Login", "default": "1"},
    cb(),
    {"fieldname": "login_background_image", "fieldtype": "Attach Image", "label": "Login Background Image"},
    {"fieldname": "login_welcome_text_ar", "fieldtype": "Data", "label": "Login Welcome (Arabic)", "default": "مرحباً بك في كانديلا"},
    {"fieldname": "login_welcome_text_en", "fieldtype": "Data", "label": "Login Welcome (English)", "default": "Welcome to Candela"},

    sb("Language & Locale"),
    {"fieldname": "default_language", "fieldtype": "Select", "label": "Default Language", "options": "ar\nen\nit", "default": "ar"},
    {"fieldname": "enable_english", "fieldtype": "Check", "label": "Enable English", "default": "1"},
    {"fieldname": "enable_italian", "fieldtype": "Check", "label": "Enable Italian", "default": "0"},
    cb(),
    {"fieldname": "currency_symbol", "fieldtype": "Data", "label": "Currency Symbol", "default": "ج.م"},
    {"fieldname": "currency_code", "fieldtype": "Data", "label": "Currency Code", "default": "EGP"},

    sb("Notifications"),
    {"fieldname": "notify_new_reservation", "fieldtype": "Check", "label": "Notify New Reservation", "default": "1"},
    {"fieldname": "notify_new_order", "fieldtype": "Check", "label": "Notify New Order", "default": "1"},
    {"fieldname": "notify_new_review", "fieldtype": "Check", "label": "Notify New Review", "default": "1"},
    cb(),
    {"fieldname": "notification_email", "fieldtype": "Data", "label": "Notification Email", "options": "Email"},
    {"fieldname": "whatsapp_notify_staff", "fieldtype": "Check", "label": "WhatsApp Notify Staff", "default": "0"},

    sb("Demo Data"),
    {"fieldname": "demo_data_installed", "fieldtype": "Check", "label": "Demo Data Installed", "read_only": 1, "default": "0"},
    {"fieldname": "demo_installed_on", "fieldtype": "Datetime", "label": "Demo Installed On", "read_only": 1},

    sb("Maintenance"),
    {"fieldname": "maintenance_mode", "fieldtype": "Check", "label": "Maintenance Mode", "default": "0"},
    {"fieldname": "maintenance_message", "fieldtype": "Small Text", "label": "Maintenance Message"},
    cb(),
    {"fieldname": "custom_css", "fieldtype": "Code", "label": "Custom CSS", "options": "CSS"},
    {"fieldname": "custom_js", "fieldtype": "Code", "label": "Custom JS", "options": "JS"},
    {"fieldname": "custom_head_html", "fieldtype": "Code", "label": "Custom Head HTML", "options": "HTML"},
]

# Fix column breaks to have unique fieldnames
cb_counter = [0]
for f in settings_fields:
    if f["fieldtype"] == "Column Break":
        cb_counter[0] += 1
        f["fieldname"] = f"cb_{cb_counter[0]}"

write_doctype("Candela Settings", settings_fields,
    issingle=True,
    description="Central configuration for Candela Restaurant website and operations.",
    permissions=[
        {"create": 1, "read": 1, "write": 1, "role": "System Manager"},
        {"create": 1, "read": 1, "write": 1, "role": "Candela Manager"},
        {"read": 1, "role": "Candela Staff"},
    ],
    js_content="""// Copyright (c) 2026, Arkan Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Candela Settings', {
    refresh(frm) {
        // Install Demo Data button
        if (!frm.doc.demo_data_installed) {
            frm.add_custom_button(__('Install Demo Data'), function() {
                frappe.confirm(
                    __('This will add demo menu items, gallery photos, events, and reviews. Continue?'),
                    function() {
                        frappe.call({
                            method: 'candela.demo.load_demo_data',
                            freeze: true,
                            freeze_message: __('Installing demo data...'),
                            callback: function(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint({
                                        title: __('Demo Data Installed'),
                                        message: r.message.message,
                                        indicator: 'green'
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __('Demo'));
        }

        // Remove Demo Data button
        if (frm.doc.demo_data_installed) {
            frm.add_custom_button(__('Remove Demo Data'), function() {
                frappe.confirm(
                    __('This will permanently delete ALL demo data. Your real data will NOT be affected. Continue?'),
                    function() {
                        frappe.call({
                            method: 'candela.demo.purge_demo_data',
                            freeze: true,
                            freeze_message: __('Removing demo data...'),
                            callback: function(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint({
                                        title: __('Demo Data Removed'),
                                        message: r.message.message,
                                        indicator: 'orange'
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __('Demo'));
        }

        // Quick links
        frm.add_custom_button(__('View Website'), function() {
            window.open('/dela', '_blank');
        });
    }
});
""")

# ═══════════════════════════════════════════════════
# MENU CATEGORY
# ═══════════════════════════════════════════════════

print("Creating Menu Category...")

write_doctype("Menu Category", [
    {"fieldname": "category_name_ar", "fieldtype": "Data", "label": "Category Name (Arabic)", "reqd": 1},
    {"fieldname": "category_name_en", "fieldtype": "Data", "label": "Category Name (English)", "reqd": 1, "unique": 1},
    {"fieldname": "category_name_it", "fieldtype": "Data", "label": "Category Name (Italian)"},
    {"fieldname": "slug", "fieldtype": "Data", "label": "Slug", "unique": 1},
    cb(),
    {"fieldname": "icon_emoji", "fieldtype": "Data", "label": "Icon Emoji"},
    {"fieldname": "image", "fieldtype": "Attach Image", "label": "Image"},
    {"fieldname": "description_ar", "fieldtype": "Small Text", "label": "Description (Arabic)"},
    {"fieldname": "description_en", "fieldtype": "Small Text", "label": "Description (English)"},
    {"fieldname": "sort_order", "fieldtype": "Int", "label": "Sort Order", "default": "0"},
    {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
    {"fieldname": "show_on_homepage", "fieldtype": "Check", "label": "Show on Homepage", "default": "0"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="field:category_name_en",
    naming_rule="By fieldname",
    sort_field="sort_order",
    py_content='''# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MenuCategory(Document):
\tdef before_save(self):
\t\tif not self.slug and self.category_name_en:
\t\t\tself.slug = self.category_name_en.lower().replace(" ", "-")
''')

# ═══════════════════════════════════════════════════
# MENU ITEM
# ═══════════════════════════════════════════════════

print("Creating Menu Item...")

write_doctype("Menu Item", [
    {"fieldname": "item_name_ar", "fieldtype": "Data", "label": "Item Name (Arabic)", "reqd": 1},
    {"fieldname": "item_name_en", "fieldtype": "Data", "label": "Item Name (English)", "reqd": 1, "unique": 1},
    {"fieldname": "item_name_it", "fieldtype": "Data", "label": "Item Name (Italian)"},
    {"fieldname": "slug", "fieldtype": "Data", "label": "Slug", "unique": 1},
    {"fieldname": "category", "fieldtype": "Link", "label": "Category", "options": "Menu Category", "reqd": 1, "in_standard_filter": 1},
    sb("Details"),
    {"fieldname": "description_ar", "fieldtype": "Text Editor", "label": "Description (Arabic)"},
    {"fieldname": "description_en", "fieldtype": "Text Editor", "label": "Description (English)"},
    sb("Pricing"),
    {"fieldname": "price", "fieldtype": "Currency", "label": "Price (EGP)", "reqd": 1, "in_list_view": 1},
    {"fieldname": "discounted_price", "fieldtype": "Currency", "label": "Discounted Price"},
    sb("Media"),
    {"fieldname": "image", "fieldtype": "Attach Image", "label": "Image"},
    {"fieldname": "image_alt_text", "fieldtype": "Data", "label": "Image Alt Text"},
    sb("Attributes"),
    {"fieldname": "dietary_tags", "fieldtype": "Table", "label": "Dietary Tags", "options": "Menu Item Dietary Tag"},
    {"fieldname": "spice_level", "fieldtype": "Select", "label": "Spice Level", "options": "\nMild\nMedium\nHot"},
    {"fieldname": "preparation_time_min", "fieldtype": "Int", "label": "Prep Time (minutes)"},
    {"fieldname": "calories", "fieldtype": "Int", "label": "Calories"},
    sb("Flags"),
    {"fieldname": "is_available", "fieldtype": "Check", "label": "Available", "default": "1", "in_list_view": 1},
    {"fieldname": "is_featured", "fieldtype": "Check", "label": "Featured", "default": "0", "in_list_view": 1},
    {"fieldname": "is_new", "fieldtype": "Check", "label": "New", "default": "0"},
    cb(),
    {"fieldname": "is_bestseller", "fieldtype": "Check", "label": "Bestseller", "default": "0"},
    {"fieldname": "available_for_delivery", "fieldtype": "Check", "label": "Available for Delivery", "default": "1"},
    {"fieldname": "sort_order", "fieldtype": "Int", "label": "Sort Order"},
    sb("SEO"),
    {"fieldname": "meta_title", "fieldtype": "Data", "label": "Meta Title"},
    {"fieldname": "meta_description", "fieldtype": "Small Text", "label": "Meta Description"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="field:item_name_en",
    naming_rule="By fieldname",
    sort_field="sort_order",
    py_content='''# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MenuItem(Document):
\tdef before_save(self):
\t\tif not self.slug and self.item_name_en:
\t\t\tself.slug = self.item_name_en.lower().replace(" ", "-").replace("'", "")
''',
    js_content="""// Copyright (c) 2026, Arkan Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Menu Item', {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.slug) {
            frm.add_custom_button(__('View on Website'), function() {
                window.open('/dela/menu/' + frm.doc.slug, '_blank');
            });
        }
    }
});
""")

# ═══════════════════════════════════════════════════
# RESTAURANT TABLE
# ═══════════════════════════════════════════════════

print("Creating Restaurant Table...")

write_doctype("Restaurant Table", [
    {"fieldname": "table_number", "fieldtype": "Data", "label": "Table Number", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "section", "fieldtype": "Select", "label": "Section", "options": "Indoor\nOutdoor\nPrivate Room\nBar", "in_list_view": 1},
    {"fieldname": "capacity", "fieldtype": "Int", "label": "Capacity", "reqd": 1, "in_list_view": 1},
    {"fieldname": "is_available", "fieldtype": "Check", "label": "Available", "default": "1", "in_list_view": 1},
    {"fieldname": "is_combinable", "fieldtype": "Check", "label": "Can Combine", "default": "0"},
    {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
],
    autoname="field:table_number",
    naming_rule="By fieldname",
)

# ═══════════════════════════════════════════════════
# TABLE RESERVATION
# ═══════════════════════════════════════════════════

print("Creating Table Reservation...")

write_doctype("Table Reservation", [
    {"fieldname": "guest_name", "fieldtype": "Data", "label": "Guest Name", "reqd": 1, "in_list_view": 1},
    {"fieldname": "phone", "fieldtype": "Data", "label": "Phone", "reqd": 1, "in_list_view": 1},
    {"fieldname": "email", "fieldtype": "Data", "label": "Email", "options": "Email"},
    {"fieldname": "reservation_date", "fieldtype": "Date", "label": "Date", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
    {"fieldname": "reservation_time", "fieldtype": "Time", "label": "Time", "reqd": 1, "in_list_view": 1},
    {"fieldname": "number_of_guests", "fieldtype": "Int", "label": "Guests", "reqd": 1, "in_list_view": 1},
    sb("Preferences"),
    {"fieldname": "occasion", "fieldtype": "Select", "label": "Occasion", "options": "None\nBirthday\nAnniversary\nBusiness\nDate Night\nOther"},
    {"fieldname": "seating_preference", "fieldtype": "Select", "label": "Seating", "options": "Any\nIndoor\nOutdoor\nPrivate Room"},
    {"fieldname": "special_requests", "fieldtype": "Small Text", "label": "Special Requests"},
    sb("Internal"),
    {"fieldname": "assigned_table", "fieldtype": "Link", "label": "Assigned Table", "options": "Restaurant Table"},
    {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Pending\nConfirmed\nSeated\nCompleted\nCancelled\nNo-Show", "default": "Pending", "in_list_view": 1, "in_standard_filter": 1},
    cb(),
    {"fieldname": "confirmation_sent", "fieldtype": "Check", "label": "Confirmation Sent"},
    {"fieldname": "confirmation_method", "fieldtype": "Select", "label": "Confirmation Method", "options": "\nWhatsApp\nSMS\nEmail"},
    sb("Notes"),
    {"fieldname": "internal_notes", "fieldtype": "Small Text", "label": "Internal Notes"},
    {"fieldname": "source", "fieldtype": "Select", "label": "Source", "options": "Website\nPhone\nWalk-in\nWhatsApp", "default": "Website"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="naming_series:",
    naming_rule="By \"Naming Series\" field",
    permissions=[
        {"create": 1, "delete": 1, "read": 1, "write": 1, "role": "System Manager"},
        {"create": 1, "delete": 1, "read": 1, "write": 1, "role": "Candela Manager"},
        {"create": 1, "read": 1, "write": 1, "role": "Candela Staff"},
    ],
)

# ═══════════════════════════════════════════════════
# ONLINE ORDER
# ═══════════════════════════════════════════════════

print("Creating Online Order...")

write_doctype("Online Order", [
    {"fieldname": "naming_series", "fieldtype": "Select", "label": "Series", "options": "CORD-.YYYY.-.#####", "default": "CORD-.YYYY.-.#####", "hidden": 1},
    {"fieldname": "customer_name", "fieldtype": "Data", "label": "Customer Name", "reqd": 1, "in_list_view": 1},
    {"fieldname": "phone", "fieldtype": "Data", "label": "Phone", "reqd": 1},
    {"fieldname": "email", "fieldtype": "Data", "label": "Email", "options": "Email"},
    sb("Order Type"),
    {"fieldname": "order_type", "fieldtype": "Select", "label": "Order Type", "options": "Delivery\nPickup", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
    sb("Delivery Details"),
    {"fieldname": "delivery_address", "fieldtype": "Small Text", "label": "Delivery Address", "depends_on": "eval:doc.order_type=='Delivery'", "mandatory_depends_on": "eval:doc.order_type=='Delivery'"},
    {"fieldname": "delivery_zone", "fieldtype": "Link", "label": "Delivery Zone", "options": "Delivery Zone", "depends_on": "eval:doc.order_type=='Delivery'"},
    {"fieldname": "delivery_fee", "fieldtype": "Currency", "label": "Delivery Fee"},
    {"fieldname": "delivery_notes", "fieldtype": "Small Text", "label": "Delivery Notes"},
    sb("Items"),
    {"fieldname": "items", "fieldtype": "Table", "label": "Order Items", "options": "Order Item", "reqd": 1},
    sb("Pricing"),
    {"fieldname": "subtotal", "fieldtype": "Currency", "label": "Subtotal", "read_only": 1, "in_list_view": 1},
    {"fieldname": "discount_amount", "fieldtype": "Currency", "label": "Discount"},
    {"fieldname": "promo_code", "fieldtype": "Link", "label": "Promo Code", "options": "Promo Code"},
    cb(),
    {"fieldname": "total", "fieldtype": "Currency", "label": "Total", "read_only": 1, "in_list_view": 1},
    sb("Payment"),
    {"fieldname": "payment_method", "fieldtype": "Select", "label": "Payment Method", "options": "Cash on Delivery\nPaymob\nFawry", "default": "Cash on Delivery"},
    {"fieldname": "payment_status", "fieldtype": "Select", "label": "Payment Status", "options": "Pending\nPaid\nFailed\nRefunded", "default": "Pending"},
    {"fieldname": "payment_reference", "fieldtype": "Data", "label": "Payment Reference"},
    sb("Status"),
    {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Pending\nConfirmed\nPreparing\nReady\nOut for Delivery\nDelivered\nCancelled", "default": "Pending", "in_list_view": 1, "in_standard_filter": 1},
    {"fieldname": "estimated_time", "fieldtype": "Int", "label": "Estimated Time (min)"},
    {"fieldname": "actual_delivery_time", "fieldtype": "Datetime", "label": "Actual Delivery Time"},
    sb("Tracking"),
    {"fieldname": "tracking_token", "fieldtype": "Data", "label": "Tracking Token", "unique": 1, "read_only": 1},
    {"fieldname": "internal_notes", "fieldtype": "Small Text", "label": "Internal Notes"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="naming_series:",
    naming_rule="By \"Naming Series\" field",
    py_content='''# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
import uuid
from frappe.model.document import Document


class OnlineOrder(Document):
\tdef before_insert(self):
\t\tif not self.tracking_token:
\t\t\tself.tracking_token = str(uuid.uuid4())[:8].upper()

\tdef validate(self):
\t\tself.calculate_totals()

\tdef calculate_totals(self):
\t\tself.subtotal = 0
\t\tfor item in self.items:
\t\t\titem.amount = (item.unit_price or 0) * (item.quantity or 0)
\t\t\tself.subtotal += item.amount
\t\tself.total = self.subtotal - (self.discount_amount or 0) + (self.delivery_fee or 0)
''',
    js_content="""// Copyright (c) 2026, Arkan Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Online Order', {
    refresh(frm) {
        if (frm.doc.tracking_token) {
            frm.add_custom_button(__('Track Order'), function() {
                window.open('/dela/order-tracking?token=' + frm.doc.tracking_token, '_blank');
            });
        }
    }
});
""")

# ═══════════════════════════════════════════════════
# RESTAURANT EVENT
# ═══════════════════════════════════════════════════

print("Creating Restaurant Event...")

write_doctype("Restaurant Event", [
    {"fieldname": "event_name_ar", "fieldtype": "Data", "label": "Event Name (Arabic)", "reqd": 1, "in_list_view": 1},
    {"fieldname": "event_name_en", "fieldtype": "Data", "label": "Event Name (English)", "reqd": 1, "in_list_view": 1},
    {"fieldname": "slug", "fieldtype": "Data", "label": "Slug"},
    {"fieldname": "event_date", "fieldtype": "Date", "label": "Date", "reqd": 1, "in_list_view": 1, "in_standard_filter": 1},
    {"fieldname": "event_time", "fieldtype": "Time", "label": "Start Time"},
    {"fieldname": "end_time", "fieldtype": "Time", "label": "End Time"},
    sb("Details"),
    {"fieldname": "description_ar", "fieldtype": "Text Editor", "label": "Description (Arabic)"},
    {"fieldname": "description_en", "fieldtype": "Text Editor", "label": "Description (English)"},
    {"fieldname": "image", "fieldtype": "Attach Image", "label": "Image"},
    sb("Capacity & Pricing"),
    {"fieldname": "price", "fieldtype": "Currency", "label": "Price"},
    {"fieldname": "max_capacity", "fieldtype": "Int", "label": "Max Capacity"},
    {"fieldname": "current_bookings", "fieldtype": "Int", "label": "Current Bookings", "read_only": 1, "default": "0"},
    sb("Settings"),
    {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1", "in_list_view": 1},
    {"fieldname": "is_featured", "fieldtype": "Check", "label": "Featured"},
    {"fieldname": "booking_link", "fieldtype": "Data", "label": "Booking Link"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="field:event_name_en",
    naming_rule="By fieldname",
    py_content='''# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RestaurantEvent(Document):
\tdef before_save(self):
\t\tif not self.slug and self.event_name_en:
\t\t\tself.slug = self.event_name_en.lower().replace(" ", "-").replace("&", "and")
''')

# ═══════════════════════════════════════════════════
# CUSTOMER REVIEW
# ═══════════════════════════════════════════════════

print("Creating Customer Review...")

write_doctype("Customer Review", [
    {"fieldname": "customer_name", "fieldtype": "Data", "label": "Customer Name", "reqd": 1, "in_list_view": 1},
    {"fieldname": "rating", "fieldtype": "Rating", "label": "Rating", "in_list_view": 1},
    {"fieldname": "review_text_ar", "fieldtype": "Small Text", "label": "Review (Arabic)"},
    {"fieldname": "review_text_en", "fieldtype": "Small Text", "label": "Review (English)"},
    {"fieldname": "visit_date", "fieldtype": "Date", "label": "Visit Date"},
    sb("Moderation"),
    {"fieldname": "is_approved", "fieldtype": "Check", "label": "Approved", "default": "0", "in_list_view": 1, "in_standard_filter": 1},
    {"fieldname": "is_featured", "fieldtype": "Check", "label": "Featured"},
    {"fieldname": "source", "fieldtype": "Select", "label": "Source", "options": "Website\nGoogle\nInstagram\nTripAdvisor", "default": "Website"},
    {"fieldname": "customer_photo", "fieldtype": "Attach Image", "label": "Customer Photo"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="autoincrement",
    naming_rule="Autoincrement",
)

# ═══════════════════════════════════════════════════
# GALLERY IMAGE
# ═══════════════════════════════════════════════════

print("Creating Gallery Image...")

write_doctype("Gallery Image", [
    {"fieldname": "image", "fieldtype": "Attach Image", "label": "Image", "reqd": 1},
    {"fieldname": "title_ar", "fieldtype": "Data", "label": "Title (Arabic)", "in_list_view": 1},
    {"fieldname": "title_en", "fieldtype": "Data", "label": "Title (English)", "in_list_view": 1},
    {"fieldname": "category", "fieldtype": "Select", "label": "Category", "options": "Food\nInterior\nEvents\nKitchen\nExterior", "in_list_view": 1, "in_standard_filter": 1},
    {"fieldname": "sort_order", "fieldtype": "Int", "label": "Sort Order"},
    {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="autoincrement",
    naming_rule="Autoincrement",
    sort_field="sort_order",
)

# ═══════════════════════════════════════════════════
# DELIVERY ZONE
# ═══════════════════════════════════════════════════

print("Creating Delivery Zone...")

write_doctype("Delivery Zone", [
    {"fieldname": "zone_name", "fieldtype": "Data", "label": "Zone Name", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "delivery_fee", "fieldtype": "Currency", "label": "Delivery Fee", "reqd": 1, "in_list_view": 1},
    {"fieldname": "estimated_minutes", "fieldtype": "Int", "label": "Estimated Minutes", "in_list_view": 1},
    {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1", "in_list_view": 1},
    {"fieldname": "notes", "fieldtype": "Small Text", "label": "Notes"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="field:zone_name",
    naming_rule="By fieldname",
)

# ═══════════════════════════════════════════════════
# PROMO CODE
# ═══════════════════════════════════════════════════

print("Creating Promo Code...")

write_doctype("Promo Code", [
    {"fieldname": "code", "fieldtype": "Data", "label": "Code", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "discount_type", "fieldtype": "Select", "label": "Discount Type", "options": "Percentage\nFixed Amount", "reqd": 1, "in_list_view": 1},
    {"fieldname": "discount_value", "fieldtype": "Float", "label": "Discount Value", "reqd": 1, "in_list_view": 1},
    {"fieldname": "minimum_order", "fieldtype": "Currency", "label": "Minimum Order"},
    {"fieldname": "max_uses", "fieldtype": "Int", "label": "Max Uses", "description": "0 = unlimited"},
    {"fieldname": "times_used", "fieldtype": "Int", "label": "Times Used", "read_only": 1, "default": "0"},
    {"fieldname": "valid_from", "fieldtype": "Date", "label": "Valid From"},
    {"fieldname": "valid_until", "fieldtype": "Date", "label": "Valid Until"},
    {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1", "in_list_view": 1},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="field:code",
    naming_rule="By fieldname",
)

# ═══════════════════════════════════════════════════
# NEWSLETTER SUBSCRIBER
# ═══════════════════════════════════════════════════

print("Creating Newsletter Subscriber...")

write_doctype("Newsletter Subscriber", [
    {"fieldname": "email", "fieldtype": "Data", "label": "Email", "reqd": 1, "unique": 1, "options": "Email", "in_list_view": 1},
    {"fieldname": "name_field", "fieldtype": "Data", "label": "Name"},
    {"fieldname": "subscribed_on", "fieldtype": "Date", "label": "Subscribed On", "default": "Today"},
    {"fieldname": "is_active", "fieldtype": "Check", "label": "Active", "default": "1", "in_list_view": 1},
    {"fieldname": "source", "fieldtype": "Select", "label": "Source", "options": "Website\nEvent\nManual", "default": "Website"},
    {"fieldname": "is_demo_data", "fieldtype": "Check", "label": "Demo Data", "hidden": 1, "default": "0"},
],
    autoname="field:email",
    naming_rule="By fieldname",
)

print("\n✅ All DocTypes created successfully!")
