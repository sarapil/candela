// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// License: GPL-3.0

/**
 * Candela 3D Restaurant Layout
 * ==============================
 * Integrates frappe_visual's 3D framework with Candela restaurant management.
 * Provides interactive 3D floor plans with real-time table status,
 * reservation indicators, and kitchen area visualization.
 *
 * Reuses HospitalityOverlay from frappe_visual (shared with Velara).
 *
 * Usage:
 *   await frappe.candela.layout3D.create("#container", { branch: "BRANCH-001" });
 */

frappe.provide("frappe.candela.layout3D");

frappe.candela.layout3D = {
	_loaded: false,

	async load() {
		if (this._loaded) return;
		await frappe.visual.load3D();
		this._loaded = true;
	},

	/**
	 * Create a 3D restaurant floor plan with live table status.
	 * @param {string|Element} container — CSS selector or DOM element
	 * @param {Object} opts — { branch, floor, modelUrl }
	 */
	async create(container, opts = {}) {
		await this.load();

		const el = typeof container === "string" ? document.querySelector(container) : container;
		if (!el) return;

		const { ThreeEngine, HospitalityOverlay } = frappe.visual.three;

		const engine = new ThreeEngine(el, {
			background: opts.background || "#fdf8f0",
			shadows: true,
			antialias: true,
		});
		engine.init();

		// Use hospitality overlay with restaurant-specific status colors
		const overlay = new HospitalityOverlay(engine, {
			statusColors: {
				available: 0x22c55e,   // Green — free table
				occupied: 0xef4444,    // Red — guests seated
				reserved: 0xf59e0b,   // Amber — reservation
				cleaning: 0x6b7280,   // Gray — being cleaned
				preparing: 0x3b82f6,  // Blue — setting up
			},
		});

		// Load restaurant model if provided
		if (opts.modelUrl) {
			const { ModelLoader } = frappe.visual.three;
			const loader = new ModelLoader(engine);
			try {
				const model = await loader.load(opts.modelUrl);
				engine.scene.add(model);
			} catch (e) {
				console.error("Failed to load restaurant model:", e);
			}
		}

		// Load tables data from Candela
		if (opts.branch) {
			try {
				const filters = { branch: opts.branch };
				if (opts.floor) filters.floor = opts.floor;

				const tables = await frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "CD Table",
						filters,
						fields: ["name", "table_number", "section", "status",
							"capacity", "mesh_name", "current_order"],
						limit_page_length: 0,
					},
				});

				if (tables.message) {
					const units = tables.message.map(t => ({
						id: t.name,
						meshName: t.mesh_name || `table-${t.table_number}`,
						status: (t.status || "available").toLowerCase(),
						label: `${__("Table")} ${t.table_number} (${t.capacity} ${__("seats")})`,
						metadata: {
							section: t.section,
							capacity: t.capacity,
							order: t.current_order,
						},
					}));
					overlay.registerUnits(units);
				}
			} catch (e) {
				console.warn("Could not load CD Table data:", e);
			}
		}

		// Click handler — show table details or create order
		overlay.onUnitClick = (tableData) => {
			if (!tableData) return;

			if (tableData.status === "available") {
				frappe.confirm(
					__("Create order for Table {0}?", [tableData.label]),
					() => frappe.new_doc("CD Order", {
						table: tableData.id,
					}),
				);
			} else if (tableData.metadata?.order) {
				frappe.set_route("Form", "CD Order", tableData.metadata.order);
			} else {
				frappe.set_route("Form", "CD Table", tableData.id);
			}
		};

		return { engine, overlay };
	},

	/**
	 * Create a restaurant dashboard with 3D layout + table status.
	 */
	async createDashboard(container, opts = {}) {
		const el = typeof container === "string" ? document.querySelector(container) : container;
		if (!el) return;

		el.innerHTML = `
			<div class="cd-layout-dashboard fv-fx-page-enter" style="display:flex;gap:16px;height:450px;">
				<div class="cd-layout-viewer" style="flex:3;border-radius:12px;overflow:hidden;border:1px solid var(--border-color);"></div>
				<div class="cd-layout-stats fv-fx-glass" style="flex:1;padding:16px;border-radius:12px;overflow-y:auto;">
					<h4>${__("Table Status")}</h4>
					<div class="cd-stats-content"></div>
				</div>
			</div>
		`;

		const viewerEl = el.querySelector(".cd-layout-viewer");
		const statsEl = el.querySelector(".cd-stats-content");

		const result = await this.create(viewerEl, opts);
		if (!result) return;

		const summary = result.overlay.getOccupancySummary();
		const statusLabels = {
			available: { label: __("Available"), color: "#22c55e", icon: "✅" },
			occupied: { label: __("Occupied"), color: "#ef4444", icon: "🍽️" },
			reserved: { label: __("Reserved"), color: "#f59e0b", icon: "📋" },
			cleaning: { label: __("Cleaning"), color: "#6b7280", icon: "🧹" },
			preparing: { label: __("Preparing"), color: "#3b82f6", icon: "🔧" },
		};

		let statsHTML = `
			<div style="margin-bottom:12px;">
				<div class="text-muted">${__("Total Tables")}</div>
				<div style="font-size:2em;font-weight:bold;color:var(--primary);">${summary.total}</div>
			</div>
			<div style="margin-bottom:12px;">
				<div class="text-muted">${__("Occupancy")}</div>
				<div style="font-size:1.5em;font-weight:bold;">${summary.occupancyRate}%</div>
			</div>
			<hr>
		`;

		for (const [status, info] of Object.entries(statusLabels)) {
			const count = summary.byStatus?.[status] || 0;
			statsHTML += `
				<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
					<span style="display:flex;align-items:center;gap:6px;">
						<span style="width:10px;height:10px;border-radius:50%;background:${info.color};display:inline-block;"></span>
						${info.label}
					</span>
					<strong>${count}</strong>
				</div>
			`;
		}

		statsEl.innerHTML = statsHTML;
		return result;
	},
};
