/**
 * Candela Desk — Admin realtime notifications
 */
(function() {
	'use strict';
	if (typeof frappe === 'undefined') return;

	frappe.realtime.on('candela_new_reservation', function(data) {
		frappe.show_alert({ message: __('New reservation from {0}', [data.guest_name]), indicator: 'blue' }, 7);
	});

	frappe.realtime.on('candela_new_order', function(data) {
		frappe.show_alert({ message: __('New order #{0}', [data.order_id]), indicator: 'green' }, 7);
	});

	frappe.realtime.on('candela_new_review', function(data) {
		frappe.show_alert({ message: __('New review from {0}', [data.customer_name]), indicator: 'orange' }, 7);
	});
})();
