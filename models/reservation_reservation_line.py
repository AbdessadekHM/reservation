from odoo import models, fields, api


class ReservationLine(models.Model):
    _name = "reservation.reservation.line"
    _description = "table of reservation lines"

    reservation_id = fields.Many2one("reservation.reservation", readonly=True)
    product_id = fields.Many2one("product.product")

    quantity = fields.Integer(string="Quantity")
    unit_price = fields.Float(string="Price")
    subtotal = fields.Float(compute="_calculate_subtotal")

    @api.depends("quantity", "unit_price")
    def _calculate_subtotal(self):
        for record in self:
            record.subtotal = record.unit_price * record.quantity
        pass
