from odoo import models, fields

class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit="sale.order"

    reservation_id=fields.Many2one("reservation.reservation", unique=True)

    _check_unique_sale=models.Constraint(
        'unique(reservation_id)',
        'a sale order is already created for this reservation'
    )

    def action_cancel(self):

        reservation = self.env["reservation.reservation"].search([
            ('id','=', self.reservation_id)
        ])

        reservation.state='cancelled'


        return super().action_cancel()





