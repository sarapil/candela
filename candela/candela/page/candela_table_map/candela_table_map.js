frappe.pages["candela-table-map"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Table Map"),
		single_column: true,
	});
	wrapper.table_map = new CandelaTableMap(page);
};

frappe.pages["candela-table-map"].on_page_show = function (wrapper) {
	if (wrapper.table_map) {
		const branch = frappe.get_route()[1];
		if (branch) wrapper.table_map.load_branch(branch);
		wrapper.table_map.resume();
	}
};

frappe.pages["candela-table-map"].on_page_hide = function (wrapper) {
	if (wrapper.table_map) wrapper.table_map.pause();
};

class CandelaTableMap {
	constructor(page) {
		this.page = page;
		this.current_branch = null;
		this.engine = null;
		this.auto_refresh = null;
		this.status_filters = new Set(["Available", "Occupied", "Reserved", "Cleaning"]);
		this.setup_controls();
		this.render_layout();
	}

	setup_controls() {
		this.page.add_field({
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "CD Branch",
			change: () => {
				const val = this.page.fields_dict.branch.get_value();
				if (val) this.load_branch(val);
			},
		});

		this.page.add_field({
			fieldname: "section",
			label: __("Section"),
			fieldtype: "Select",
			options: [__("All Sections")],
			change: () => this.filter_section(),
		});

		this.page.add_inner_button(__("New Order"), () => this.quick_new_order(), __("Actions"));
		this.page.add_inner_button(__("Screenshot"), () => this.screenshot(), __("Export"));
		this.page.add_inner_button(__("Fullscreen"), () => this.toggle_fullscreen());

		this.page.add_action_item(__("Toggle Live Mode"), () => this.toggle_auto_refresh());

		// XR integration — VR restaurant walkthrough + AR table layout
		frappe.base_base?.xr_mixin?.attach(this, {
			get_engine: () => this.engine,
			get_spatial_data: () => this.getXRPanels(),
			vr_options: { startPosition: [0, 1.7, 5] },
			ar_options: { scale: 0.1, shadowPlane: true },
		});
	}

	getXRPanels() {
		if (!this.current_branch) return [];
		const total = this.page.main.find(".stat-total").text();
		const occ = this.page.main.find(".stat-occupied").text();
		return [
			{ content: `<h3>${this.current_branch}</h3><p>${__("Tables")}: ${total} | ${__("Occupied")}: ${occ}</p>`, position: [0, 2.2, -3], billboard: true },
		];
	}

	render_layout() {
		const container = this.page.main.find("#candela-table-map-container");
		container.html(`
			<div class="candela-map-wrapper" style="display:flex; gap:12px; min-height:calc(100vh - 160px);">
				<div class="map-main" style="flex:1; display:flex; flex-direction:column; gap:12px;">
					<div class="table-stats" style="display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:8px;">
						<div class="stat-card fv-fx-glass fv-fx-hover-lift" style="padding:12px; border-radius:8px; text-align:center;">
							<div style="font-size:11px; color:var(--text-muted);">${__("Total Tables")}</div>
							<div class="stat-total" style="font-size:22px; font-weight:700;">0</div>
						</div>
						<div class="stat-card fv-fx-glass fv-fx-hover-lift" style="padding:12px; border-radius:8px; text-align:center;">
							<div style="font-size:11px; color:var(--text-muted);">${__("Available")}</div>
							<div class="stat-available" style="font-size:22px; font-weight:700; color:var(--green-500);">0</div>
						</div>
						<div class="stat-card fv-fx-glass fv-fx-hover-lift" style="padding:12px; border-radius:8px; text-align:center;">
							<div style="font-size:11px; color:var(--text-muted);">${__("Occupied")}</div>
							<div class="stat-occupied" style="font-size:22px; font-weight:700; color:var(--red-500);">0</div>
						</div>
						<div class="stat-card fv-fx-glass fv-fx-hover-lift" style="padding:12px; border-radius:8px; text-align:center;">
							<div style="font-size:11px; color:var(--text-muted);">${__("Reserved")}</div>
							<div class="stat-reserved" style="font-size:22px; font-weight:700; color:var(--blue-500);">0</div>
						</div>
						<div class="stat-card fv-fx-glass fv-fx-hover-lift" style="padding:12px; border-radius:8px; text-align:center;">
							<div style="font-size:11px; color:var(--text-muted);">${__("Covers")}</div>
							<div class="stat-covers" style="font-size:22px; font-weight:700; color:var(--orange-500);">0</div>
						</div>
					</div>
					<div class="viewport-3d fv-fx-glass" style="flex:1; min-height:500px; border-radius:8px; position:relative; overflow:hidden;">
						<div class="viewport-placeholder" style="display:flex; align-items:center; justify-content:center; height:100%; color:var(--text-muted);">
							<div style="text-align:center;">
								<div style="font-size:48px; margin-bottom:12px;">🍽️</div>
								<div>${__("Select a branch to view table map")}</div>
							</div>
						</div>
					</div>
					<div class="table-legend" style="display:flex; gap:16px; flex-wrap:wrap; padding:8px;">
						<span style="display:flex; align-items:center; gap:4px;">
							<span style="width:12px; height:12px; border-radius:50%; background:var(--green-500);"></span>
							${__("Available")}
						</span>
						<span style="display:flex; align-items:center; gap:4px;">
							<span style="width:12px; height:12px; border-radius:50%; background:var(--red-500);"></span>
							${__("Occupied")}
						</span>
						<span style="display:flex; align-items:center; gap:4px;">
							<span style="width:12px; height:12px; border-radius:50%; background:var(--blue-500);"></span>
							${__("Reserved")}
						</span>
						<span style="display:flex; align-items:center; gap:4px;">
							<span style="width:12px; height:12px; border-radius:50%; background:var(--yellow-500);"></span>
							${__("Cleaning")}
						</span>
						<span style="display:flex; align-items:center; gap:4px;">
							<span style="width:12px; height:12px; border-radius:2px; background:var(--amber-500);"></span>
							${__("Outdoor")}
						</span>
					</div>
				</div>
				<div class="map-sidebar fv-fx-glass" style="width:280px; border-radius:8px; padding:16px; overflow-y:auto; max-height:calc(100vh - 160px);">
					<h6 style="margin-bottom:12px;">${__("Status Filter")}</h6>
					<div class="status-filters" style="display:flex; flex-direction:column; gap:6px; margin-bottom:16px;">
						<label style="display:flex; align-items:center; gap:6px; cursor:pointer;">
							<input type="checkbox" data-status="Available" checked> ${__("Available")}
						</label>
						<label style="display:flex; align-items:center; gap:6px; cursor:pointer;">
							<input type="checkbox" data-status="Occupied" checked> ${__("Occupied")}
						</label>
						<label style="display:flex; align-items:center; gap:6px; cursor:pointer;">
							<input type="checkbox" data-status="Reserved" checked> ${__("Reserved")}
						</label>
						<label style="display:flex; align-items:center; gap:6px; cursor:pointer;">
							<input type="checkbox" data-status="Cleaning" checked> ${__("Cleaning")}
						</label>
					</div>
					<hr>
					<h6 style="margin:12px 0;">${__("Table Detail")}</h6>
					<div class="table-detail" style="color:var(--text-muted); font-size:12px;">
						${__("Click a table on the map")}
					</div>
					<hr>
					<h6 style="margin:12px 0;">${__("Active Orders")}</h6>
					<div class="active-orders" style="font-size:12px; color:var(--text-muted);">
						${__("No active orders")}
					</div>
					<hr>
					<h6 style="margin:12px 0;">${__("Reservations Today")}</h6>
					<div class="today-reservations" style="font-size:12px; color:var(--text-muted);">
						${__("No reservations")}
					</div>
				</div>
			</div>
		`);

		container.find(".status-filters input").on("change", () => {
			this.status_filters.clear();
			container.find(".status-filters input:checked").each(function () {
				this.status_filters?.add($(this).data("status"));
			}.bind(this));
			this.apply_status_filter();
		});
	}

	async load_branch(branch_name) {
		this.current_branch = branch_name;
		frappe.dom.freeze(__("Loading table map..."));

		try {
			const tables = await frappe.xcall(
				"frappe.client.get_list",
				{
					doctype: "CD Table",
					filters: { branch: branch_name },
					fields: ["name", "table_name", "table_number", "section", "status",
						"capacity", "is_outdoor", "x_pos", "y_pos", "shape",
						"current_order", "current_waiter"],
					limit_page_length: 0,
				}
			);

			this.update_stats(tables);
			this.update_sections(tables);
			await this.render_3d_map(tables);
			this.load_active_orders(branch_name);
			this.load_today_reservations(branch_name);
		} catch (e) {
			frappe.msgprint({ title: __("Error"), indicator: "red", message: e.message || __("Failed to load branch") });
		} finally {
			frappe.dom.unfreeze();
		}
	}

	update_stats(tables) {
		const c = this.page.main.find("#candela-table-map-container");
		c.find(".stat-total").text(tables.length);
		c.find(".stat-available").text(tables.filter((t) => t.status === "Available").length);
		c.find(".stat-occupied").text(tables.filter((t) => t.status === "Occupied").length);
		c.find(".stat-reserved").text(tables.filter((t) => t.status === "Reserved").length);
		c.find(".stat-covers").text(tables.reduce((s, t) => s + (t.status === "Occupied" ? (t.capacity || 0) : 0), 0));
	}

	update_sections(tables) {
		const sections = [...new Set(tables.map((t) => t.section).filter(Boolean))].sort();
		const field = this.page.fields_dict.section;
		field.df.options = [__("All Sections"), ...sections];
		field.refresh();
	}

	async render_3d_map(tables) {
		const viewport = this.page.main.find(".viewport-3d");
		viewport.find(".viewport-placeholder").remove();

		try {
			await frappe.require("fv_3d.bundle.js");

			if (!this.engine) {
				this.engine = await frappe.visual.three.engine({
					container: viewport[0],
					background: 0xfaf5eb,
					controls: "orbit",
					grid: true,
					ambient_light: 0.7,
				});
			}

			this.engine.clearScene();

			const overlay = await frappe.visual.three.hospitalityOverlay({
				engine: this.engine,
			});

			const status_map = {};
			tables.forEach((t) => { status_map[t.name] = t.status; });
			overlay.setTableStatuses(status_map);

			tables.forEach((table) => {
				const x = (table.x_pos || Math.random() * 16 - 8);
				const z = (table.y_pos || Math.random() * 16 - 8);
				const shape = (table.shape || "square").toLowerCase();
				const size = this.get_table_size(table.capacity || 4);

				if (shape === "round" || shape === "circle") {
					this.engine.addCylinder({
						id: table.name,
						position: [x, 0.4, z],
						radius: size / 2,
						height: 0.8,
						color: this.get_table_color(table),
						metadata: table,
					});
				} else {
					this.engine.addBox({
						id: table.name,
						position: [x, 0.4, z],
						size: [size, 0.8, size * 0.7],
						color: this.get_table_color(table),
						metadata: table,
					});
				}
			});

			this.engine.onSelect((obj) => {
				if (obj && obj.userData) this.show_table_detail(obj.userData);
			});

			this.engine.fitAll();
		} catch (e) {
			viewport.html(`<div style="padding:40px; text-align:center; color:var(--text-muted);">
				<p>${__("3D engine not available. Install frappe_visual for full 3D support.")}</p>
				<p style="font-size:12px;">${e.message || ""}</p>
			</div>`);
		}
	}

	get_table_size(capacity) {
		if (capacity <= 2) return 0.8;
		if (capacity <= 4) return 1.2;
		if (capacity <= 6) return 1.6;
		return 2.0;
	}

	get_table_color(table) {
		const colors = {
			Available: 0x22c55e,
			Occupied: 0xef4444,
			Reserved: 0x3b82f6,
			Cleaning: 0xeab308,
		};
		return colors[table.status] || 0x94a3b8;
	}

	show_table_detail(table) {
		const detail = this.page.main.find(".table-detail");
		const status_color = { Available: "green", Occupied: "red", Reserved: "blue", Cleaning: "yellow" };

		detail.html(`
			<div style="display:flex; flex-direction:column; gap:8px;">
				<div style="font-weight:600; font-size:14px;">
					${__("Table")} ${frappe.utils.escape_html(table.table_number || table.table_name || table.name)}
				</div>
				<div><span class="indicator-pill ${status_color[table.status] || "gray"}">${__(table.status)}</span></div>
				<div><strong>${__("Section")}:</strong> ${__(table.section || "-")}</div>
				<div><strong>${__("Capacity")}:</strong> ${table.capacity || "-"} ${__("seats")}</div>
				${table.is_outdoor ? `<div><span class="indicator-pill orange">${__("Outdoor")}</span></div>` : ""}
				${table.current_waiter ? `<div><strong>${__("Waiter")}:</strong> ${frappe.utils.escape_html(table.current_waiter)}</div>` : ""}
				${table.current_order ? `<div><strong>${__("Order")}:</strong> <a href="/app/cd-order/${encodeURIComponent(table.current_order)}">${frappe.utils.escape_html(table.current_order)}</a></div>` : ""}
				<div style="margin-top:8px; display:flex; gap:6px; flex-wrap:wrap;">
					${table.status === "Available" ? `<button class="btn btn-primary btn-xs btn-new-order">${__("New Order")}</button>` : ""}
					${table.status === "Occupied" && table.current_order ? `<button class="btn btn-warning btn-xs btn-bill">${__("Print Bill")}</button>` : ""}
					${table.status === "Occupied" ? `<button class="btn btn-success btn-xs btn-free">${__("Free Table")}</button>` : ""}
					<button class="btn btn-default btn-xs btn-open">${__("Open")}</button>
				</div>
			</div>
		`);

		detail.find(".btn-new-order").on("click", () => {
			frappe.new_doc("CD Order", { table: table.name, branch: this.current_branch });
		});
		detail.find(".btn-bill").on("click", () => {
			if (table.current_order) {
				frappe.set_route("print", "CD Order", table.current_order);
			}
		});
		detail.find(".btn-free").on("click", () => {
			frappe.xcall("frappe.client.set_value", {
				doctype: "CD Table", name: table.name,
				fieldname: "status", value: "Cleaning",
			}).then(() => {
				frappe.show_alert({ message: __("Table freed"), indicator: "green" });
				this.load_branch(this.current_branch);
			});
		});
		detail.find(".btn-open").on("click", () => {
			frappe.set_route("Form", "CD Table", table.name);
		});
	}

	async load_active_orders(branch_name) {
		try {
			const orders = await frappe.xcall(
				"frappe.client.get_list",
				{
					doctype: "CD Order",
					filters: { branch: branch_name, status: ["in", ["Open", "Preparing", "Served"]] },
					fields: ["name", "table", "waiter_name", "grand_total", "status", "creation"],
					order_by: "creation desc",
					limit_page_length: 15,
				}
			);

			const el = this.page.main.find(".active-orders");
			if (!orders.length) {
				el.html(`<span style="color:var(--text-muted);">${__("No active orders")}</span>`);
				return;
			}
			el.html(orders.map((o) => `
				<div style="padding:6px 0; border-bottom:1px solid var(--border-color); cursor:pointer;"
					 data-name="${frappe.utils.escape_html(o.name)}">
					<div style="display:flex; justify-content:space-between;">
						<span style="font-weight:500;">${frappe.utils.escape_html(o.name)}</span>
						<span class="indicator-pill ${o.status === "Open" ? "orange" : o.status === "Preparing" ? "blue" : "green"}"
							  style="font-size:10px;">${__(o.status)}</span>
					</div>
					<div style="font-size:11px; color:var(--text-muted);">
						${frappe.utils.escape_html(o.waiter_name || "")} · ${frappe.format(o.grand_total, { fieldtype: "Currency" })}
					</div>
				</div>
			`).join(""));

			el.find("[data-name]").on("click", function () {
				frappe.set_route("Form", "CD Order", $(this).data("name"));
			});
		} catch {
			// active orders fetch optional
		}
	}

	async load_today_reservations(branch_name) {
		try {
			const reservations = await frappe.xcall(
				"frappe.client.get_list",
				{
					doctype: "CD Reservation",
					filters: {
						branch: branch_name,
						reservation_date: frappe.datetime.get_today(),
						status: ["in", ["Confirmed", "Pending"]],
					},
					fields: ["name", "guest_name", "party_size", "reservation_time", "table", "status"],
					order_by: "reservation_time asc",
					limit_page_length: 10,
				}
			);

			const el = this.page.main.find(".today-reservations");
			if (!reservations.length) {
				el.html(`<span style="color:var(--text-muted);">${__("No reservations today")}</span>`);
				return;
			}
			el.html(reservations.map((r) => `
				<div style="padding:6px 0; border-bottom:1px solid var(--border-color); cursor:pointer;"
					 data-name="${frappe.utils.escape_html(r.name)}">
					<div style="font-weight:500;">${frappe.utils.escape_html(r.guest_name || r.name)}</div>
					<div style="font-size:11px; color:var(--text-muted);">
						${r.reservation_time || ""} · ${r.party_size} ${__("guests")}
						${r.table ? ` · ${__("Table")} ${frappe.utils.escape_html(r.table)}` : ""}
					</div>
				</div>
			`).join(""));

			el.find("[data-name]").on("click", function () {
				frappe.set_route("Form", "CD Reservation", $(this).data("name"));
			});
		} catch {
			// reservations fetch optional
		}
	}

	filter_section() {
		if (!this.engine) return;
		const section = this.page.fields_dict.section.get_value();
		if (section === __("All Sections")) {
			this.engine.showAll();
		} else {
			this.engine.filterByMetadata("section", section);
		}
	}

	apply_status_filter() {
		if (!this.engine) return;
		this.engine.filterByMetadata("status", [...this.status_filters], "include");
	}

	quick_new_order() {
		frappe.new_doc("CD Order", { branch: this.current_branch });
	}

	toggle_auto_refresh() {
		if (this.auto_refresh) {
			clearInterval(this.auto_refresh);
			this.auto_refresh = null;
			frappe.show_alert({ message: __("Live mode OFF"), indicator: "gray" });
		} else {
			this.auto_refresh = setInterval(() => {
				if (this.current_branch) this.load_branch(this.current_branch);
			}, 15000);
			frappe.show_alert({ message: __("Live mode ON (15s)"), indicator: "green" });
		}
	}

	screenshot() {
		if (this.engine) this.engine.screenshot(`candela_${this.current_branch || "tables"}.png`);
	}

	toggle_fullscreen() {
		const el = this.page.main.find(".viewport-3d")[0];
		if (!document.fullscreenElement) {
			el.requestFullscreen?.();
		} else {
			document.exitFullscreen?.();
		}
	}

	resume() {
		if (this.engine) this.engine.resume?.();
	}

	pause() {
		if (this.auto_refresh) {
			clearInterval(this.auto_refresh);
			this.auto_refresh = null;
		}
		if (this.engine) this.engine.pause?.();
	}
}
