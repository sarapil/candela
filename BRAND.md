# 🕯️ Candela Brand Guide

> *"Light up your restaurant operations"* — Creative & inspiring

## Brand Essence

Candela (Italian: "candle") represents the warm, inviting glow of Italian hospitality combined with the precision of modern restaurant operations. Our visual identity balances **luxury warmth** (amber/gold tones) with **operational clarity** (clean UI, data-driven dashboards).

---

## 🎨 Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--cd-primary` | `#F59E0B` | Amber — primary actions, CTAs, active states |
| `--cd-primary-dark` | `#D97706` | Hover states, emphasis |
| `--cd-primary-light` | `#FEF3C7` | Backgrounds, highlights, badges |
| `--cd-dark` | `#1C1917` | Stone 900 — text, headers, dark mode bg |
| `--cd-dark-secondary` | `#292524` | Stone 800 — cards, panels |
| `--cd-text` | `#44403C` | Stone 700 — body text |
| `--cd-text-light` | `#78716C` | Stone 500 — secondary text, captions |
| `--cd-surface` | `#FAFAF9` | Stone 50 — page backgrounds |
| `--cd-border` | `#E7E5E4` | Stone 200 — borders, dividers |
| `--cd-success` | `#16A34A` | Green — available tables, confirmed |
| `--cd-danger` | `#DC2626` | Red — reserved, errors, alerts |
| `--cd-warning` | `#F59E0B` | Amber — occupied, pending |

---

## 🔤 Typography

| Use | Font | Weight |
|-----|------|--------|
| Headings | Inter / system-ui | 700 (Bold) |
| Body | Inter / system-ui | 400 (Regular) |
| Numbers / Data | Tabular Nums | 500 (Medium) |
| Arabic | System Arabic (Segoe UI, Tahoma) | 400–700 |
| Italian accents | Ensure proper rendering of à, è, é, ì, ò, ù | — |

---

## 🖼️ Logo System

| Variant | File | Usage |
|---------|------|-------|
| Animated (Primary) | `candela-logo.svg` | App screen, splash, about page (512×512) |
| Topbar | `candela-topbar.svg` | Desk navbar icon (28×28) |
| Favicon | `favicon.svg` | Browser tab icon |
| Dark (on light bg) | `logo-dark.svg` | Light backgrounds |
| White (on dark bg) | `logo-white.svg` | Dark backgrounds, footers |
| Gold (accent) | `logo-gold.svg` | Premium contexts, certificates |
| Flame only | `flame.svg` | Compact icon, mobile |
| Splash | `candela-splash.svg` | Loading screen |
| Login | `candela-login.svg` | Login page animated logo |

### Logo Rules
- ✅ Minimum clear space: 1× flame width on all sides
- ✅ Minimum size: 24px (flame icon), 120px (full logo)
- ❌ Never stretch, rotate, or recolor the logo
- ❌ Never place on busy backgrounds without overlay

---

## 🖥️ Desktop Icons

**14 icons** (7 solid + 7 subtle) covering all workspace categories:
- Solid variants: Full amber fill with white icon
- Subtle variants: Amber outline on transparent background
- Size: 54×54px SVG with 4px corner radius

---

## 🎯 Competitive Positioning

### Tagline Options
| Context | Tagline |
|---------|---------|
| Technical | "Full-stack restaurant management on Frappe v16" |
| Business | "Light up your restaurant operations" |
| Arabic | "أضئ عمليات مطعمك" |
| Feature | "From menu to POS to kitchen to accounting — one platform" |

### Differentiators (vs Toast, Square, Foodics, Odoo)
1. **Open-source & self-hosted** — No vendor lock-in, no transaction fees
2. **ERPNext backbone** — Real accounting, not just POS reports
3. **Recipe-level food costing** — Track cost per dish, not just revenue
4. **Arabic-first** — Full RTL, 1242 translated strings, MENA market ready
5. **CAPS permissions** — Field-level cost masking, 21 granular capabilities
6. **Visual onboarding** — frappe_visual storyboards, not PDF manuals
7. **Kitchen intelligence** — Station-based KDS with production logging

---

## 👥 Persona Visual Language

| Persona | Icon | Color Accent | Dashboard Focus |
|---------|------|-------------|----------------|
| Manager | 📊 chart-bar | Amber `#F59E0B` | Revenue, food cost %, P&L |
| Chef | 👨‍🍳 chef-hat | Red `#DC2626` | Kitchen queue, production |
| Cashier | 💰 cash | Green `#16A34A` | POS, daily closing |
| Waiter | 🍽️ layout-grid | Blue `#3B82F6` | Tables, reservations |
| Procurement | 📦 package | Purple `#8B5CF6` | Suppliers, stock levels |
| Marketing | 📢 speakerphone | Pink `#EC4899` | Campaigns, reviews |

---

## 📏 Spacing & Layout

| Token | Value |
|-------|-------|
| Border Radius (cards) | `12px` |
| Border Radius (buttons) | `8px` |
| Border Radius (inputs) | `6px` |
| Card Shadow | `0 1px 3px rgba(0,0,0,0.1)` |
| Card Hover Shadow | `0 4px 12px rgba(245,158,11,0.15)` |
| Page Max Width | `1280px` |
| Section Padding | `2rem` |
| Grid Gap | `1.5rem` |

---

## 🌙 Dark Mode

| Token | Light | Dark |
|-------|-------|------|
| Background | `#FAFAF9` | `#1C1917` |
| Surface | `#FFFFFF` | `#292524` |
| Text | `#44403C` | `#E7E5E4` |
| Border | `#E7E5E4` | `#44403C` |
| Primary | `#F59E0B` | `#FBBF24` |

---

## ↔️ RTL Support

- All layouts use `logical` CSS properties (`margin-inline-start`, `padding-inline-end`)
- Sidebar flips automatically
- Charts and graphs remain LTR (numbers)
- Table column order preserved
- Icon direction flipped where semantically appropriate (arrows, navigation)

---

## 🔗 Domain Context

**Industry:** Restaurant Technology (RestaurantTech)
**Sub-domains:** Fine Dining, Café & Coffee Shop, Catering, Cloud Kitchen, Hotel Restaurant, Bakery, Event & Banquet
**Target Market:** MENA (Egypt, UAE, Saudi Arabia) expanding to Mediterranean markets
**Currency Support:** EGP (primary), AED, SAR, USD, EUR
**Tax Compliance:** UAE VAT with Emirate-level reporting

---

## 📋 Sales Tone Guidelines

| Audience | Tone | Example |
|----------|------|---------|
| Restaurant Owner | Inspiring, ROI-focused | "See your true food cost in real-time, not at month-end" |
| Chef | Professional, practical | "Your recipes drive automatic inventory — no more guessing" |
| IT Decision Maker | Technical, trustworthy | "Self-hosted on Frappe v16, ERPNext accounting, CAPS permissions" |
| Investor / Buyer | Visionary, data-rich | "55 DocTypes covering 100% of restaurant operations" |
