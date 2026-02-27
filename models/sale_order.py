from odoo import models, fields, api, Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    reservation_id = fields.Many2one("reservation.reservation")

    # amount_total = fields.Float(compute="_calculate_total_amount")
    # amount_total

    _check_unique_sale = models.Constraint(
        "unique(reservation_id)", "a sale order is already created for this reservation"
    )

    @api.depends("order_line")
    def _calculate_total_amount(self):
        for record in self:
            record.amount_total = sum([line.price_unit * line.product_uom_qty for line in record.order_line])

    def write(self, val_list):

        print("\n\n\n\n\n\n\n\n")
        print("from sale write method")
        print(val_list)
        print("\n\n\n\n\n\n\n\n")

        super().write(val_list)


        reservation = self.env["reservation.reservation"].search([
            ('id', '=', self.reservation_id)
        ])

        reservation_lines = self.env["reservation.reservation.line"].search([
            ('reservation_id','=',self.reservation_id)
        ])

        data = {}

        if "order_line" in val_list.keys() :
            print("we've get this")



            lines_ids = [

                Command.create(
                    {
                        "product_id": line.product_id.id,
                        "unit_price": line.price_unit,
                        "quantity": line.product_uom_qty,
                    }
                )
                for line in self.order_line
            
            ]
            data["line_ids"] = lines_ids
        
        if "partner_id" in val_list.keys():
            data["partner_id"] = val_list["partner_id"]
        
        if len(data.keys()) > 0:
            data["state"] = "confirmed"

            reservation_lines.unlink()
            print("\n\n\n\n\n\n\n")
            print("data ")
            print(data)
            print("\n\n\n\n\n\n\n")
            reservation.write(data)
            print("normally data should be saved")

        

    def action_cancel(self):

        reservation = self.env["reservation.reservation"].search(
            [("id", "=", self.reservation_id)]
        )

        reservation.state = "cancelled"

        return super().action_cancel()
