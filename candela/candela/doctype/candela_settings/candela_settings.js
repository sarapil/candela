// Copyright (c) 2026, Arkan Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Candela Settings', {
    refresh(frm) {
        // Install Demo Data button
        if (!frm.doc.demo_data_installed) {
            frm.add_custom_button(__('Install Demo Data'), function() {
                frappe.confirm(
                    __('This will add demo menu items, gallery photos, events, and reviews. Continue?'),
                    function() {
                        frappe.call({
                            method: 'candela.demo.load_demo_data',
                            freeze: true,
                            freeze_message: __('Installing demo data...'),
                            callback: function(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint({
                                        title: __('Demo Data Installed'),
                                        message: r.message.message,
                                        indicator: 'green'
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __('Demo'));
        }

        // Remove Demo Data button
        if (frm.doc.demo_data_installed) {
            frm.add_custom_button(__('Remove Demo Data'), function() {
                frappe.confirm(
                    __('This will permanently delete ALL demo data. Your real data will NOT be affected. Continue?'),
                    function() {
                        frappe.call({
                            method: 'candela.demo.purge_demo_data',
                            freeze: true,
                            freeze_message: __('Removing demo data...'),
                            callback: function(r) {
                                if (r.message && r.message.success) {
                                    frappe.msgprint({
                                        title: __('Demo Data Removed'),
                                        message: r.message.message,
                                        indicator: 'orange'
                                    });
                                    frm.reload_doc();
                                }
                            }
                        });
                    }
                );
            }, __('Demo'));
        }

        // Quick links
        frm.add_custom_button(__('View Website'), function() {
            window.open('/dela', '_blank');
        });
    }
});
