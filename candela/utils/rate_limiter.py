# Copyright (c) 2026, Arkan Labs and contributors
# For license information, please see license.txt

"""
Redis-based rate limiter for guest-accessible APIs.

Usage:
    from candela.utils.rate_limiter import check_rate_limit

    @frappe.whitelist(allow_guest=True)
    def submit_reservation(...):
        check_rate_limit("reservation", limit=5, window=60)   # 5 per minute
        ...
"""

import frappe
from frappe import _


def check_rate_limit(action: str, limit: int = 10, window: int = 60):
    """Enforce a per-IP rate limit using Redis.

    Args:
        action:  A short key name (e.g. "reservation", "order", "review").
        limit:   Maximum number of calls allowed within *window* seconds.
        window:  Sliding window size in seconds (default 60).

    Raises:
        frappe.TooManyRequestsError when the limit is exceeded.
    """
    ip = frappe.local.request_ip if hasattr(frappe.local, "request_ip") else "unknown"
    cache_key = f"candela_rl:{action}:{ip}"

    try:
        current = frappe.cache.get_value(cache_key) or 0
        current = int(current)

        if current >= limit:
            frappe.local.response["http_status_code"] = 429
            frappe.throw(
                _("Too many requests. Please wait a moment and try again."),
                title=_("Rate Limit Exceeded"),
            )

        frappe.cache.set_value(cache_key, current + 1, expires_in_sec=window)
    except frappe.ValidationError:
        raise
    except Exception:
        # If Redis is down, allow the request through (fail-open)
        pass
