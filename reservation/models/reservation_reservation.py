from odoo import models, fields, api

class Reservation(models.Model):
    _name = "reservation.reservation"
    _description="table of reservation"
    _inherit=["mail.thread"]

    name=fields.Char(string="Reservation name", default=lambda self: self._get_sequence_number(), readonly=True)
    partner_id=fields.Many2one("res.partner", "Client")
    reservation_date=fields.Date(default=fields.Date.today())
    state=fields.Selection([
        ('draft', 'Draf'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    sale_order_ids=fields.One2many("sale.order", "reservation_id")
    line_ids=fields.One2many("reservation.reservation.line", "reservation_id")
    amount_total=fields.Float(compute="_calculate_amount_total")

    def _get_sequence_number(self):

        sequence_number = self.env["ir.sequence"].next_by_code('reservation.reservation')

        return sequence_number

    @api.depends("line_ids")
    def _calculate_amount_total(self):
        for record in self:
            record.amount_total=sum([line.subtotal for line in record.line_ids])

    


