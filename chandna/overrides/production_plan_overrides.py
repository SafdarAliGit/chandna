from pypika.terms import ExistsCriterion

import frappe
from erpnext.manufacturing.doctype.production_plan.production_plan import ProductionPlan


class ProductionPlanOverrides(ProductionPlan):
    @frappe.whitelist()
    def get_items(self):
        self.set("po_items", [])
        if self.get_items_from == "Sales Order":
            self.get_so_items()

        elif self.get_items_from == "Material Request":
            self.get_mr_items()

    def get_so_items(self):
        # Check for empty table or empty rows
        if not self.get("sales_orders") or not self.get_so_mr_list("sales_order", "sales_orders"):
            frappe.throw(frappe._("Please fill the Sales Orders table"), title=_("Sales Orders Required"))

        so_list = self.get_so_mr_list("sales_order", "sales_orders")

        bom = frappe.qb.DocType("BOM")
        so_item = frappe.qb.DocType("Sales Order Item")

        items_subquery = frappe.qb.from_(bom).select(bom.name).where(bom.is_active == 1)
        items_query = (
            frappe.qb.from_(so_item)
            .select(
                so_item.parent,
                so_item.item_code,
                so_item.warehouse,
                (
                        (so_item.qty - so_item.work_order_qty - so_item.delivered_qty) * so_item.conversion_factor
                ).as_("pending_qty"),
                so_item.description,
                so_item.name,
                so_item.bom_no,
                so_item.color
            )
            .distinct()
            .where(
                (so_item.parent.isin(so_list))
                & (so_item.docstatus == 1)
                & (so_item.qty > so_item.work_order_qty)
            )
        )

        if self.item_code and frappe.db.exists("Item", self.item_code):
            items_query = items_query.where(so_item.item_code == self.item_code)
            items_subquery = items_subquery.where(
                self.get_bom_item_condition() or bom.item == so_item.item_code
            )

        items_query = items_query.where(ExistsCriterion(items_subquery))

        items = items_query.run(as_dict=True)

        pi = frappe.qb.DocType("Packed Item")

        packed_items_query = (
            frappe.qb.from_(so_item)
            .from_(pi)
            .select(
                pi.parent,
                pi.item_code,
                pi.warehouse.as_("warehouse"),
                (((so_item.qty - so_item.work_order_qty) * pi.qty) / so_item.qty).as_("pending_qty"),
                pi.parent_item,
                pi.description,
                so_item.name,
            )
            .distinct()
            .where(
                (so_item.parent == pi.parent)
                & (so_item.docstatus == 1)
                & (pi.parent_item == so_item.item_code)
                & (so_item.parent.isin(so_list))
                & (so_item.qty > so_item.work_order_qty)
                & (
                    ExistsCriterion(
                        frappe.qb.from_(bom)
                        .select(bom.name)
                        .where((bom.item == pi.item_code) & (bom.is_active == 1))
                    )
                )
            )
        )

        if self.item_code:
            packed_items_query = packed_items_query.where(so_item.item_code == self.item_code)

        packed_items = packed_items_query.run(as_dict=True)

        self.add_items(items + packed_items)
        self.calculate_total_planned_qty()
