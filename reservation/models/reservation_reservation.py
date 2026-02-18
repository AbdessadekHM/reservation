from odoo import models, fields, api, Command
from odoo.exceptions import ValidationError #type:ignore
from io import BytesIO
import xlsxwriter  
import base64

class Reservation(models.Model):
    _name = "reservation.reservation"
    _description="table of reservation"
    _inherit=["mail.thread"]

    name=fields.Char(string="Reservation name", default=lambda self: self._get_sequence_number(), readonly=True)
    partner_id=fields.Many2one("res.partner", "Client")
    reservation_start_date=fields.Date(default=fields.Date.today(), string="Start date")
    reservation_end_date=fields.Date(default=fields.Date.today(), string="End date")
    state=fields.Selection([
        ('draft', 'Draf'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='draft')
    sale_order_id=fields.One2many("sale.order", "reservation_id")
    sale_order_id=fields.One2many("sale.order", "reservation_id")
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

    def cancel(self):
        if not len(self.line_ids) :
            raise ValidationError("You should at least create one reservation line")

        if self.state != 'confirmed':
            raise ValidationError("You can't cancel an unconfirmed reservation")

        
        sale_order = self.env["sale.order"].search([('reservation_id', '=', self.id)])

        for sale in sale_order: 
            sale.state='cancel'

        self.state = "cancelled"

    def redirect_to_sales(self):

        print("\n\n\n\n\n")
        print("i get redirect")
        print("\n\n\n\n\n")

        return {
            'name':'sale_order_window_action',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
            'domain': [('reservation_id', '=', self.id)],
        }
        pass
        
    def print_test(self):

        selected_ids = self.env.context.get('active_ids',[])
        records = list()
        rows = list()
        for record_id in selected_ids:
            record = self._get_record_by_id(record_id)
            for line in record.line_ids:
                rows.append([line.reservation_id.name, line.reservation_id.partner_id.name,line.product_id.name,line.quantity, line.subtotal])

            records.append(record)
        headers = ["reservation", "client", "produit","quantite","totale"]

        excel = self._generate_excel(rows=rows, headers=headers)
        excel_data = base64.b64encode(excel)

        attachment = self.env['ir.attachment'].create({
        'name': 'report.xlsx',
        'type': 'binary',
        'datas': excel_data,
        'res_model': self._name,
        'res_id': self.id,
        'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        print("\n\n\n")
        print(attachment)
        print(attachment.id)
        print("\n\n\n")

        
        download_url = f'/web/content/{attachment.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'new',
        }

        








    def _get_record_by_id(self, id):
        record = self.env["reservation.reservation"].search([
            ('id', '=', id)
        ])

        return record

    def _generate_excel(self, rows, headers):
        with BytesIO() as buffer:
            with xlsxwriter.Workbook(buffer, {'in_memory': True}) as workbook:
                worksheet = workbook.add_worksheet()

                for col, header in enumerate(headers):
                    worksheet.write(0, col, header)
                for row_idx, row in enumerate(rows, start=1):
                    for col_idx, cell in enumerate(row):
                        worksheet.write(row_idx, col_idx, cell)
            return buffer.getvalue()



    


