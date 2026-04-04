// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT
// For license information, please see license.txt

frappe.ui.form.on('Menu Item', {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.slug) {
            frm.add_custom_button(__('View on Website'), function() {
                window.open('/dela/menu/' + frm.doc.slug, '_blank');
            });
        }
    }
});
