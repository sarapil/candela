/**
 * Candela Onboarding & Contextual Help System
 * Uses frappe.visual.storyboard() inside frappe.visual.floatingWindow()
 * Accessible from ❓ button on every form toolbar, report, and settings
 */
(function () {
	"use strict";

	const AMBER = "#F59E0B";
	const DARK  = "#1C1917";

	window.candela = window.candela || {};

	/* ═══════════════════════════════════════════════════════
	   GENERAL ONBOARDING — for all users
	   ═══════════════════════════════════════════════════════ */
	window.candela.onboarding = {
		startGeneral(containerSelector) {
			const slides = getGeneralSlides();
			if (containerSelector) {
				renderInContainer(containerSelector, slides);
			} else {
				renderInFloatingWindow(__("Candela Onboarding"), slides);
			}
		},

		startForRole(role) {
			const slides = getRoleSlides(role);
			renderInFloatingWindow(__("{0} Guide", [role]), slides);
		}
	};

	/* ═══════════════════════════════════════════════════════
	   CONTEXTUAL HELP — topic-specific micro-tutorials
	   ═══════════════════════════════════════════════════════ */
	window.candela.help = {
		open(topic) {
			const slides = getHelpSlides(topic);
			if (slides.length) {
				renderInFloatingWindow(__("Help: {0}", [topic]), slides);
			} else {
				frappe.msgprint(__("No help available for this topic yet."));
			}
		}
	};

	/* ── General Onboarding Slides ─────────────────────── */
	function getGeneralSlides() {
		return [
			{
				title: __("🕯️ Welcome to Candela!"),
				content: `
					<div class="cd-onboard-card">
						<p style="font-size:1.1rem;text-align:center">${__("Candela is your complete restaurant management platform. Let's walk through everything it can do!")}</p>
						<div class="cd-onboard-grid">
							${oCard("🍽️", __("Menu"), __("Create and manage your full menu with categories, items, ingredients, dietary tags, and pricing"))}
							${oCard("📱", __("Orders"), __("Take orders via POS terminal or online website — both flow into the same kitchen queue"))}
							${oCard("📅", __("Reservations"), __("Customers book tables online — you manage availability and send confirmations"))}
							${oCard("👨‍🍳", __("Kitchen"), __("Real-time kitchen display shows incoming orders organized by station"))}
							${oCard("📦", __("Inventory"), __("Track ingredients, create purchase requests, receive goods, do stock counts"))}
							${oCard("📊", __("Reports"), __("Sales analysis, food cost reports, reservation analytics, staff performance"))}
						</div>
					</div>`
			},
			{
				title: __("🗂️ DocType Relationships"),
				content: `
					<div class="cd-onboard-card">
						<p>${__("Here's how all the data in Candela connects together:")}</p>
						<div id="cd-onboard-erd" style="height:400px;border-radius:12px;overflow:hidden;background:${DARK}"></div>
					</div>`,
				onMount(container) {
					const el = container.querySelector("#cd-onboard-erd");
					if (el && frappe.visual && frappe.visual.erd) {
						frappe.visual.erd({ container: el, app: "candela", module: "Candela", theme: "dark", layout: "elk" });
					}
				}
			},
			{
				title: __("⚡ Core Workflow"),
				content: `
					<div class="cd-onboard-card">
						<p>${__("The typical flow from customer to cash register:")}</p>
						<div id="cd-onboard-flow" style="height:350px;border-radius:12px;overflow:hidden;background:${DARK}"></div>
						<ol class="cd-flow-steps">
							<li>${__("Customer makes a reservation or places an order online")}</li>
							<li>${__("Order appears in kitchen display, organized by station")}</li>
							<li>${__("Chef prepares food, marks production log with ingredients used")}</li>
							<li>${__("Stock is automatically deducted from inventory")}</li>
							<li>${__("Cashier creates POS invoice and processes payment")}</li>
							<li>${__("Manager reviews daily closing report")}</li>
						</ol>
					</div>`,
				onMount(container) {
					const el = container.querySelector("#cd-onboard-flow");
					if (el && frappe.visual && frappe.visual.dependencyGraph) {
						frappe.visual.dependencyGraph({
							container: el, theme: "dark",
							nodes: [
								{ id: "order", label: __("Order"), icon: "shopping-cart" },
								{ id: "kitchen", label: __("Kitchen"), icon: "chef-hat" },
								{ id: "produce", label: __("Produce"), icon: "tools-kitchen-2" },
								{ id: "stock", label: __("Stock"), icon: "package" },
								{ id: "pay", label: __("Payment"), icon: "cash" },
								{ id: "close", label: __("Closing"), icon: "report-money" }
							],
							edges: [
								{ source: "order", target: "kitchen" },
								{ source: "kitchen", target: "produce" },
								{ source: "produce", target: "stock" },
								{ source: "order", target: "pay" },
								{ source: "pay", target: "close" }
							]
						});
					}
				}
			},
			{
				title: __("🔐 Your Permissions"),
				content: `
					<div class="cd-onboard-card">
						<p>${__("Candela uses role-based access control with CAPS (Capability Access Permission System):")}</p>
						<table class="table table-bordered" style="color:#D6D3D1;font-size:.9rem">
							<thead><tr style="color:${AMBER}"><th>${__("Role")}</th><th>${__("Can Access")}</th></tr></thead>
							<tbody>
								<tr><td><strong>${__("Manager")}</strong></td><td>${__("Everything — settings, reports, approvals, staff management")}</td></tr>
								<tr><td><strong>${__("Chef")}</strong></td><td>${__("Kitchen display, production logs, recipes, ingredient stock levels")}</td></tr>
								<tr><td><strong>${__("Waiter")}</strong></td><td>${__("Table map, POS, reservations, customer notes")}</td></tr>
								<tr><td><strong>${__("Cashier")}</strong></td><td>${__("POS terminal, shift management, daily expenses")}</td></tr>
								<tr><td><strong>${__("Procurement")}</strong></td><td>${__("Purchase requests/orders, suppliers, goods receipt, inventory")}</td></tr>
								<tr><td><strong>${__("Marketing")}</strong></td><td>${__("Campaigns, promo codes, reviews, newsletter, events")}</td></tr>
							</tbody>
						</table>
					</div>`
			},
			{
				title: __("❓ Getting Help"),
				content: `
					<div class="cd-onboard-card" style="text-align:center">
						<p style="font-size:1.1rem">${__("You can always access help from anywhere in Candela:")}</p>
						<div class="cd-onboard-grid" style="max-width:500px;margin:20px auto">
							${oCard("❓", __("Form Help"), __("Click the ❓ button on any form's toolbar to see context-specific guidance"))}
							${oCard("📚", __("Onboarding"), __("Visit /candela-onboarding anytime to review this guide"))}
							${oCard("🕯️", __("About Page"), __("Visit /candela-about for the full app showcase with diagrams"))}
						</div>
						<a class="btn btn-primary btn-lg" href="/app/candela" style="background:${AMBER};border-color:${AMBER};color:${DARK};font-weight:700;margin-top:24px">
							${__("Start Using Candela")} →
						</a>
					</div>`
			}
		];
	}

	/* ── Role-Specific Slides ──────────────────────────── */
	function getRoleSlides(role) {
		const roleMap = {
			"Candela Manager": [
				{ title: __("📊 Manager Dashboard"), content: mkP(__("As a manager, your home is the Admin Dashboard at /deladmin. Here you see today's reservations, order count, revenue, and alerts.")) },
				{ title: __("👥 Staff Management"), content: mkP(__("Manage shifts at /deladmin/staff. Assign roles, set schedules, and track attendance.")) },
				{ title: __("💰 Daily Closing"), content: mkP(__("At end of day, visit /deladmin/closing to reconcile POS totals, record expenses, and generate the daily report.")) },
				{ title: __("📦 Procurement Approvals"), content: mkP(__("Review and approve purchase requests from the kitchen. Monitor supplier performance and costs.")) }
			],
			"Candela Chef": [
				{ title: __("👨‍🍳 Kitchen Display"), content: mkP(__("Your workspace is /deladmin/kitchen. Orders appear in real-time organized by station.")) },
				{ title: __("📝 Production Logging"), content: mkP(__("Log what you produce at /deladmin/production. Record waste and ingredient usage.")) },
				{ title: __("📦 Stock Alerts"), content: mkP(__("When ingredients run low, create a purchase request directly from the kitchen.")) }
			],
			"Candela Waiter": [
				{ title: __("🍽️ Table Map"), content: mkP(__("See all tables at /deladmin/tables. Green = available, amber = occupied, red = reserved.")) },
				{ title: __("💰 POS Terminal"), content: mkP(__("Create orders at /deladmin/pos. Select items, apply promos, and send to kitchen.")) },
				{ title: __("📅 Reservations"), content: mkP(__("Check today's reservations. Greet customers by name and seat them at their reserved table.")) }
			],
			"Candela Cashier": [
				{ title: __("💰 POS Shift"), content: mkP(__("Open your shift at /deladmin/pos with a starting cash amount. Close it at end of shift.")) },
				{ title: __("🧾 Daily Expenses"), content: mkP(__("Record petty cash expenses during your shift for accurate daily closing.")) }
			],
			"Candela Procurement": [
				{ title: __("📋 Purchase Flow"), content: mkP(__("Purchase Request → Purchase Order → Goods Receipt Note → Stock Entry. All linked automatically.")) },
				{ title: __("🏭 Suppliers"), content: mkP(__("Manage suppliers in the Candela Supplier doctype. Track pricing and delivery reliability.")) },
				{ title: __("📦 Warehouses"), content: mkP(__("Manage storage locations at /deladmin/warehouses. Transfer stock between them as needed.")) }
			],
			"Candela Marketing": [
				{ title: __("📢 Campaigns"), content: mkP(__("Create marketing campaigns with activities, budgets, and ROI tracking.")) },
				{ title: __("🎫 Promo Codes"), content: mkP(__("Generate promo codes with discount %, max uses, and expiry dates.")) },
				{ title: __("⭐ Reviews"), content: mkP(__("Monitor customer reviews. Respond to feedback and track satisfaction trends.")) }
			]
		};
		return roleMap[role] || [{ title: __("ℹ️ No specific guide"), content: mkP(__("Contact your administrator for role-specific training.")) }];
	}

	/* ── Help Slides per Topic ─────────────────────────── */
	function getHelpSlides(topic) {
		const helpMap = {
			"Candela Settings": [
				{ title: __("⚙️ Candela Settings"), content: mkP(__("This is where you configure your restaurant's basic information: name, address, phone, opening hours, currency, and brand colors. Changes here affect the public website and all internal screens.")) },
				{ title: __("🕐 Opening Hours"), content: mkP(__("Set opening and closing times for each day. These are displayed on the website and used to validate reservation time slots.")) }
			],
			"Menu Item": [
				{ title: __("🍽️ Menu Items"), content: mkP(__("Each menu item belongs to a category and can have: price, description, dietary tags (vegan, gluten-free, etc.), ingredients with quantities, preparation time, and a photo.")) },
				{ title: __("📊 Pricing"), content: mkP(__("Price changes are logged automatically. You can view the price history in the Price Change Log doctype.")) }
			],
			"Table Reservation": [
				{ title: __("📅 Reservations"), content: mkP(__("Reservations come from the website or can be created manually. Each reservation has: guest name, date/time, party size, table assignment, and special notes.")) },
				{ title: __("🔄 Status Flow"), content: mkP(__("Pending → Confirmed → Seated → Completed. No-shows are marked automatically after 30 minutes.")) }
			],
			"Online Order": [
				{ title: __("📱 Online Orders"), content: mkP(__("Orders from the customer website arrive here. Each has items, delivery address, payment status, and real-time tracking status.")) },
				{ title: __("⚡ Kitchen Integration"), content: mkP(__("When confirmed, orders are sent to the kitchen display. Ingredients are deducted from stock automatically.")) }
			],
			"POS Invoice": [
				{ title: __("💰 POS Invoices"), content: mkP(__("POS invoices are created from the POS terminal. They link to a POS Shift and deduct stock automatically on creation.")) }
			],
			"Stock Entry": [
				{ title: __("📦 Stock Entries"), content: mkP(__("Stock entries track all inventory movements: receipts from suppliers, production consumption, transfers between warehouses, and adjustments.")) }
			],
			"Kitchen Station": [
				{ title: __("👨‍🍳 Kitchen Stations"), content: mkP(__("Stations organize your kitchen (e.g., Grill, Pasta, Dessert). Orders are routed to the correct station based on item configuration.")) }
			],
			"Daily Closing": [
				{ title: __("📊 Daily Closing"), content: mkP(__("The daily closing report summarizes: total POS sales, online order revenue, cash collected, expenses, and discrepancies. Auto-generated or created manually.")) }
			]
		};
		return helpMap[topic] || [];
	}

	/* ── Render Helpers ────────────────────────────────── */
	function mkP(text) {
		return `<div class="cd-onboard-card"><p>${text}</p></div>`;
	}

	function oCard(icon, title, desc) {
		return `<div class="cd-o-card"><span class="cd-o-icon">${icon}</span><strong>${title}</strong><small>${desc}</small></div>`;
	}

	function renderInFloatingWindow(title, slides) {
		if (frappe.visual && frappe.visual.floatingWindow) {
			const fw = frappe.visual.floatingWindow({
				title: title,
				position: document.dir === "rtl" ? "left" : "right",
				width: 520,
				minimizable: true,
				maximizable: true,
				onRender(container) {
					renderStoryboard(container, slides);
				}
			});
			fw.show();
		} else {
			// Fallback: frappe dialog
			const d = new frappe.ui.Dialog({
				title: title,
				size: "extra-large"
			});
			renderStoryboard(d.body, slides);
			d.show();
		}
	}

	function renderInContainer(selector, slides) {
		const el = typeof selector === "string" ? document.querySelector(selector) : selector;
		if (!el) return;
		renderStoryboard(el, slides);
	}

	function renderStoryboard(container, slides) {
		injectCSS();
		if (frappe.visual && frappe.visual.storyboard) {
			frappe.visual.storyboard({
				container: container,
				slides: slides,
				theme: "dark",
				nav_position: "both",
				show_progress: true,
				brand_color: AMBER
			});
		} else {
			// Fallback manual renderer
			let idx = 0;
			function draw() {
				const s = slides[idx];
				container.innerHTML = `
					<div class="cd-sb-wrap">
						<div class="cd-sb-nav">${navBtn("prev", idx > 0)}<span>${idx + 1}/${slides.length}</span>${navBtn("next", idx < slides.length - 1)}</div>
						<h3 style="color:${AMBER};text-align:center;margin:12px 0">${s.title}</h3>
						<div>${s.content}</div>
						<div class="cd-sb-nav">${navBtn("prev", idx > 0)}<span>${idx + 1}/${slides.length}</span>${navBtn("next", idx < slides.length - 1)}</div>
					</div>`;
				container.querySelectorAll(".cd-sb-prev").forEach(b => b.onclick = () => { if (idx > 0) { idx--; draw(); } });
				container.querySelectorAll(".cd-sb-next").forEach(b => b.onclick = () => { if (idx < slides.length - 1) { idx++; draw(); } });
				if (s.onMount) setTimeout(() => s.onMount(container), 100);
			}
			draw();
		}
	}

	function navBtn(dir, enabled) {
		const cls = dir === "prev" ? "cd-sb-prev" : "cd-sb-next";
		const label = dir === "prev" ? __("← Previous") : __("Next →");
		const style = dir === "next" ? `background:${AMBER};color:${DARK};border-color:${AMBER}` : "";
		return `<button class="btn btn-sm ${dir === 'next' ? 'btn-primary' : 'btn-default'} ${cls}" style="${style}" ${enabled ? "" : "disabled"}>${label}</button>`;
	}

	/* ── Form Toolbar Help Button ──────────────────────── */
	if (typeof frappe !== "undefined" && frappe.ui && frappe.ui.form) {
		$(document).on("form-refresh", function (e, frm) {
			if (!frm || !frm.doctype) return;
			// Remove old help button
			frm.page.remove_inner_button(__("❓ Help"));
			// Add help button if we have help for this doctype
			const topics = ["Candela Settings", "Menu Item", "Menu Category", "Table Reservation",
				"Online Order", "POS Invoice", "POS Shift", "Stock Entry", "Kitchen Station",
				"Daily Closing", "Ingredient", "Restaurant Table", "Delivery Zone",
				"Promo Code", "Marketing Campaign", "Customer Review", "Staff Shift",
				"Purchase Request", "Purchase Order", "Goods Receipt Note", "Stock Reconciliation",
				"Restaurant Asset", "Maintenance Request", "Candela Supplier", "Candela Warehouse"];
			if (topics.includes(frm.doctype)) {
				frm.page.add_inner_button(__("❓ Help"), function () {
					window.candela.help.open(frm.doctype);
				});
			}
		});
	}

	/* ── CSS ───────────────────────────────────────────── */
	function injectCSS() {
		if (document.getElementById("cd-onboard-css")) return;
		const s = document.createElement("style");
		s.id = "cd-onboard-css";
		s.textContent = `
		.cd-onboard-card{background:rgba(28,25,23,.7);backdrop-filter:blur(16px);border:1px solid rgba(245,158,11,.15);border-radius:14px;padding:24px;margin:12px 0;color:#FEF3C7}
		.cd-onboard-card p{color:#D6D3D1;line-height:1.7;margin:0}
		.cd-onboard-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-top:16px}
		.cd-o-card{background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:10px;padding:14px;display:flex;flex-direction:column;gap:4px}
		.cd-o-icon{font-size:1.4rem}
		.cd-o-card strong{color:#FBBF24;font-size:.9rem}
		.cd-o-card small{color:#A8A29E;font-size:.82rem;line-height:1.4}
		.cd-flow-steps{color:#D6D3D1;font-size:.9rem;line-height:2;margin-top:16px}
		.cd-sb-wrap{padding:8px}
		.cd-sb-nav{display:flex;justify-content:space-between;align-items:center;padding:8px 0;color:#A8A29E;font-size:.85rem}
		`;
		document.head.appendChild(s);
	}
})();
