// Copyright (c) 2026, Arkan Lab — License: MIT
frappe.ui.form.on("POS Invoice", {
	refresh(frm) {
		if (!frm.is_new()) {
			render_cd_pos_visual(frm);
		}
	},
});

function render_cd_pos_visual(frm) {
	const items_count = (frm.doc.items || []).length;
	const wrapper = frm.dashboard.add_section("", __("Order Summary"));
	$(wrapper).html(`
		<div class="cd-pos-visual fv-fx-page-enter" style="padding:12px 0;">
			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;">
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:24px;font-weight:700;color:var(--primary);">${items_count}</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Items")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:22px;font-weight:700;color:var(--green-500);">
						${format_currency(frm.doc.grand_total || 0)}
					</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Grand Total")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:16px;font-weight:600;">
						${frappe.utils.escape_html(frm.doc.customer || "—")}
					</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Customer")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:16px;font-weight:600;">
						${frappe.utils.escape_html(frm.doc.table || "—")}
					</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Table")}</div>
				</div>
			</div>
		</div>
	`);
}
