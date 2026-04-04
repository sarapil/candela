// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT
// For license information, please see license.txt

/**
 * Candela About — 10-Slide Storyboard Showcase
 * Uses frappe.visual.storyboard(), appMap(), erd(), dependencyGraph()
 * Target: admins, executives, decision makers
 */
(function () {
	"use strict";

	const AMBER = "#F59E0B";
	const DARK  = "#1C1917";

	/* ── SVG Illustrations ─────────────────────────────── */
	const heroSVG = `<svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg">
		<defs>
			<linearGradient id="cag" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0%" stop-color="${AMBER}"/>
				<stop offset="100%" stop-color="#D97706"/>
			</linearGradient>
			<filter id="glow"><feGaussianBlur stdDeviation="4" result="b"/>
				<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
			</filter>
		</defs>
		<rect rx="16" width="400" height="260" fill="${DARK}" opacity=".95"/>
		<!-- candle body -->
		<rect x="180" y="110" width="40" height="90" rx="6" fill="url(#cag)"/>
		<!-- flame -->
		<ellipse cx="200" cy="95" rx="14" ry="22" fill="#FBBF24" filter="url(#glow)">
			<animate attributeName="ry" values="22;18;22" dur="1.5s" repeatCount="indefinite"/>
			<animate attributeName="rx" values="14;11;14" dur="2s" repeatCount="indefinite"/>
		</ellipse>
		<ellipse cx="200" cy="90" rx="6" ry="12" fill="#FEF3C7">
			<animate attributeName="ry" values="12;9;12" dur="1.2s" repeatCount="indefinite"/>
		</ellipse>
		<!-- plate -->
		<ellipse cx="200" cy="205" rx="70" ry="12" fill="#78716C" opacity=".4"/>
		<!-- text -->
		<text x="200" y="245" text-anchor="middle" fill="#FBBF24" font-size="18" font-weight="700" font-family="serif">C A N D E L A</text>
	</svg>`;

	/* ── Slide Definitions ─────────────────────────────── */
	function getSlides() {
		return [
			/* 1 — App Overview */
			{
				title: __("🕯️ Candela Restaurant"),
				content: `
					<div style="text-align:center;margin-bottom:24px">${heroSVG}</div>
					<div class="cd-glass-card">
						<h3>${__("Italian Café & Restaurant Management")}</h3>
						<p>${__("A complete restaurant operations platform covering menu management, table reservations, online ordering, POS, kitchen display, procurement, inventory, production tracking, staff management, marketing campaigns, and a stunning customer-facing website.")}</p>
						<div class="cd-feature-grid">
							${featureCard("🍽️", __("Menu & Dining"), __("Full menu management with categories, dietary tags, ingredients, and pricing"))}
							${featureCard("📱", __("Online Ordering"), __("Customer website with real-time order tracking and delivery zones"))}
							${featureCard("💰", __("POS System"), __("Point of sale with shift management and daily closing reconciliation"))}
							${featureCard("👨‍🍳", __("Kitchen Display"), __("Real-time kitchen station management and production logging"))}
							${featureCard("📦", __("Procurement"), __("Purchase requests, orders, goods receipt, supplier management"))}
							${featureCard("📊", __("Analytics"), __("Sales reports, food cost analysis, inventory tracking, marketing ROI"))}
						</div>
					</div>`
			},
			/* 2 — Module Map */
			{
				title: __("📐 Module Architecture"),
				content: `
					<div class="cd-glass-card">
						<p>${__("Candela is organized into 8 functional modules, each with dedicated DocTypes and workflows:")}</p>
						<div id="cd-about-appmap" style="height:450px;border-radius:12px;overflow:hidden;background:${DARK}"></div>
					</div>`,
				onMount(container) {
					const el = container.querySelector("#cd-about-appmap");
					if (el && frappe.visual && frappe.visual.appMap) {
						frappe.visual.appMap({
							container: el,
							app: "candela",
							layout: "elk",
							theme: "dark",
							highlight_module: "Candela"
						});
					}
				}
			},
			/* 3 — Entity Relationships */
			{
				title: __("🔗 Entity Relationship Diagram"),
				content: `
					<div class="cd-glass-card">
						<p>${__("How Candela's 55 DocTypes connect to each other — from Menu Items to POS Invoices to Stock Entries:")}</p>
						<div id="cd-about-erd" style="height:500px;border-radius:12px;overflow:hidden;background:${DARK}"></div>
					</div>`,
				onMount(container) {
					const el = container.querySelector("#cd-about-erd");
					if (el && frappe.visual && frappe.visual.erd) {
						frappe.visual.erd({
							container: el,
							app: "candela",
							module: "Candela",
							theme: "dark",
							layout: "elk"
						});
					}
				}
			},
			/* 4 — Workflow Visualization */
			{
				title: __("⚡ Business Workflows"),
				content: `
					<div class="cd-glass-card">
						<p>${__("Every operation in Candela follows a clear workflow — from customer order to kitchen production to payment:")}</p>
						<div id="cd-about-workflow" style="height:450px;border-radius:12px;overflow:hidden;background:${DARK}"></div>
					</div>`,
				onMount(container) {
					const el = container.querySelector("#cd-about-workflow");
					if (el && frappe.visual && frappe.visual.dependencyGraph) {
						frappe.visual.dependencyGraph({
							container: el,
							theme: "dark",
							nodes: [
								{ id: "customer", label: __("Customer"), icon: "user", group: "front" },
								{ id: "reservation", label: __("Reservation"), icon: "calendar", group: "front" },
								{ id: "online_order", label: __("Online Order"), icon: "device-mobile", group: "front" },
								{ id: "pos", label: __("POS Invoice"), icon: "receipt", group: "ops" },
								{ id: "kitchen", label: __("Kitchen Queue"), icon: "chef-hat", group: "ops" },
								{ id: "production", label: __("Production Log"), icon: "tools-kitchen-2", group: "ops" },
								{ id: "stock_deduct", label: __("Stock Deduction"), icon: "package", group: "inv" },
								{ id: "purchase_req", label: __("Purchase Request"), icon: "shopping-cart", group: "inv" },
								{ id: "purchase_order", label: __("Purchase Order"), icon: "file-invoice", group: "inv" },
								{ id: "grn", label: __("Goods Receipt"), icon: "truck-delivery", group: "inv" },
								{ id: "stock_entry", label: __("Stock Entry"), icon: "database", group: "inv" },
								{ id: "daily_closing", label: __("Daily Closing"), icon: "report-money", group: "fin" },
								{ id: "reports", label: __("Reports"), icon: "chart-bar", group: "fin" }
							],
							edges: [
								{ source: "customer", target: "reservation" },
								{ source: "customer", target: "online_order" },
								{ source: "reservation", target: "pos" },
								{ source: "online_order", target: "kitchen" },
								{ source: "pos", target: "kitchen" },
								{ source: "kitchen", target: "production" },
								{ source: "production", target: "stock_deduct" },
								{ source: "stock_deduct", target: "purchase_req" },
								{ source: "purchase_req", target: "purchase_order" },
								{ source: "purchase_order", target: "grn" },
								{ source: "grn", target: "stock_entry" },
								{ source: "pos", target: "daily_closing" },
								{ source: "daily_closing", target: "reports" }
							],
							groups: {
								front: { label: __("Customer Facing"), color: "#F59E0B" },
								ops:   { label: __("Operations"), color: "#059669" },
								inv:   { label: __("Inventory"), color: "#3B82F6" },
								fin:   { label: __("Finance"), color: "#8B5CF6" }
							}
						});
					}
				}
			},
			/* 5 — Stakeholder Perspectives */
			{
				title: __("👥 Stakeholder Perspectives"),
				content: `
					<div class="cd-glass-card">
						<h4>${__("Each team member sees exactly what they need:")}</h4>
						<div class="cd-persona-grid">
							${personaCard("👨‍💼", __("Restaurant Manager"), [
								__("Full dashboard with sales, reservations, and alerts"),
								__("Staff schedule and shift management"),
								__("Procurement approval and cost reports"),
								__("Daily closing reconciliation")
							])}
							${personaCard("👨‍🍳", __("Chef / Kitchen Staff"), [
								__("Kitchen Display System with order queue"),
								__("Production logging and waste tracking"),
								__("Recipe ingredient lists"),
								__("Stock level alerts for key ingredients")
							])}
							${personaCard("💁", __("Waiter / Front Staff"), [
								__("Table status map — available, occupied, reserved"),
								__("POS terminal for order taking"),
								__("Reservation list for the day"),
								__("Customer preferences and notes")
							])}
							${personaCard("🛒", __("Procurement Officer"), [
								__("Purchase requests from kitchen"),
								__("Supplier management and ordering"),
								__("Goods receipt and quality checks"),
								__("Inventory levels and reorder points")
							])}
							${personaCard("📢", __("Marketing Manager"), [
								__("Campaign management and activity tracking"),
								__("Promo code creation and analytics"),
								__("Customer reviews and ratings"),
								__("Newsletter subscriber management")
							])}
							${personaCard("💰", __("Cashier"), [
								__("POS shift open/close"),
								__("Invoice creation and payment"),
								__("Daily expense recording"),
								__("Shift reconciliation")
							])}
						</div>
					</div>`
			},
			/* 6 — Industry Use-Cases */
			{
				title: __("🏢 Industry Adaptations"),
				content: `
					<div class="cd-glass-card">
						<h4>${__("Candela adapts to different food service businesses:")}</h4>
						<div class="cd-use-case-grid">
							${useCaseCard("🍝", __("Fine Dining Restaurant"), __("Table reservations, multi-course menu management, wine pairing notes, premium customer experience tracking, event hosting"))}
							${useCaseCard("☕", __("Café & Coffee Shop"), __("Quick service POS, loyalty programs, pastry production tracking, morning shift management, takeaway orders"))}
							${useCaseCard("🍕", __("Delivery-First Kitchen"), __("Online ordering focus, delivery zone management, driver tracking, promo codes, customer acquisition campaigns"))}
							${useCaseCard("🏨", __("Hotel Restaurant"), __("Room-charge integration, banquet event management, multi-outlet operations, corporate account billing"))}
							${useCaseCard("🍱", __("Corporate Catering"), __("Corporate lunch packages, bulk ordering, recurring meal plans, dietary accommodation tracking, invoice consolidation"))}
							${useCaseCard("🎉", __("Event & Banquet Hall"), __("Event booking with custom menus, large-scale production planning, temporary staff scheduling, venue asset management"))}
						</div>
					</div>`
			},
			/* 7 — Integration Map */
			{
				title: __("🔌 Integrations"),
				content: `
					<div class="cd-glass-card">
						<h4>${__("Candela connects with the Arkan Lab ecosystem:")}</h4>
						<div id="cd-about-integrations" style="height:400px;border-radius:12px;overflow:hidden;background:${DARK}"></div>
					</div>`,
				onMount(container) {
					const el = container.querySelector("#cd-about-integrations");
					if (el && frappe.visual && frappe.visual.dependencyGraph) {
						frappe.visual.dependencyGraph({
							container: el,
							theme: "dark",
							nodes: [
								{ id: "candela", label: "Candela", icon: "flame", group: "core", size: "lg" },
								{ id: "erpnext", label: "ERPNext", icon: "building-store", group: "erp" },
								{ id: "hrms", label: "HRMS", icon: "users", group: "erp" },
								{ id: "caps", label: "CAPS", icon: "shield-lock", group: "security" },
								{ id: "frappe_visual", label: "Frappe Visual", icon: "chart-dots-3", group: "ui" },
								{ id: "payments", label: "Payments", icon: "credit-card", group: "erp" },
								{ id: "website", label: __("Customer Website"), icon: "world", group: "public" },
								{ id: "whatsapp", label: "WhatsApp", icon: "brand-whatsapp", group: "channels" }
							],
							edges: [
								{ source: "candela", target: "erpnext", label: __("Accounting") },
								{ source: "candela", target: "hrms", label: __("Staff") },
								{ source: "candela", target: "caps", label: __("Permissions") },
								{ source: "candela", target: "frappe_visual", label: __("UI Components") },
								{ source: "candela", target: "payments", label: __("Online Pay") },
								{ source: "candela", target: "website", label: __("Public Pages") },
								{ source: "candela", target: "whatsapp", label: __("Notifications") }
							],
							groups: {
								core:     { label: "Candela", color: AMBER },
								erp:      { label: __("ERP"), color: "#3B82F6" },
								security: { label: __("Security"), color: "#EF4444" },
								ui:       { label: __("UI"), color: "#8B5CF6" },
								public:   { label: __("Public"), color: "#059669" },
								channels: { label: __("Channels"), color: "#10B981" }
							}
						});
					}
				}
			},
			/* 8 — Security & Permissions */
			{
				title: __("🛡️ Security & Permissions"),
				content: `
					<div class="cd-glass-card">
						<h4>${__("CAPS — Capability-Based Access Control")}</h4>
						<p>${__("Candela uses CAPS for fine-grained permissions with 21 capabilities across 6 bundles:")}</p>
						<div class="cd-caps-grid">
							${capsCard(__("Module Access"), ["CD_view_dashboard", "CD_manage_settings", "CD_view_reports"])}
							${capsCard(__("Menu Management"), ["CD_manage_menu", "CD_manage_pricing", "CD_view_recipes"])}
							${capsCard(__("Operations"), ["CD_manage_reservations", "CD_manage_orders", "CD_manage_pos"])}
							${capsCard(__("Kitchen"), ["CD_view_kitchen", "CD_manage_production", "CD_log_waste"])}
							${capsCard(__("Procurement"), ["CD_create_purchase_request", "CD_approve_purchases", "CD_receive_goods"])}
							${capsCard(__("Finance"), ["CD_view_cost_data", "CD_manage_closing", "CD_export_reports"])}
						</div>
						<p style="margin-top:16px;opacity:.8">${__("Field-level restrictions mask cost data from non-authorized roles. All permission changes are audited.")}</p>
					</div>`
			},
			/* 9 — Reports & Analytics */
			{
				title: __("📊 Reports & Analytics"),
				content: `
					<div class="cd-glass-card">
						<h4>${__("Data-Driven Restaurant Management")}</h4>
						<div class="cd-reports-grid">
							${reportCard("💰", __("Sales Dashboard"), __("Real-time revenue by hour, day, week. Top-selling items. Payment method breakdown."))}
							${reportCard("🍕", __("Food Cost Report"), __("Cost per dish, ingredient price trends, waste percentage, profit margins per menu category."))}
							${reportCard("📦", __("Inventory Status"), __("Current stock levels, reorder alerts, consumption rate, shelf life tracking."))}
							${reportCard("📅", __("Reservation Analytics"), __("Booking patterns, no-show rates, peak hours, table utilization."))}
							${reportCard("⭐", __("Customer Insights"), __("Review sentiment, order frequency, popular delivery zones, promo code usage."))}
							${reportCard("👥", __("Staff Performance"), __("Shift coverage, POS sales per cashier, kitchen throughput, overtime tracking."))}
						</div>
					</div>`
			},
			/* 10 — Getting Started */
			{
				title: __("🚀 Getting Started"),
				content: `
					<div class="cd-glass-card" style="text-align:center">
						${heroSVG}
						<h3 style="margin-top:24px">${__("Ready to light the flame?")}</h3>
						<p>${__("Follow these steps to get your restaurant running on Candela:")}</p>
						<div class="cd-steps-grid">
							${stepCard("1", __("Configure Settings"), __("Set restaurant name, address, opening hours, and currency in Candela Settings"))}
							${stepCard("2", __("Build Your Menu"), __("Create menu categories, add items with ingredients, pricing, and photos"))}
							${stepCard("3", __("Set Up Tables"), __("Define your floor plan with table numbers, capacities, and zones"))}
							${stepCard("4", __("Add Staff"), __("Create users and assign roles: Manager, Chef, Waiter, Cashier, Procurement"))}
							${stepCard("5", __("Configure Operations"), __("Set up warehouses, suppliers, kitchen stations, and delivery zones"))}
							${stepCard("6", __("Go Live!"), __("Open your first POS shift, take your first reservation, and start serving!"))}
						</div>
						<div style="margin-top:32px">
							<a class="btn btn-primary btn-lg" href="/app/candela-settings" style="background:${AMBER};border-color:${AMBER};color:${DARK};font-weight:700">
								${__("Open Candela Settings")} →
							</a>
						</div>
					</div>`
			}
		];
	}

	/* ── Helper: Card Builders ─────────────────────────── */
	function featureCard(icon, title, desc) {
		return `<div class="cd-feat-card"><span class="cd-feat-icon">${icon}</span><strong>${title}</strong><small>${desc}</small></div>`;
	}
	function personaCard(icon, title, items) {
		return `<div class="cd-persona-card"><div class="cd-persona-header">${icon} ${title}</div><ul>${items.map(i => `<li>${i}</li>`).join("")}</ul></div>`;
	}
	function useCaseCard(icon, title, desc) {
		return `<div class="cd-use-card"><span style="font-size:2rem">${icon}</span><strong>${title}</strong><p>${desc}</p></div>`;
	}
	function capsCard(title, caps) {
		return `<div class="cd-caps-card"><strong>${title}</strong>${caps.map(c => `<code>${c}</code>`).join("")}</div>`;
	}
	function reportCard(icon, title, desc) {
		return `<div class="cd-report-card">${icon} <strong>${title}</strong><p>${desc}</p></div>`;
	}
	function stepCard(num, title, desc) {
		return `<div class="cd-step-card"><div class="cd-step-num">${num}</div><strong>${title}</strong><p>${desc}</p></div>`;
	}

	/* ── Mount ─────────────────────────────────────────── */
	function mount() {
		const root = document.getElementById("candela-about-root");
		if (!root) return;

		// Inject styles
		if (!document.getElementById("cd-about-css")) {
			const style = document.createElement("style");
			style.id = "cd-about-css";
			style.textContent = getCSS();
			document.head.appendChild(style);
		}

		// Check if frappe.visual is available
		if (frappe.visual && frappe.visual.storyboard) {
			frappe.visual.storyboard({
				container: root,
				slides: getSlides(),
				theme: "dark",
				nav_position: "both",         // top AND bottom
				show_progress: true,
				transition: "slide",
				brand_color: AMBER
			});
		} else {
			// Fallback: render slides as simple HTML sections
			renderFallback(root);
		}
	}

	function renderFallback(root) {
		const slides = getSlides();
		let currentSlide = 0;

		function render() {
			const slide = slides[currentSlide];
			root.innerHTML = `
				<div class="cd-about-fallback">
					<div class="cd-about-nav-top">
						<button class="btn btn-sm btn-default cd-prev" ${currentSlide === 0 ? "disabled" : ""}>${__("← Previous")}</button>
						<span class="cd-about-counter">${currentSlide + 1} / ${slides.length}</span>
						<button class="btn btn-sm btn-primary cd-next" style="background:${AMBER};border-color:${AMBER};color:${DARK}" ${currentSlide === slides.length - 1 ? "disabled" : ""}>${__("Next →")}</button>
					</div>
					<h2 style="text-align:center;margin:20px 0;color:${AMBER}">${slide.title}</h2>
					<div class="cd-about-slide-content">${slide.content}</div>
					<div class="cd-about-nav-bottom">
						<button class="btn btn-sm btn-default cd-prev" ${currentSlide === 0 ? "disabled" : ""}>${__("← Previous")}</button>
						<span class="cd-about-counter">${currentSlide + 1} / ${slides.length}</span>
						<button class="btn btn-sm btn-primary cd-next" style="background:${AMBER};border-color:${AMBER};color:${DARK}" ${currentSlide === slides.length - 1 ? "disabled" : ""}>${__("Next →")}</button>
					</div>
				</div>`;

			root.querySelectorAll(".cd-prev").forEach(btn =>
				btn.addEventListener("click", () => { if (currentSlide > 0) { currentSlide--; render(); } })
			);
			root.querySelectorAll(".cd-next").forEach(btn =>
				btn.addEventListener("click", () => { if (currentSlide < slides.length - 1) { currentSlide++; render(); } })
			);

			if (slide.onMount) {
				setTimeout(() => slide.onMount(root), 100);
			}
		}
		render();
	}

	/* ── CSS ───────────────────────────────────────────── */
	function getCSS() {
		return `
		.cd-glass-card{background:rgba(28,25,23,.7);backdrop-filter:blur(16px);border:1px solid rgba(245,158,11,.15);border-radius:16px;padding:28px;margin:16px 0;color:#FEF3C7}
		.cd-glass-card h3,.cd-glass-card h4{color:#F59E0B;margin-bottom:12px}
		.cd-glass-card p{color:#D6D3D1;line-height:1.7}
		.cd-feature-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:20px}
		.cd-feat-card{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:6px}
		.cd-feat-icon{font-size:1.5rem}
		.cd-feat-card strong{color:#FBBF24}
		.cd-feat-card small{color:#A8A29E;font-size:.85rem;line-height:1.4}
		.cd-persona-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-top:16px}
		.cd-persona-card{background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.15);border-radius:12px;padding:16px}
		.cd-persona-header{font-size:1.1rem;font-weight:700;color:#FBBF24;margin-bottom:8px}
		.cd-persona-card ul{margin:0;padding-left:20px;color:#D6D3D1;font-size:.9rem;line-height:1.8}
		.cd-use-case-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:16px}
		.cd-use-card{background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.15);border-radius:12px;padding:20px;display:flex;flex-direction:column;gap:8px}
		.cd-use-card strong{color:#FBBF24}
		.cd-use-card p{color:#A8A29E;font-size:.88rem;margin:0;line-height:1.5}
		.cd-caps-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:16px}
		.cd-caps-card{background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:14px;display:flex;flex-direction:column;gap:6px}
		.cd-caps-card strong{color:#FCA5A5;font-size:.95rem}
		.cd-caps-card code{background:rgba(0,0,0,.3);color:#FBBF24;padding:2px 8px;border-radius:4px;font-size:.78rem;display:inline-block;margin:2px 0}
		.cd-reports-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px;margin-top:16px}
		.cd-report-card{background:rgba(59,130,246,.06);border:1px solid rgba(59,130,246,.2);border-radius:12px;padding:16px}
		.cd-report-card strong{color:#93C5FD}
		.cd-report-card p{color:#A8A29E;font-size:.88rem;margin:6px 0 0;line-height:1.5}
		.cd-steps-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;margin-top:24px;text-align:left}
		.cd-step-card{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:12px;padding:16px;position:relative}
		.cd-step-num{position:absolute;top:-10px;left:14px;background:${AMBER};color:${DARK};width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.9rem}
		.cd-step-card strong{color:#FBBF24;display:block;margin-top:10px}
		.cd-step-card p{color:#A8A29E;font-size:.85rem;margin:6px 0 0;line-height:1.4}
		.cd-about-fallback{max-width:900px;margin:0 auto;padding:20px}
		.cd-about-nav-top,.cd-about-nav-bottom{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid rgba(245,158,11,.15)}
		.cd-about-nav-bottom{border-bottom:none;border-top:1px solid rgba(245,158,11,.15);margin-top:20px}
		.cd-about-counter{color:#A8A29E;font-size:.9rem}
		`;
	}

	/* ── Init ──────────────────────────────────────────── */
	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", mount);
	} else {
		mount();
	}
})();
