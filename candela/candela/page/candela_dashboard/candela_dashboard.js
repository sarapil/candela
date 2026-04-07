frappe.pages["candela-dashboard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Candela Dashboard"),
		single_column: true,
	});
	frappe.breadcrumbs.add("Candela");
	wrapper.dashboard = new CandelaDashboard(page);
};

frappe.pages["candela-dashboard"].on_page_show = function (wrapper) {
	if (wrapper.dashboard) wrapper.dashboard.refresh();
};

class CandelaDashboard {
	constructor(page) {
		this.page = page;
		this.data = {};
		this.current_branch = null;

		this.setup_actions();
		this.render_layout();
		this.refresh();
	}

	setup_actions() {
		this.page.add_field({
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "CD Branch",
			change: () => {
				this.current_branch = this.page.fields_dict.branch.get_value() || null;
				this.refresh();
			},
		});

		this.page.set_primary_action(__("Refresh"), () => this.refresh(), "refresh");
		this.page.add_inner_button(__("Table Map"), () => frappe.set_route("candela-table-map"));
		this.page.add_inner_button(__("New Order"), () => frappe.new_doc("CD Order"));
	}

	render_layout() {
		this.page.main.html(`
			<div class="candela-dashboard" style="padding:16px;">
				<div class="cd-scene-header" style="height:180px;border-radius:12px;margin-bottom:16px;overflow:hidden;"></div>
				<div class="cd-kpi-row" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:20px;"></div>
				<div style="display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:20px;">
					<div class="cd-active-orders fv-fx-glass" style="border-radius:12px;padding:16px;">
						<h5 style="margin-bottom:12px;">${__("Active Orders")}</h5>
						<div class="cd-orders-list"></div>
					</div>
					<div class="cd-table-overview fv-fx-glass" style="border-radius:12px;padding:16px;">
						<h5 style="margin-bottom:12px;">${__("Table Status")}</h5>
						<div class="cd-table-summary"></div>
					</div>
				</div>
				<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
					<div class="cd-today-reservations fv-fx-glass" style="border-radius:12px;padding:16px;">
						<h5 style="margin-bottom:12px;">${__("Today's Reservations")}</h5>
						<div class="cd-reservations-list"></div>
					</div>
					<div class="cd-top-items fv-fx-glass" style="border-radius:12px;padding:16px;">
						<h5 style="margin-bottom:12px;">${__("Popular Items Today")}</h5>
						<div class="cd-items-list"></div>
					</div>
				</div>
			</div>
		`);
	}

	async refresh() {
		const branch = this.current_branch;
		await Promise.all([
			this.load_kpis(branch),
			this.load_active_orders(branch),
			this.load_table_status(branch),
			this.load_reservations(branch),
		]);
		this.init_scene_header();
	}

	async load_kpis(branch) {
		try {
			const filters = branch ? { branch } : {};

			const [total_orders, open_orders, total_tables, rev] = await Promise.all([
				frappe.xcall("frappe.client.get_count", {
					doctype: "CD Order",
					filters: Object.assign({ creation: [">=", frappe.datetime.get_today()] }, filters),
				}),
				frappe.xcall("frappe.client.get_count", {
					doctype: "CD Order",
					filters: Object.assign({ status: ["in", ["Open", "Preparing"]] }, filters),
				}),
				frappe.xcall("frappe.client.get_count", {
					doctype: "CD Table", filters,
				}),
				frappe.xcall("frappe.client.get_list", {
					doctype: "CD Order",
					filters: Object.assign({ creation: [">=", frappe.datetime.get_today()], docstatus: 1 }, filters),
					fields: ["sum(grand_total) as total"],
					limit_page_length: 1,
				}),
			]);

			const revenue = rev?.[0]?.total || 0;
			this.data.kpis = { total_orders, open_orders, total_tables, revenue };
			this.render_kpis();
		} catch {
			// KPIs optional
		}
	}

	render_kpis() {
		const k = this.data.kpis || {};
		const metrics = [
			{ label: __("Orders Today"), value: k.total_orders || 0, color: "var(--amber-500)", icon: "📋" },
			{ label: __("Active Orders"), value: k.open_orders || 0, color: "var(--red-500)", icon: "🔥" },
			{ label: __("Total Tables"), value: k.total_tables || 0, color: "var(--blue-500)", icon: "🍽️" },
			{ label: __("Revenue Today"), value: frappe.format(k.revenue || 0, { fieldtype: "Currency" }), color: "var(--green-500)", icon: "💰" },
		];

		this.page.main.find(".cd-kpi-row").html(metrics.map((m) => `
			<div class="fv-fx-glass fv-fx-hover-lift" style="padding:16px;border-radius:10px;text-align:center;">
				<div style="font-size:28px;margin-bottom:4px;">${m.icon}</div>
				<div style="font-size:24px;font-weight:700;color:${m.color};">${m.value}</div>
				<div style="font-size:12px;color:var(--text-muted);margin-top:4px;">${m.label}</div>
			</div>
		`).join(""));
	}

	async load_active_orders(branch) {
		try {
			const filters = { status: ["in", ["Open", "Preparing", "Served"]] };
			if (branch) filters.branch = branch;

			const orders = await frappe.xcall("frappe.client.get_list", {
				doctype: "CD Order",
				filters,
				fields: ["name", "table", "waiter_name", "grand_total", "status", "creation"],
				order_by: "creation desc",
				limit_page_length: 12,
			});

			const list = this.page.main.find(".cd-orders-list");
			if (!orders.length) {
				list.html(`<p class="text-muted">${__("No active orders")}</p>`);
				return;
			}

			list.html(orders.map((o) => {
				const sc = { Open: "orange", Preparing: "blue", Served: "green" };
				return `
					<div class="fv-fx-hover-lift" style="padding:8px;border-radius:6px;margin-bottom:6px;cursor:pointer;
						border:1px solid var(--border-color);display:flex;justify-content:space-between;align-items:center;"
						data-name="${frappe.utils.escape_html(o.name)}">
						<div>
							<strong>${frappe.utils.escape_html(o.name)}</strong>
							<div style="font-size:11px;color:var(--text-muted);">
								${frappe.utils.escape_html(o.waiter_name || "")} · ${frappe.utils.escape_html(o.table || "")}
							</div>
						</div>
						<div style="text-align:end;">
							<span class="indicator-pill ${sc[o.status] || "gray"}" style="font-size:10px;">${__(o.status)}</span>
							<div style="font-size:12px;font-weight:600;margin-top:2px;">${frappe.format(o.grand_total, { fieldtype: "Currency" })}</div>
						</div>
					</div>
				`;
			}).join(""));

			list.find("[data-name]").on("click", function () {
				frappe.set_route("Form", "CD Order", $(this).data("name"));
			});
		} catch {
			// orders fetch optional
		}
	}

	async load_table_status(branch) {
		try {
			const filters = branch ? { branch } : {};
			const tables = await frappe.xcall("frappe.client.get_list", {
				doctype: "CD Table",
				filters,
				fields: ["status"],
				limit_page_length: 0,
			});

			const counts = {};
			tables.forEach((t) => { counts[t.status] = (counts[t.status] || 0) + 1; });

			const summary = this.page.main.find(".cd-table-summary");
			const statuses = [
				{ label: __("Available"), key: "Available", color: "green" },
				{ label: __("Occupied"), key: "Occupied", color: "red" },
				{ label: __("Reserved"), key: "Reserved", color: "blue" },
				{ label: __("Cleaning"), key: "Cleaning", color: "yellow" },
			];

			summary.html(statuses.map((s) => `
				<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;
					border-bottom:1px solid var(--border-color);">
					<span class="indicator-pill ${s.color}">${s.label}</span>
					<strong>${counts[s.key] || 0}</strong>
				</div>
			`).join(""));
		} catch {
			// table status optional
		}
	}

	async load_reservations(branch) {
		try {
			const filters = {
				reservation_date: frappe.datetime.get_today(),
				status: ["in", ["Confirmed", "Pending"]],
			};
			if (branch) filters.branch = branch;

			const reservations = await frappe.xcall("frappe.client.get_list", {
				doctype: "CD Reservation",
				filters,
				fields: ["name", "guest_name", "party_size", "reservation_time", "table", "status"],
				order_by: "reservation_time asc",
				limit_page_length: 10,
			});

			const list = this.page.main.find(".cd-reservations-list");
			if (!reservations.length) {
				list.html(`<p class="text-muted">${__("No reservations today")}</p>`);
				return;
			}

			list.html(reservations.map((r) => `
				<div style="padding:8px 0;border-bottom:1px solid var(--border-color);cursor:pointer;"
					 data-name="${frappe.utils.escape_html(r.name)}">
					<div style="font-weight:500;">${frappe.utils.escape_html(r.guest_name || r.name)}</div>
					<div style="font-size:11px;color:var(--text-muted);">
						${r.reservation_time || ""} · ${r.party_size} ${__("guests")}
						${r.table ? ` · ${__("Table")} ${frappe.utils.escape_html(r.table)}` : ""}
					</div>
				</div>
			`).join(""));

			list.find("[data-name]").on("click", function () {
				frappe.set_route("Form", "CD Reservation", $(this).data("name"));
			});
		} catch {
			// reservations optional
		}
	}

	async init_scene_header() {
		const el = this.page.main.find(".cd-scene-header")[0];
		if (!el || this._sceneLoaded) return;
		try {
			await frappe.require("frappe_visual.bundle.js");
			if (frappe.visual?.scenePresetCafe) {
				const k = this.data.kpis || {};
				await frappe.visual.scenePresetCafe({
					container: el,
					theme: "warm",
					frames: [
						{ label: __("Orders"), value: String(k.total_orders || 0), status: "info" },
						{ label: __("Active"), value: String(k.open_orders || 0), status: "warning" },
						{ label: __("Revenue"), value: frappe.format(k.revenue || 0, { fieldtype: "Currency" }), status: "success" },
					],
				});
				this._sceneLoaded = true;
			}
		} catch {
			el.style.display = "none";
		}
	}
}
