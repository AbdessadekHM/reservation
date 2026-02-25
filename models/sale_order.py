from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    reservation_id = fields.Many2one("reservation.reservation")

    amount_total = fields.Integer(compute="_calculate_total_amount")

    _check_unique_sale = models.Constraint(
        "unique(reservation_id)", "a sale order is already created for this reservation"
    )

    @api.depends("order_line")
    def _calculate_total_amount(self):
        for record in self:
            record.amount_total = sum([line.price_unit * line.product_uom_qty for line in record.order_line])

    def action_cancel(self):

        reservation = self.env["reservation.reservation"].search(
            [("id", "=", self.reservation_id)]
        )

        reservation.state = "cancelled"

        return super().action_cancel()
