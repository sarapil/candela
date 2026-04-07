// Copyright (c) 2026, Arkan Lab — License: MIT
frappe.ui.form.on("Table Reservation", {
	refresh(frm) {
		const colors = {
			Pending: "orange", Confirmed: "blue", Seated: "green",
			Completed: "darkgrey", Cancelled: "red", "No Show": "red",
		};
		if (frm.doc.status) {
			frm.page.set_indicator(__(frm.doc.status), colors[frm.doc.status] || "grey");
		}

		if (!frm.is_new() && frm.doc.docstatus === 1) {
			if (frm.doc.status === "Confirmed") {
				frm.add_custom_button(__("Seat Guest"), () => {
					frm.call("seat_guest").then(() => frm.reload_doc());
				}, __("Actions"));
			}

			if (["Pending", "Confirmed"].includes(frm.doc.status)) {
				frm.add_custom_button(__("Cancel"), () => {
					frappe.confirm(__("Cancel this reservation?"), () => {
						frm.set_value("status", "Cancelled");
						frm.save();
					});
				}, __("Actions"));

				frm.add_custom_button(__("Mark No Show"), () => {
					frm.set_value("status", "No Show");
					frm.save();
				}, __("Actions"));
			}
		}

		if (!frm.is_new()) {
			render_cd_reservation_visual(frm);
		}
	},
});

function render_cd_reservation_visual(frm) {
	const res_date = frm.doc.reservation_date;
	const days_until = res_date ? frappe.datetime.get_diff(res_date, frappe.datetime.get_today()) : null;
	let when_text = "";
	if (days_until !== null) {
		if (days_until < 0) when_text = __("{0} days ago", [Math.abs(days_until)]);
		else if (days_until === 0) when_text = __("Today");
		else when_text = __("In {0} days", [days_until]);
	}

	const sc = {
		Pending: "var(--orange-500)", Confirmed: "var(--blue-500)", Seated: "var(--green-500)",
		Completed: "var(--text-muted)", Cancelled: "var(--red-500)", "No Show": "var(--red-500)",
	};
	const color = sc[frm.doc.status] || "var(--text-muted)";

	const wrapper = frm.dashboard.add_section("", __("Reservation Summary"));
	$(wrapper).html(`
		<div class="cd-res-visual fv-fx-page-enter" style="padding:12px 0;">
			<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;">
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:22px;font-weight:700;color:${color};">${__(frm.doc.status || "—")}</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Status")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:16px;font-weight:600;">${frappe.utils.escape_html(frm.doc.guest_name || "—")}</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Guest")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:28px;font-weight:700;color:var(--primary);">${frm.doc.party_size || frm.doc.guests || "—"}</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Guests")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:16px;font-weight:600;">${when_text || "—"}</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("When")}</div>
				</div>
				<div class="fv-fx-glass fv-fx-hover-lift" style="padding:14px;border-radius:10px;text-align:center;">
					<div style="font-size:16px;font-weight:600;">${frm.doc.reservation_time || "—"}</div>
					<div style="font-size:11px;color:var(--text-muted);">${__("Time")}</div>
				</div>
			</div>
		</div>
	`);
}
