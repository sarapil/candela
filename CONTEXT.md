# Candela — Technical Context

## Overview

**Italian Café & Restaurant Website + Operations Backend.** Candela is a full-stack restaurant management app combining a beautiful public-facing website (`/dela/*`) with a comprehensive operations admin dashboard (`/deladmin/*`). It covers the complete restaurant lifecycle: menu management, online ordering, table reservations, POS, kitchen display, procurement, inventory, production, staff shifts, daily closing, asset management, and marketing campaigns.

- **Publisher:** Arkan Labs
- **Version:** (latest)
- **License:** MIT
- **Color:** `#F59E0B` (amber)
- **Dependencies:** `frappe`, `caps`

## Architecture

- **Framework:** Frappe v16
- **Modules:** Candela (single module)
- **DocTypes:** 54 (including child tables)
- **API Files:** 2 (`api.py` for guest APIs, `operations_api.py` for authenticated APIs)
- **Pages:** None (uses `www/` route-based pages instead)
- **Reports:** 3
- **Website Routes:** 29 (10 public + 15 admin + 4 info/onboarding)
- **Scheduled Tasks:** 7 (daily + hourly)

### Dual-Surface Architecture

```
/dela/*          → Public customer-facing website (no login required)
/deladmin/*      → Operations admin dashboard (login required)
/candela-about   → App showcase
/candela-onboarding → Guided onboarding
```

## Key Components

### Guest API (`api.py`)

Public endpoints accessible without login:

| Endpoint | Purpose |
|----------|---------|
| `get_menu` | Fetch full menu with categories |
| `get_menu_item` | Individual menu item details |
| `submit_reservation` | Create table reservation |
| `subscribe_newsletter` | Newsletter signup |
| `submit_review` | Customer review submission |
| `get_order_status` | Track online order status |
| `get_delivery_zones` | Available delivery zones |
| `validate_promo_code` | Promo code validation |
| `submit_order` | Place online order |

### Operations API (`operations_api.py`)

Authenticated endpoints for staff/management:

| Endpoint | Purpose |
|----------|---------|
| `create_pos_invoice` | Create POS transaction |
| `get_kitchen_orders` / `update_kitchen_status` | Kitchen display system |
| `update_table_status` | Table management |
| `create_purchase_request` / `approve_purchase_request` | Procurement workflow |
| `receive_grn` | Goods receipt processing |
| `get_stock_levels` / `do_stock_transfer` | Inventory management |
| `start_reconciliation` | Stock reconciliation |
| `open_pos_shift` / `close_pos_shift` | POS shift management |
| `create_production_log` / `complete_production_log` | Kitchen production tracking |
| `generate_daily_closing` | End-of-day financial summary |
| `get_operations_dashboard` | Operations overview |
| `get_food_cost_report` | Food cost analysis |

### Governance Layer (`governance.py`)

Business rules and automated compliance:

| Function | Purpose |
|----------|---------|
| `deduct_ingredients_on_confirm` | Auto-deduct stock on order confirmation |
| `deduct_ingredients_on_pos` | Auto-deduct stock on POS sale |
| `log_price_change` | Audit trail for menu price changes |
| `enforce_recipe_on_dispensing` | Enforce recipe quantities on stock entries |
| `stock_grn_items` | Auto-create stock entries from GRN |
| `reconcile_stock` | Process stock reconciliation adjustments |

### Jinja Template Helpers (`utils.py`)

| Function | Purpose |
|----------|---------|
| `get_candela_settings` | Global settings for templates |
| `get_menu_categories` | Menu categories for navigation |
| `get_featured_items` | Featured menu items for homepage |
| `get_opening_hours_display` | Formatted opening hours |
| `get_approved_reviews` | Approved customer reviews |
| `get_active_events` | Active restaurant events |
| `get_gallery_images` | Gallery images |
| `candela_url` | URL helper |

### Frontend

**Desk (Admin) Assets:**
| File | Purpose |
|------|---------|
| `candela_workspace.js` | Workspace initialization |
| `candela_onboarding.js` | Onboarding storyboard |
| `candela_users.js` | User management |
| `candela_about.js` | About page |
| `candela_desk.css` | Admin styling |
| `candela-variables.css` | CSS custom properties |

**Website (Public) Assets:**
| File | Purpose |
|------|---------|
| `candela_website.js` | Website interactivity |
| `candela_theme.css` | Theme styling |
| `candela_animations.css` | CSS/GSAP animations |
| `candela_responsive.css` | Responsive breakpoints |
| `candela_rtl.css` | RTL (Arabic) layout support |

## Website Pages

### Public Website (`/dela/*`)

| Route | Page | Purpose |
|-------|------|---------|
| `/dela` | `index.html` | Homepage with hero, featured items, reviews |
| `/dela/menu` | `menu.html` | Full menu with categories and filters |
| `/dela/about` | `about.html` | Restaurant story and team |
| `/dela/gallery` | `gallery.html` | Photo gallery |
| `/dela/reservation` | `reservation.html` | Online table reservation |
| `/dela/events` | `events.html` | Upcoming events |
| `/dela/order` | `order.html` | Online ordering |
| `/dela/order-tracking` | `order_tracking.html` | Order status tracking |
| `/dela/contact` | `contact.html` | Contact form and location |

### Admin Dashboard (`/deladmin/*`)

| Route | Page | Purpose |
|-------|------|---------|
| `/deladmin` | `index.html` | Operations overview dashboard |
| `/deladmin/pos` | `pos.html` | Point of Sale interface |
| `/deladmin/kitchen` | `kitchen.html` | Kitchen display system (KDS) |
| `/deladmin/tables` | `tables.html` | Table layout management |
| `/deladmin/inventory` | `inventory.html` | Stock levels and management |
| `/deladmin/procurement` | `procurement.html` | Purchase requests and orders |
| `/deladmin/warehouses` | `warehouses.html` | Warehouse management |
| `/deladmin/production` | `production.html` | Kitchen production logs |
| `/deladmin/shifts` | `shifts.html` | Staff shift management |
| `/deladmin/closing` | `closing.html` | Daily closing reports |
| `/deladmin/assets` | `assets.html` | Equipment and asset management |
| `/deladmin/marketing` | `marketing.html` | Campaigns and promotions |
| `/deladmin/staff` | `staff.html` | Staff management |
| `/deladmin/reports` | `reports.html` | Operational reports |
| `/deladmin/settings` | `settings.html` | Restaurant configuration |
| `/deladmin/users` | `users.html` | User/role management |
| `/deladmin/overview` | `overview.html` | High-level overview |

## DocType Summary

### Configuration

| DocType | Purpose |
|---------|---------|
| Candela Settings | Global restaurant configuration |
| Opening Hours | Business hours by day |
| Service Mode | Service modes (dine-in, takeaway, delivery) |
| Delivery Zone | Delivery area definitions with fees |
| Kitchen Station | Kitchen stations (grill, salad, pastry, etc.) |

### Menu & Recipes

| DocType | Purpose |
|---------|---------|
| Menu Category | Menu sections (appetizers, mains, desserts) |
| Menu Item | Individual menu items with pricing |
| Menu Item Dietary Tag | Child: dietary tags (vegan, gluten-free) |
| Ingredient | Ingredient master with stock tracking |
| Recipe Item | Child: ingredient in a recipe |

### Orders & POS

| DocType | Purpose |
|---------|---------|
| Online Order | Customer-placed online orders |
| Order Item | Child: items in an order |
| POS Invoice | Point-of-sale transactions |
| POS Invoice Item | Child: items in POS invoice |
| POS Shift | POS shift open/close with cash reconciliation |
| Restaurant Table | Physical table management |
| Table Reservation | Customer reservations |

### Procurement & Inventory

| DocType | Purpose |
|---------|---------|
| Candela Supplier | Supplier profiles |
| Candela Warehouse | Warehouse/storage locations |
| Purchase Request | Internal purchase requisitions |
| Purchase Request Item | Child: items in request |
| Purchase Order | Orders to suppliers |
| Purchase Order Item | Child: items in order |
| Goods Receipt Note | Receiving goods from suppliers |
| GRN Item | Child: items in GRN |
| Stock Entry | Stock movements (in/out/transfer) |
| Stock Transfer | Inter-warehouse transfers |
| Stock Transfer Item | Child: items in transfer |
| Stock Reconciliation | Physical stock count adjustments |
| Reconciliation Item | Child: items in reconciliation |

### Production & Operations

| DocType | Purpose |
|---------|---------|
| Production Log | Kitchen production batches |
| Production Waste | Food waste tracking |
| Daily Closing | End-of-day financial summary |
| Daily Expense | Daily expense entries |
| Staff Shift | Staff shift scheduling |
| Price Change Log | Audit trail for menu price changes |

### Marketing & Customers

| DocType | Purpose |
|---------|---------|
| Marketing Campaign | Marketing campaign management |
| Campaign Activity | Child: activities in campaign |
| Promo Code | Promotional discount codes |
| Customer Review | Customer review/feedback |
| Online Review | External platform reviews |
| Newsletter Subscriber | Email newsletter signups |
| Customer Persona | Customer profile archetypes |
| Corporate Account | B2B corporate accounts |
| Corporate Lunch Package | Corporate meal packages |
| Content Calendar Entry | Marketing content scheduling |
| Competitor | Competitor restaurant profiles |
| Influencer | Influencer contacts |
| Influencer Visit | Influencer visit tracking |

### Facilities

| DocType | Purpose |
|---------|---------|
| Cafe Amenity | Amenity features (WiFi, parking) |
| Restaurant Asset | Equipment and asset tracking |
| Maintenance Request | Equipment maintenance requests |
| Restaurant Event | Special event management |
| Gallery Image | Photo gallery management |

## Reports

| Report | Purpose |
|--------|---------|
| Daily Orders Summary | Daily order volume and revenue |
| Menu Item Popularity | Most/least ordered items |
| Reservation Analytics | Reservation patterns and trends |

## Scheduled Tasks

| Schedule | Tasks |
|----------|-------|
| Daily | Mark past reservations completed, deactivate expired promos, check low stock alerts, check preventive maintenance, auto-populate daily closing |
| Hourly | Mark no-show reservations |

## Integration Points

- **CAPS:** Declares capabilities with `CD_` prefix; fixture-based CAPS setup for roles (Candela Manager, Staff, Chef, Cashier, Waiter, Procurement, Marketing)
- **Frappe Core:** Heavy use of Jinja template methods for server-rendered public website; doc_events for order/reservation/POS automation
- **ERPNext (indirect):** Stock entry patterns, purchase order workflows, POS invoice patterns
- **Notifications:** Real-time notifications for new reservations, orders, reviews, POS orders
- **User Data Protection:** GDPR-compliant data redaction for reservations, orders, newsletter subscribers

## Roles

`Candela Manager`, `Candela Staff`, `Candela Chef`, `Candela Cashier`, `Candela Waiter`, `Candela Procurement`, `Candela Marketing`
