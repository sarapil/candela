// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT
// For license information, please see license.txt

frappe.ui.form.on('Online Order', {
    refresh(frm) {
        if (frm.doc.tracking_token) {
            frm.add_custom_button(__('Track Order'), function() {
                window.open('/dela/order-tracking?token=' + frm.doc.tracking_token, '_blank');
            });
        }
    }
});
