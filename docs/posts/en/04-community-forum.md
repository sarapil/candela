<!-- Post Type: Community Forum | Platform: discuss.frappe.io, GitHub Discussions -->
<!-- Target: Frappe developers and power users -->
<!-- Last Updated: 2026-04-04 -->

# [Announcement] Candela — Complete Restaurant Management for ERPNext | Open Source

Hi Frappe Community! 👋

We're excited to share **Candela**, a new open-source restaurant app for Frappe/ERPNext.

## What it does

✅ Digital Menu with QR Codes
✅ Kitchen Display System (KDS)
✅ Table Management & Floor Plan
✅ Order Management (Dine-in/Takeout/Delivery)
✅ Inventory & Recipe Management
✅ Staff Scheduling
✅ Customer Loyalty Program
✅ Multi-Branch Support
✅ Delivery Driver Tracking
✅ Real-time Sales Dashboard

## Why we built it

- Restaurant POS not connected to accounting
- Kitchen orders getting lost or delayed
- Menu changes require technical support
- No visibility into food cost vs selling price
- Staff scheduling done on paper

We couldn't find a good restaurant solution that integrates natively with ERPNext, so we built one.

## Tech Stack

- **Backend:** Python, Frappe Framework v16
- **Frontend:** JavaScript, Frappe UI, frappe_visual components
- **Database:** MariaDB (standard Frappe)
- **License:** MIT
- **Dependencies:** frappe_visual, caps, arkan_help

## Installation

```bash
bench get-app https://github.com/sarapil/candela
bench --site your-site install-app candela
bench --site your-site migrate
```

## Screenshots

[Screenshots will be added to the GitHub repository]

## Roadmap

We're actively developing and would love community feedback on:
1. What features would you like to see?
2. What integrations are most important?
3. Any bugs or issues you encounter?

## Links

- 🔗 **GitHub:** https://github.com/sarapil/candela
- 📖 **Docs:** https://arkan.it.com/candela/docs
- 🏪 **Marketplace:** Frappe Cloud Marketplace
- 📧 **Contact:** support@arkan.it.com

## About Arkan Lab

We're building a complete ecosystem of open-source business apps for Frappe/ERPNext, covering hospitality, construction, CRM, communications, coworking, and more. All apps are designed to work together seamlessly.

Check out our full portfolio: https://arkan.it.com

---

*Feedback and contributions welcome! Star ⭐ the repo if you find it useful.*
