// Copyright (c) 2026, Arkan Lab — https://arkan.it.com
// License: MIT

frappe.pages["candela-onboarding"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __("Candela Onboarding — إعداد كانديلا"),
        single_column: true,
    });

    page.main.addClass("candela-onboarding-page");
    new CandelaOnboarding(page);
};

class CandelaOnboarding {
    constructor(page) {
        this.page = page;
        this.current_step = 0;
        this.completed_steps = new Set();
        this.steps = this.get_steps();
        this.init();
    }

    async init() {
        try {
            await frappe.require("frappe_visual.bundle.js");
        } catch (e) {
            console.warn("frappe_visual not available, using fallback");
        }
        this.render();
    }

    get_steps() {
        return [
            {
                key: "welcome",
                title: __("Welcome to Candela"),
                title_ar: "مرحباً بك في كانديلا",
                icon: "flame",
                description: __("Complete restaurant management: orders, kitchen, tables, menus, POS, and delivery."),
            },
            {
                key: "restaurant_setup",
                title: __("Restaurant Setup"),
                title_ar: "إعداد المطعم",
                icon: "building-store",
                description: __("Configure your restaurant branches, tables, kitchen stations, and basic settings."),
            },
            {
                key: "menu_config",
                title: __("Menu Configuration"),
                title_ar: "إعداد قائمة الطعام",
                icon: "book-2",
                description: __("Create menu categories, items, recipes, and pricing."),
            },
            {
                key: "roles_team",
                title: __("Roles & Team"),
                title_ar: "الأدوار والفريق",
                icon: "users",
                description: __("Assign roles: Manager, Chef, Waiter, Cashier, Delivery."),
            },
            {
                key: "order_workflow",
                title: __("Order Workflow"),
                title_ar: "سير عمل الطلبات",
                icon: "arrows-sort",
                description: __("Understand the order lifecycle: New → Preparing → Served → Paid."),
            },
            {
                key: "pos_billing",
                title: __("POS & Billing"),
                title_ar: "نقطة البيع والفواتير",
                icon: "cash-register",
                description: __("Set up POS shifts, payment methods, and invoice workflows."),
            },
            {
                key: "reservations",
                title: __("Table Reservations"),
                title_ar: "حجز الطاولات",
                icon: "calendar-event",
                description: __("Manage table reservations, walk-ins, and seating capacity."),
            },
            {
                key: "advanced",
                title: __("Advanced Features"),
                title_ar: "الميزات المتقدمة",
                icon: "sparkles",
                description: __("Online ordering, delivery zones, marketing campaigns, and analytics."),
            },
            {
                key: "go_live",
                title: __("Go Live!"),
                title_ar: "!ابدأ العمل",
                icon: "rocket",
                description: __("Final checks and launch your restaurant operations."),
            },
        ];
    }

    render() {
        const $main = $(this.page.main);
        $main.empty();

        $main.html(`
            <div class="fv-onboarding-wrapper" style="max-width:1100px;margin:0 auto;padding:24px">
                <div class="fv-fx-page-enter" id="onboarding-header"></div>
                <div class="fv-fx-page-enter" id="onboarding-progress" style="margin:24px 0"></div>
                <div class="fv-fx-page-enter" id="onboarding-content" style="margin-top:20px"></div>
                <div id="onboarding-nav" style="margin-top:24px"></div>
            </div>
        `);

        this.render_header();
        this.render_progress();
        this.render_step_content();
        this.render_navigation();
    }

    render_header() {
        const stats_html = `
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;margin-top:20px">
                ${this.stat_card("🍽️", __("Menu Items"), "Menu Item")}
                ${this.stat_card("🪑", __("Tables"), "Restaurant Table")}
                ${this.stat_card("📋", __("Orders Today"), "Online Order")}
                ${this.stat_card("👨‍🍳", __("Kitchen Stations"), "Kitchen Station")}
            </div>
        `;

        $("#onboarding-header").html(`
            <div class="fv-fx-glass" style="padding:32px;border-radius:16px;text-align:center">
                <div style="font-size:3rem;margin-bottom:8px">🕯️</div>
                <h1 style="font-size:1.8rem;font-weight:700;margin:0">
                    ${__("Candela Restaurant Management")}
                </h1>
                <p style="color:var(--text-muted);font-size:1.05rem;margin:8px 0 0">
                    ${__("نظام إدارة المطاعم الشامل — Complete Restaurant Operations")}
                </p>
                ${stats_html}
            </div>
        `);

        this.load_stat_counts();
    }

    stat_card(emoji, label, doctype) {
        return `
            <div class="fv-fx-hover-lift" style="background:var(--card-bg);border-radius:12px;padding:16px;text-align:center;border:1px solid var(--border-color)">
                <div style="font-size:1.5rem">${emoji}</div>
                <div id="stat-${doctype.replace(/\s/g, '-')}" style="font-size:1.4rem;font-weight:700;color:var(--text-color)">—</div>
                <div style="font-size:0.8rem;color:var(--text-muted)">${label}</div>
            </div>
        `;
    }

    load_stat_counts() {
        const doctypes = ["Menu Item", "Restaurant Table", "Online Order", "Kitchen Station"];
        doctypes.forEach((dt) => {
            frappe.xcall("frappe.client.get_count", { doctype: dt }).then((count) => {
                $(`#stat-${dt.replace(/\s/g, '-')}`).text(count || 0);
            }).catch(() => {
                $(`#stat-${dt.replace(/\s/g, '-')}`).text("—");
            });
        });
    }

    render_progress() {
        const total = this.steps.length;
        const pct = Math.round(((this.completed_steps.size) / total) * 100);

        const dots = this.steps.map((s, i) => {
            const is_done = this.completed_steps.has(i);
            const is_active = i === this.current_step;
            const bg = is_done ? "#F59E0B" : is_active ? "#D97706" : "var(--border-color)";
            const scale = is_active ? "transform:scale(1.3)" : "";
            return `<div style="width:${is_active ? 14 : 10}px;height:${is_active ? 14 : 10}px;border-radius:50%;background:${bg};transition:all .3s;${scale};cursor:pointer" data-step="${i}" class="progress-dot"></div>`;
        }).join("");

        $("#onboarding-progress").html(`
            <div style="display:flex;align-items:center;gap:12px">
                <div style="flex:1;height:6px;border-radius:3px;background:var(--border-color);overflow:hidden">
                    <div style="width:${pct}%;height:100%;background:linear-gradient(90deg,#F59E0B,#D97706);border-radius:3px;transition:width .5s"></div>
                </div>
                <span style="font-size:0.85rem;font-weight:600;color:#F59E0B">${pct}%</span>
            </div>
            <div style="display:flex;justify-content:center;gap:8px;margin-top:12px">${dots}</div>
        `);

        $("#onboarding-progress").find(".progress-dot").on("click", (e) => {
            this.current_step = parseInt($(e.target).data("step"));
            this.render_progress();
            this.render_step_content();
            this.render_navigation();
        });
    }

    render_step_content() {
        const step = this.steps[this.current_step];
        const content_fn = this[`render_${step.key}`];
        const $el = $("#onboarding-content");

        $el.html(`
            <div class="fv-fx-glass" style="padding:32px;border-radius:16px">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
                    <div style="width:48px;height:48px;border-radius:12px;background:rgba(245,158,11,0.15);color:#F59E0B;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:700">
                        ${this.current_step + 1}
                    </div>
                    <div>
                        <h2 style="font-size:1.3rem;font-weight:700;margin:0">${step.title}</h2>
                        <p style="font-size:0.85rem;color:var(--text-muted);margin:0">${step.title_ar}</p>
                    </div>
                </div>
                <p style="color:var(--text-muted);font-size:1rem;margin-bottom:20px">${step.description}</p>
                <div id="step-body"></div>
            </div>
        `);

        if (content_fn) {
            content_fn.call(this, $("#step-body"));
        }
    }

    render_welcome($el) {
        $el.html(`
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px">
                ${this.feature_card("🍕", __("Menu Management"), __("Create categories, items, recipes with ingredients and costing"))}
                ${this.feature_card("📋", __("Order Processing"), __("Real-time kitchen display, order tracking, and status updates"))}
                ${this.feature_card("🪑", __("Table Management"), __("Visual floor plan, seating, and capacity management"))}
                ${this.feature_card("💰", __("POS & Billing"), __("Point of sale, split bills, discounts, and payment processing"))}
                ${this.feature_card("📅", __("Reservations"), __("Online and walk-in booking with automated confirmations"))}
                ${this.feature_card("🚚", __("Delivery & Online"), __("Delivery zones, online ordering, and third-party integration"))}
                ${this.feature_card("📊", __("Analytics"), __("Revenue reports, popular items, peak hours, and staff performance"))}
                ${this.feature_card("📣", __("Marketing"), __("Campaigns, promo codes, influencer tracking, and customer reviews"))}
            </div>
        `);
    }

    render_restaurant_setup($el) {
        const actions = [
            { label: __("Configure Settings"), route: "candela-settings", icon: "⚙️" },
            { label: __("Add Branch"), route: "restaurant-branch/new", icon: "🏪" },
            { label: __("Create Tables"), route: "restaurant-table", icon: "🪑" },
            { label: __("Setup Kitchen"), route: "kitchen-station/new", icon: "👨‍🍳" },
        ];

        $el.html(`
            <div style="margin-bottom:20px">
                <h4 style="font-weight:600">${__("Quick Setup Actions")}</h4>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px">
                    ${actions.map(a => `
                        <div class="fv-fx-hover-lift" style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:16px;cursor:pointer;text-align:center"
                             onclick="frappe.set_route('${a.route}')">
                            <div style="font-size:2rem;margin-bottom:8px">${a.icon}</div>
                            <div style="font-size:0.9rem;font-weight:600">${a.label}</div>
                        </div>
                    `).join("")}
                </div>
            </div>
            <div class="fv-fx-glass" style="padding:20px;border-radius:12px;background:rgba(245,158,11,0.05)">
                <h4 style="font-weight:600">${__("Setup Checklist — قائمة الإعداد")}</h4>
                ${this.checklist_item(__("Restaurant name & details configured"))}
                ${this.checklist_item(__("At least one branch created"))}
                ${this.checklist_item(__("Tables added with capacity"))}
                ${this.checklist_item(__("Kitchen stations defined"))}
                ${this.checklist_item(__("Opening hours set"))}
            </div>
        `);
    }

    render_menu_config($el) {
        const actions = [
            { label: __("Add Category"), route: "menu-category/new", icon: "📂" },
            { label: __("Add Menu Item"), route: "menu-item/new", icon: "🍕" },
            { label: __("Add Recipe"), route: "recipe-item/new", icon: "📝" },
            { label: __("Add Ingredient"), route: "ingredient/new", icon: "🥬" },
        ];

        $el.html(`
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:20px">
                ${actions.map(a => `
                    <div class="fv-fx-hover-lift" style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:16px;cursor:pointer;text-align:center"
                         onclick="frappe.set_route('${a.route}')">
                        <div style="font-size:2rem;margin-bottom:8px">${a.icon}</div>
                        <div style="font-size:0.9rem;font-weight:600">${a.label}</div>
                    </div>
                `).join("")}
            </div>
            <div style="background:var(--card-bg);border-radius:12px;padding:20px;border:1px solid var(--border-color)">
                <h4 style="font-weight:600">${__("Menu Hierarchy — هيكل القائمة")}</h4>
                <div style="font-family:monospace;font-size:0.85rem;line-height:2;color:var(--text-muted)">
                    📂 ${__("Menu Category")} (${__("e.g. Appetizers, Main Course, Drinks")})<br>
                    &nbsp;&nbsp;└── 🍕 ${__("Menu Item")} (${__("name, price, image, availability")})<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 📝 ${__("Recipe Item")} (${__("preparation steps, time, difficulty")})<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── 🥬 ${__("Ingredient")} (${__("quantity, unit, cost, allergens")})
                </div>
            </div>
        `);
    }

    render_roles_team($el) {
        const roles = [
            { role: __("CD Manager"), desc: __("Full access: settings, reports, staff, menu"), color: "#F59E0B", icon: "👔" },
            { role: __("CD Admin"), desc: __("System configuration, branches, POS setup"), color: "#D97706", icon: "⚙️" },
            { role: __("CD Chef"), desc: __("Kitchen display, order queue, recipe management"), color: "#EF4444", icon: "👨‍🍳" },
            { role: __("CD Waiter"), desc: __("Take orders, table service, reservations"), color: "#3B82F6", icon: "🍽️" },
            { role: __("CD Cashier"), desc: __("POS, billing, payments, shift closing"), color: "#10B981", icon: "💰" },
            { role: __("CD Delivery"), desc: __("Online orders, delivery tracking, zones"), color: "#8B5CF6", icon: "🚚" },
        ];

        $el.html(`
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px">
                ${roles.map(r => `
                    <div class="fv-fx-hover-lift" style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:18px;border-inline-start:4px solid ${r.color}">
                        <div style="font-size:1.6rem;margin-bottom:6px">${r.icon}</div>
                        <div style="font-weight:700;font-size:0.95rem;color:${r.color}">${r.role}</div>
                        <div style="font-size:0.8rem;color:var(--text-muted);margin-top:4px">${r.desc}</div>
                    </div>
                `).join("")}
            </div>
        `);
    }

    render_order_workflow($el) {
        const states = [
            { label: __("New Order"), icon: "📋", color: "#3B82F6", desc: __("Customer places order via waiter or online") },
            { label: __("Sent to Kitchen"), icon: "🔔", color: "#F59E0B", desc: __("Order appears on Kitchen Display System") },
            { label: __("Preparing"), icon: "👨‍🍳", color: "#D97706", desc: __("Chef starts preparation, timer begins") },
            { label: __("Ready"), icon: "✅", color: "#10B981", desc: __("Food ready for serving or pickup") },
            { label: __("Served"), icon: "🍽️", color: "#6366F1", desc: __("Delivered to table or customer") },
            { label: __("Paid"), icon: "💰", color: "#059669", desc: __("Payment processed, invoice generated") },
        ];

        $el.html(`
            <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:center">
                ${states.map((s, i) => `
                    <div style="display:flex;align-items:center;gap:8px">
                        <div class="fv-fx-hover-lift" style="background:${s.color}15;border:2px solid ${s.color};border-radius:12px;padding:14px 18px;text-align:center;min-width:120px">
                            <div style="font-size:1.5rem">${s.icon}</div>
                            <div style="font-size:0.85rem;font-weight:700;color:${s.color};margin-top:4px">${s.label}</div>
                            <div style="font-size:0.7rem;color:var(--text-muted);margin-top:2px">${s.desc}</div>
                        </div>
                        ${i < states.length - 1 ? '<div style="font-size:1.2rem;color:var(--text-muted)">→</div>' : ''}
                    </div>
                `).join("")}
            </div>
        `);
    }

    render_pos_billing($el) {
        const actions = [
            { label: __("POS Profile"), route: "pos-profile", icon: "🖥️" },
            { label: __("Open POS"), route: "pos-invoice/new", icon: "💳" },
            { label: __("POS Shift"), route: "pos-shift/new", icon: "🔄" },
        ];

        $el.html(`
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:20px">
                ${actions.map(a => `
                    <div class="fv-fx-hover-lift" style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:16px;cursor:pointer;text-align:center"
                         onclick="frappe.set_route('${a.route}')">
                        <div style="font-size:2rem;margin-bottom:8px">${a.icon}</div>
                        <div style="font-size:0.9rem;font-weight:600">${a.label}</div>
                    </div>
                `).join("")}
            </div>
            <div class="fv-fx-glass" style="padding:20px;border-radius:12px">
                <h4 style="font-weight:600">${__("POS Workflow — سير عمل نقطة البيع")}</h4>
                <div style="font-size:0.9rem;line-height:2;color:var(--text-muted)">
                    1️⃣ ${__("Open POS Shift at start of day")}<br>
                    2️⃣ ${__("Process orders → auto-creates POS Invoice")}<br>
                    3️⃣ ${__("Accept payments: Cash, Card, Split")}<br>
                    4️⃣ ${__("Close POS Shift → reconcile cash drawer")}<br>
                    5️⃣ ${__("Daily Closing → generate end-of-day report")}
                </div>
            </div>
        `);
    }

    render_reservations($el) {
        const actions = [
            { label: __("New Reservation"), route: "table-reservation/new", icon: "📅" },
            { label: __("View Calendar"), route: "table-reservation?view=Calendar", icon: "📆" },
            { label: __("Table Map"), route: "restaurant-table", icon: "🗺️" },
        ];

        $el.html(`
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:20px">
                ${actions.map(a => `
                    <div class="fv-fx-hover-lift" style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:16px;cursor:pointer;text-align:center"
                         onclick="frappe.set_route('${a.route}')">
                        <div style="font-size:2rem;margin-bottom:8px">${a.icon}</div>
                        <div style="font-size:0.9rem;font-weight:600">${a.label}</div>
                    </div>
                `).join("")}
            </div>
            <div style="background:var(--card-bg);border-radius:12px;padding:20px;border:1px solid var(--border-color)">
                <h4 style="font-weight:600">${__("Reservation Flow — مسار الحجز")}</h4>
                <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:12px">
                    ${["📞 " + __("Received"), "✅ " + __("Confirmed"), "🪑 " + __("Seated"), "✔️ " + __("Completed"), "❌ " + __("Cancelled")].map(s =>
                        `<span style="background:var(--bg-color);border:1px solid var(--border-color);border-radius:20px;padding:6px 14px;font-size:0.8rem">${s}</span>`
                    ).join("→ ")}
                </div>
            </div>
        `);
    }

    render_advanced($el) {
        const features = [
            { title: __("Online Ordering"), desc: __("Accept orders from website, WhatsApp, or third-party platforms"), icon: "🌐" },
            { title: __("Delivery Zones"), desc: __("Define delivery areas with minimum orders and delivery fees"), icon: "🚚" },
            { title: __("Marketing Campaigns"), desc: __("Create promos, track influencers, manage social presence"), icon: "📣" },
            { title: __("Customer Reviews"), desc: __("Collect feedback, respond to reviews, track satisfaction"), icon: "⭐" },
            { title: __("Inventory Tracking"), desc: __("Track ingredients, auto-deduct on orders, low stock alerts"), icon: "📦" },
            { title: __("Staff Scheduling"), desc: __("Manage shifts, attendance, and performance metrics"), icon: "📋" },
        ];

        $el.html(`
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px">
                ${features.map(f => `
                    <div class="fv-fx-hover-lift fv-fx-glass" style="padding:18px;border-radius:12px">
                        <div style="font-size:1.6rem;margin-bottom:8px">${f.icon}</div>
                        <div style="font-weight:700;font-size:0.95rem">${f.title}</div>
                        <div style="font-size:0.8rem;color:var(--text-muted);margin-top:4px">${f.desc}</div>
                    </div>
                `).join("")}
            </div>
        `);
    }

    render_go_live($el) {
        $el.html(`
            <div style="text-align:center;padding:20px">
                <div style="font-size:4rem;margin-bottom:16px">🎉</div>
                <h3 style="font-weight:700">${__("You're Ready to Go Live!")}</h3>
                <p style="color:var(--text-muted)">${__("أنت جاهز للبدء! — Review the checklist below and start serving customers.")}</p>
            </div>
            <div class="fv-fx-glass" style="padding:24px;border-radius:12px;margin-top:16px">
                <h4 style="font-weight:600">${__("Launch Checklist — قائمة الإطلاق")}</h4>
                ${this.checklist_item(__("Restaurant settings configured"))}
                ${this.checklist_item(__("Tables and kitchen stations created"))}
                ${this.checklist_item(__("Menu items with prices added"))}
                ${this.checklist_item(__("Roles assigned to team members"))}
                ${this.checklist_item(__("POS profile and payment methods set"))}
                ${this.checklist_item(__("Test order placed and processed"))}
                ${this.checklist_item(__("Daily closing workflow tested"))}
            </div>
            <div style="text-align:center;margin-top:24px">
                <button class="btn btn-primary btn-lg" onclick="frappe.set_route('candela-dashboard')" style="background:#F59E0B;border-color:#F59E0B;padding:12px 40px;font-size:1rem;border-radius:12px">
                    ${__("Open Dashboard — فتح لوحة التحكم")} 🚀
                </button>
            </div>
        `);
    }

    feature_card(icon, title, desc) {
        return `
            <div class="fv-fx-hover-lift" style="background:var(--card-bg);border:1px solid var(--border-color);border-radius:12px;padding:18px">
                <div style="font-size:1.6rem;margin-bottom:8px">${icon}</div>
                <div style="font-weight:700;font-size:0.9rem">${title}</div>
                <div style="font-size:0.8rem;color:var(--text-muted);margin-top:4px">${desc}</div>
            </div>
        `;
    }

    checklist_item(label) {
        return `
            <div style="display:flex;align-items:center;gap:10px;padding:6px 0">
                <div style="width:20px;height:20px;border-radius:4px;border:2px solid var(--border-color);flex-shrink:0"></div>
                <span style="font-size:0.9rem">${label}</span>
            </div>
        `;
    }

    render_navigation() {
        const $nav = $("#onboarding-nav");
        const is_first = this.current_step === 0;
        const is_last = this.current_step === this.steps.length - 1;

        $nav.html(`
            <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 0;border-top:1px solid var(--border-color)">
                <button class="btn btn-default btn-sm" ${is_first ? 'disabled' : ''} id="btn-prev"
                        style="border-radius:8px;padding:8px 20px">
                    ← ${__("Previous")}
                </button>
                <span style="font-size:0.85rem;color:var(--text-muted)">
                    ${this.current_step + 1} / ${this.steps.length}
                </span>
                <button class="btn btn-primary btn-sm" id="btn-next"
                        style="border-radius:8px;padding:8px 20px;background:#F59E0B;border-color:#F59E0B">
                    ${is_last ? __("Finish") + " ✓" : __("Next") + " →"}
                </button>
            </div>
        `);

        $nav.find("#btn-prev").on("click", () => {
            if (this.current_step > 0) {
                this.completed_steps.add(this.current_step);
                this.current_step--;
                this.render_progress();
                this.render_step_content();
                this.render_navigation();
            }
        });

        $nav.find("#btn-next").on("click", () => {
            this.completed_steps.add(this.current_step);
            if (this.current_step < this.steps.length - 1) {
                this.current_step++;
                this.render_progress();
                this.render_step_content();
                this.render_navigation();
            } else {
                frappe.set_route("candela-dashboard");
            }
        });
    }
}
