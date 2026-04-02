import frappe
from frappe.utils import flt
from candela.utils import get_candela_settings, get_lang, is_rtl


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw("Please login to access Marketing", frappe.PermissionError)

	lang = get_lang()
	context.candela = get_candela_settings()
	context.page_type = "admin"
	context.title = "التسويق" if lang == "ar" else "Marketing"
	context.candela_lang = lang
	context.candela_dir = "rtl" if is_rtl() else "ltr"
	context.no_breadcrumbs = True

	# Marketing Campaigns
	context.campaigns = frappe.get_all(
		"Marketing Campaign",
		fields=["name", "campaign_name", "campaign_type", "phase",
		        "start_date", "end_date", "budget", "spent",
		        "total_reach", "roi_percentage"],
		order_by="creation desc",
		limit=15,
	)

	# Influencers
	context.influencers = frappe.get_all(
		"Influencer",
		fields=["name", "influencer_name", "platform", "followers_count",
		        "category", "total_reach", "roi_score", "rating"],
		order_by="followers_count desc",
		limit=15,
	)

	# Online Reviews
	context.reviews = frappe.get_all(
		"Online Review",
		fields=["name", "platform", "reviewer_name", "rating", "review_date",
		        "sentiment", "response_posted", "review_text"],
		order_by="review_date desc",
		limit=20,
	)

	# Competitors
	context.competitors = frappe.get_all(
		"Competitor",
		fields=["name", "competitor_name", "cuisine", "location",
		        "price_range", "google_rating", "competitor_type"],
		order_by="google_rating desc",
		limit=10,
	)

	# Customer Personas
	context.personas = frappe.get_all(
		"Customer Persona",
		fields=["name", "persona_name_ar", "persona_name_en", "persona_code",
		        "age_range", "income_level", "visit_pattern", "preferred_channels"],
		order_by="persona_name_en asc",
	)

	# Corporate Accounts
	context.corporate_accounts = frappe.get_all(
		"Corporate Account",
		fields=["name", "company_name", "contact_person", "status",
		        "credit_limit", "total_orders"],
		order_by="creation desc",
		limit=10,
	)

	# Stats
	avg_rating = flt(frappe.db.sql("""
		SELECT COALESCE(AVG(rating), 0) FROM `tabOnline Review`
		WHERE rating > 0
	""")[0][0])

	total_marketing_spend = flt(frappe.db.sql("""
		SELECT COALESCE(SUM(spent), 0) FROM `tabMarketing Campaign`
		WHERE phase IN ('Active', 'Completed')
	""")[0][0])

	context.stats = {
		"active_campaigns": frappe.db.count("Marketing Campaign", {"phase": "Active"}),
		"total_influencers": len(context.influencers),
		"avg_rating": avg_rating,
		"unresponded_reviews": frappe.db.count("Online Review", {"response_posted": 0}),
		"total_marketing_spend": total_marketing_spend,
		"corporate_accounts": len(context.corporate_accounts),
	}
