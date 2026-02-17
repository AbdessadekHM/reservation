from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError #type:ignore

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
        

    def confirm(self):
        if not len(self.line_ids) :
            raise ValidationError("You should at least create one reservation line")
        
        order_lines = []

        for line in self.line_ids:
            order_lines.append(
                Command.create({
                    "name": f"{line.reservation_id.name}",
                    "product_id": line.product_id.id,
                    "price_unit": line.unit_price,
                    "product_uom_qty": line.quantity
                })
            )
            pass
        sale_order = self.env["sale.order"].create({
            "partner_id": self.partner_id.id,
            "reservation_id": self.id,
            "order_line": order_lines
            })
        self.state = "confirmed"


        pass

    


