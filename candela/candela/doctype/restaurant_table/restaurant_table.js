// Copyright (c) 2026, Arkan Lab — License: MIT
frappe.ui.form.on("Restaurant Table", {
	refresh(frm) {
		const colors = {
			Available: "green", Occupied: "red", Reserved: "blue",
			Cleaning: "yellow", "Out of Service": "darkgrey",
		};
		if (frm.doc.status) {
			frm.page.set_indicator(__(frm.doc.status), colors[frm.doc.status] || "grey");
		}

		if (!frm.is_new()) {
			if (frm.doc.status === "Occupied") {
				frm.add_custom_button(__("View Active Order"), () => {
					frappe.set_route("List", "CD Order", {
						table: frm.doc.name, status: ["in", ["Open", "Preparing", "Served"]],
					});
				}, __("Actions"));
			}

			frm.add_custom_button(__("View on Table Map"), () => {
				frappe.set_route("candela-table-map");
			}, __("View"));

			render_cd_table_visual(frm);
		}
	},
});

function render_cd_table_visual(frm) {
	const sc = {
		Available: "var(--green-500)", Occupied: "var(--red-500)", Reserved: "var(--blue-500)",
		Cleaning: "var(--yellow-500)", "Out of Service": "var(--text-muted)",
	};
	const color = sc[frm.doc.status] || "var(--text-muted)";

	const wrapper = frm.dashboard.add_section("", __("Table Info"));
	$(wrapper).html(`
		<div class="cd-table-visual fv-fx-page-enter" style="padding:12px 0;">
			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;">
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:22px;font-weight:700;color:${color};">
						${__(frm.doc.status || "Available")}
					</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Status")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:28px;font-weight:700;color:var(--primary);">
						${frm.doc.capacity || frm.doc.seats || "—"}
					</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Capacity")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:16px;font-weight:600;">
						${frappe.utils.escape_html(frm.doc.section || frm.doc.area || "—")}
					</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Section")}</div>
				</div>
			</div>
		</div>
	`);
}
