"""
Candela — Constants
Application-wide constants for Candela.
"""

# App metadata
APP_NAME = "candela"
APP_TITLE = "Candela"
APP_PREFIX = "CD"
APP_COLOR = "#F59E0B"

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Cache TTL (seconds)
CACHE_SHORT = 300       # 5 minutes
CACHE_MEDIUM = 3600     # 1 hour
CACHE_LONG = 86400      # 24 hours

# Status constants
STATUS_DRAFT = "Draft"
STATUS_ACTIVE = "Active"
STATUS_CANCELLED = "Cancelled"
STATUS_COMPLETED = "Completed"

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
