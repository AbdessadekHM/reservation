from odoo import models, fields

class SaleOrder(models.Model):
    # _name = "sale.order"
    _inherit="sale.order"

    reservation_id=fields.Many2one("reservation.reservation")






