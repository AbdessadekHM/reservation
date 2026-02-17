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
    amount_total=fields.Float(compute="")


    def _create_name(self):
        for record in self:
            sequence_number = self.env["ir.sequence"].next_by_code('custom.order')
            print("\n\n\n")
            print("\n\n\n")
            print("sequenced number is ")
            print(sequence_number)
            print("\n\n\n")
            print("\n\n\n")
            record.name=sequence_number
        pass
    def _get_sequence_number(self):

        sequence_number = self.env["ir.sequence"].next_by_code('reservation.reservation')

        print("\n\n\n")
        print("\n\n\n")
        print("sequenced number is ")
        print(sequence_number)
        print("\n\n\n")
        print("\n\n\n")
        return sequence_number


        pass



