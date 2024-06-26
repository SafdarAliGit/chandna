frappe.ui.form.on("Item", {
    refresh: function (frm) {
        if (frm.doc.item_group_name == "Yarn") {
            frm.set_df_property("brand_name", "hidden", 0);
            frm.set_df_property("yarn_count", "hidden", 0);
            frm.set_df_property("yarn_quality", "hidden", 0);
            frm.set_df_property("color", "hidden", 0);
            frm.set_df_property("yarn_gsm", "hidden", 0);
        } else {
            frm.set_df_property("brand_name", "hidden", 1);
            frm.set_df_property("yarn_count", "hidden", 1);
            frm.set_df_property("yarn_quality", "hidden", 1);
            frm.set_df_property("color", "hidden", 1);
            frm.set_df_property("yarn_gsm", "hidden", 1);
        }

    },
    brand_name: function (frm) {
        set_item_code_and_name(frm);
    },
    yarn_count: function (frm) {
        set_item_code_and_name(frm);
    },
    yarn_quality: function (frm) {
        set_item_code_and_name(frm);
    },
    color: function (frm) {
        set_item_code_and_name(frm);
    },
    yarn_gsm: function (frm) {
        set_item_code_and_name(frm);
    },

    item_group_name: function (frm) {
        items_visibility(frm);
    },

});

function set_item_code_and_name(frm) {
    var item_code = '';
    var item_name = '';
    item_code = `${frm.doc.brand_name || ''} ${frm.doc.yarn_count || ''} ${frm.doc.yarn_quality || ''} ${frm.doc.color || ''} ${frm.doc.yarn_gsm || ''}`;
    item_name = `${frm.doc.brand_name || ''} ${frm.doc.yarn_count || ''} ${frm.doc.yarn_quality || ''} ${frm.doc.color || ''} ${frm.doc.yarn_gsm || ''}`;
    frm.set_value("item_code", item_code);
    frm.set_value("item_name", item_name);

}

function items_visibility(frm) {
    if (frm.doc.item_group_name == "Yarn") {
        frm.set_df_property("brand_name", "hidden", 0);
        frm.set_df_property("yarn_count", "hidden", 0);
        frm.set_df_property("yarn_quality", "hidden", 0);
        frm.set_df_property("color", "hidden", 0);
        frm.set_df_property("yarn_gsm", "hidden", 0);
    } else {
        frm.set_df_property("brand_name", "hidden", 1);
        frm.set_df_property("yarn_count", "hidden", 1);
        frm.set_df_property("yarn_quality", "hidden", 1);
        frm.set_df_property("color", "hidden", 1);
        frm.set_df_property("yarn_gsm", "hidden", 1);
    }
}

