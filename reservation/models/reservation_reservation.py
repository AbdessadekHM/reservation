from odoo import models, fields

class Reservation(models.Model):
    _name = "reservation.reservation"
    _description="table of reservation"
    _inherit=["mail.thread"]

    name=fields.Char(string="Reservation name")
    partner_id=fields.Many2one("res.partner", "Client")
    reservation_date=fields.Date(default=fields.Date.today())
    state=fields.Selection([
        ('draft', 'Draf'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    sale_order_ids=fields.One2many("sale.order", "reservation_id")
    line_ids=fields.One2many("reservation.reservation.line", "reservation_id")
    amount_total=fields.Float(compute="")


