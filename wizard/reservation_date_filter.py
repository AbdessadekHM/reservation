from odoo import models, fields, api
from odoo.exceptions import ValidationError  # type: ignore
from ..utils.helpers import generate_excel
import base64


class DateFilter(models.TransientModel):
    _name = "reservation.date.filter"

    reservation_date = fields.Date(default=fields.Date.today())

    def get_report(self):

        selected_ids = self.env.context.get("active_ids")

        records = self.env["reservation.reservation"].search(
            [
                ("id", "in", selected_ids),
                ("reservation_end_date", ">=", self.reservation_date),
                ("reservation_start_date", "<=", self.reservation_date),
            ]
        )

        if not records:
            raise ValidationError("There is no reservation at that time")

        rows = list()
        for record in records:
            for line in record.line_ids:
                rows.append(
                    [
                        line.reservation_id.name,
                        line.reservation_id.partner_id.name,
                        line.product_id.name,
                        line.quantity,
                        line.subtotal,
                    ]
                )

        headers = ["reservation", "client", "produit", "quantite", "totale"]

        excel = generate_excel(rows=rows, headers=headers)
        excel_data = base64.b64encode(excel)

        attachment = self.env["ir.attachment"].create(
            {
                "name": "report.xlsx",
                "type": "binary",
                "datas": excel_data,
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        )

        download_url = f"/web/content/{attachment.id}?download=true"
        return {
            "type": "ir.actions.act_url",
            "url": download_url,
            "target": "new",
        }

    def _get_record_by_id(self, record_id):
        return self.env["reservation.reservation"].search([("id", "=", record_id)])
