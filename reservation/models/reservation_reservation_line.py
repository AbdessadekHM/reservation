from odoo import models, fields

class ReservationLine(models.Model):
    _name = "reservation.reservation.line"
    _description="table of reservation lines"

    name=fields.Char(string="Reservation line")
    
    reservation_id=fields.Many2one("reservation.reservation")
    product_id=fields.Many2one("product.product")

    quantity=fields.Integer(string="Quantity")
    unit_price=fields.Float(string="Price")
    subtotal=fields.Float(compute="")




