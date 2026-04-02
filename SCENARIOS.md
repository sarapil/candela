# 📋 Usage Scenarios — سيناريوهات الاستخدام
> **Candela Restaurant** · Prefix: CD · 55 DocTypes · 27 API Methods · 7 Roles

---

## 🗺️ Workflow Map — خريطة سير العمل

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  🌐 Website  │────▶│ 📋 Ordering  │────▶│ 🍳 Kitchen   │
│  (Guest)     │     │  & POS       │     │  Production  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
  Reservation          POS Invoice          Production Log
  Online Order         Order Items          Waste Tracking
  Newsletter           Promo Code           Quality Check
  Review               Payment              Ingredient Use
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ 🪑 Tables    │     │ 💰 Closing   │     │ 📦 Inventory │
│  Management  │     │  & Finance   │     │  & Procure   │
└──────────────┘     └──────────────┘     └──────────────┘
  Table Status         Daily Closing        Stock Entry
  Reservations         POS Shift            Purchase Req
  Floor Map            Expenses             GRN Receipt
                       Revenue              Stock Transfer
                                            Reconciliation
       │                    │                    │
       └────────────┬───────┘────────────────────┘
                    ▼
            ┌──────────────┐
            │ 📊 Reports   │
            │  & Marketing │
            └──────────────┘
              Food Cost
              Operations Dashboard
              Campaigns
              Events
              Reviews
```

---

## 🔄 Scenario Categories

### A. Guest-Facing Workflows (Public Website)

#### SC-001: Browse Menu & Order Online
| Field | Detail |
|-------|--------|
| Actor | Guest (unauthenticated) |
| Trigger | Visits `/dela/menu` |
| Steps | 1. Browse categories → 2. View item details → 3. Add to cart → 4. Enter delivery info → 5. Apply promo code → 6. Submit order |
| API Calls | `get_menu()`, `get_menu_item()`, `validate_promo_code()`, `get_delivery_zones()`, `submit_order()` |
| DocTypes | Menu Category, Menu Item, Online Order, Order Item, Delivery Zone, Promo Code |
| Success | Order created with tracking token, email/SMS confirmation |
| Error Cases | Invalid promo, out-of-delivery-zone, item unavailable |

#### SC-002: Make a Table Reservation
| Field | Detail |
|-------|--------|
| Actor | Guest |
| Trigger | Visits `/dela/reservation` |
| Steps | 1. Select date/time → 2. Choose guests count → 3. Enter contact info → 4. Submit |
| API Calls | `submit_reservation()` |
| DocTypes | Table Reservation, Restaurant Table |
| Success | Reservation confirmed, notification to manager |
| Governance | `notify_new_reservation` doc_event |

#### SC-003: Track Order Status
| Field | Detail |
|-------|--------|
| Actor | Guest with tracking token |
| API Calls | `get_order_status(tracking_token)` |

#### SC-004: Submit a Review
| Actor | Guest | API | `submit_review()` |

#### SC-005: Subscribe to Newsletter
| Actor | Guest | API | `subscribe_newsletter()` |

---

### B. POS & Front-of-House

#### SC-010: Open POS Shift
| Field | Detail |
|-------|--------|
| Actor | Candela Cashier |
| Steps | 1. Open shift with opening cash → 2. POS terminal ready |
| API | `open_pos_shift(opening_cash, shift_type)` |
| DocTypes | POS Shift |

#### SC-011: Create POS Invoice (Dine-in)
| Field | Detail |
|-------|--------|
| Actor | Candela Cashier / Waiter |
| Steps | 1. Select table → 2. Add items → 3. Apply discount → 4. Process payment → 5. Print receipt |
| API | `create_pos_invoice(order_type, items, ...)` |
| DocTypes | POS Invoice, POS Invoice Item, Restaurant Table |
| Governance | `deduct_ingredients_on_pos` auto-fires → Stock Entry |

#### SC-012: Manage Table Status
| Actor | Candela Waiter |
| API | `update_table_status(table, action)` |
| Actions | occupy, free, reserve, clean |

#### SC-013: Close POS Shift
| Actor | Candela Cashier |
| API | `close_pos_shift(shift_name, closing_cash)` |
| Validation | Cash variance check |

---

### C. Kitchen Operations

#### SC-020: Kitchen Display — View & Process Orders
| Field | Detail |
|-------|--------|
| Actor | Candela Chef |
| Steps | 1. View pending orders on KDS → 2. Mark in-progress → 3. Mark ready |
| API | `get_kitchen_orders()`, `update_kitchen_status(order_name, source, new_status)` |
| DocTypes | Online Order, POS Invoice |
| Display | Color-coded by priority and age |

#### SC-021: Log Production
| Actor | Candela Chef |
| API | `create_production_log()`, `complete_production_log()` |
| DocTypes | Production Log, Production Waste |
| Governance | Recipe-based ingredient deduction |

---

### D. Procurement & Inventory

#### SC-030: Create Purchase Request
| Actor | Candela Procurement |
| API | `create_purchase_request(items, urgency, supplier)` |

#### SC-031: Approve Purchase Request
| Actor | Candela Manager |
| API | `approve_purchase_request(name)` |

#### SC-032: Receive Goods (GRN)
| Actor | Candela Procurement |
| API | `receive_grn(name)` |
| Governance | Auto-creates Stock Entry on GRN approval |

#### SC-033: Stock Transfer Between Warehouses
| Actor | Candela Staff |
| API | `do_stock_transfer(from_warehouse, to_warehouse, items)` |

#### SC-034: Stock Reconciliation
| Actor | Candela Manager |
| API | `start_reconciliation(warehouse)` |

#### SC-035: Low Stock Alert
| Trigger | Scheduler (daily) |
| Task | `check_low_stock_alerts()` |
| Action | Notification to Procurement role |

---

### E. Daily Closing & Finance

#### SC-040: Generate Daily Closing
| Actor | Candela Manager / System (auto) |
| API | `generate_daily_closing(closing_date)` |
| DocTypes | Daily Closing, Daily Expense |
| Scheduler | `auto_populate_daily_closing` (daily) |

#### SC-041: View Operations Dashboard
| Actor | Candela Manager |
| API | `get_operations_dashboard()` |

#### SC-042: Food Cost Report
| Actor | Candela Manager |
| API | `get_food_cost_report(from_date, to_date)` |

---

### F. Marketing & CRM

#### SC-050: Create Marketing Campaign
| Actor | Candela Marketing |
| DocTypes | Marketing Campaign, Campaign Activity, Content Calendar Entry |

#### SC-051: Manage Restaurant Events
| DocTypes | Restaurant Event |
| Governance | `notify_new_event` |

#### SC-052: Influencer Visit Tracking
| DocTypes | Influencer, Influencer Visit |

#### SC-053: Corporate Lunch Packages
| DocTypes | Corporate Account, Corporate Lunch Package |

---

### G. Governance & Automated Rules

| ID | Rule | Trigger | Action |
|----|------|---------|--------|
| GOV-001 | Ingredient deduction on order confirm | `Online Order.on_update` | `deduct_ingredients_on_confirm()` |
| GOV-002 | Ingredient deduction on POS | `POS Invoice.after_insert` | `deduct_ingredients_on_pos()` |
| GOV-003 | Price change logging | `Menu Item.on_update` | `log_price_change()` → Price Change Log |
| GOV-004 | Recipe enforcement | `Stock Entry.before_insert` | `enforce_recipe_on_dispensing()` |
| GOV-005 | GRN auto-stock | `Goods Receipt Note.on_update` | `stock_grn_items()` |
| GOV-006 | Stock reconciliation | `Stock Reconciliation.on_update` | `reconcile_stock()` |
| GOV-007 | Expired promo cleanup | Scheduler (daily) | `deactivate_expired_promos()` |
| GOV-008 | No-show detection | Scheduler (hourly) | `mark_no_show_reservations()` |
| GOV-009 | Preventive maintenance | Scheduler (daily) | `check_preventive_maintenance()` |

---

### H. Scheduler Tasks

| Schedule | Task | Description |
|----------|------|-------------|
| Daily | `mark_past_reservations_completed` | Auto-complete past reservations |
| Daily | `deactivate_expired_promos` | Disable expired promo codes |
| Daily | `check_low_stock_alerts` | Alert on low inventory |
| Daily | `check_preventive_maintenance` | Alert on upcoming maintenance |
| Daily | `auto_populate_daily_closing` | Generate daily closing report |
| Hourly | `mark_no_show_reservations` | Flag no-show guests |

---

## 🎯 Impact Matrix — مصفوفة التأثير

| File Changed | Affected Scenarios |
|-------------|--------------------|
| `api.py` | SC-001 to SC-005, SC-010 to SC-013, SC-020 to SC-021 |
| `operations_api.py` | SC-030 to SC-035, SC-040 to SC-042 |
| `governance.py` | GOV-001 to GOV-006 |
| `notifications.py` | SC-002, SC-004, SC-051 |
| `tasks.py` | GOV-007 to GOV-009, all scheduler tasks |
| Menu Item DocType | SC-001, SC-011, GOV-003 |
| Online Order DocType | SC-001, SC-003, SC-020, GOV-001 |
| POS Invoice DocType | SC-011, SC-013, SC-020, GOV-002 |
| Stock Entry DocType | SC-033, GOV-001, GOV-002, GOV-004 |
| Table Reservation DocType | SC-002, GOV-008 |

---

*Generated: 2026-03-29 · Candela v1.0 · Arkan Labs*
