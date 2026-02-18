from odoo import fields, models, tools


class ReservationReport(models.Model):

    _name="reservation.reservation.report"


    _auto=False



    name=fields.Char(string="Reservation name", readonly=True)
    partner_id=fields.Many2one("res.partner", "Client", aggregator="sum", readonly=True)
    reservation_start_date=fields.Date(default=fields.Date.today(), string="Start date", store=False, readonly=True)
    reservation_end_date=fields.Date(default=fields.Date.today(), string="End date", store=False, readonly=True)
    state=fields.Selection([
        ('draft', 'Draf'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='draft', readonly=True, aggregator="sum")
    sale_order_id=fields.One2many("sale.order", "reservation_id")
    line_ids=fields.One2many("reservation.reservation.line", "reservation_id")
    line_ids_count=fields.Integer(readonly=True, string="line ids number")
    total_volume=fields.Float(aggregator="sum", readonly=True)


    def _select(self):
        return """
            r.id as id,
            r.name,
            r.partner_id,
            r.state,
            SUM(r.amount_total) AS total_volume,
            COUNT(l.id) as line_ids_count



            """
        pass

    def _from(self):
        return """
            reservation_reservation AS r
            JOIN
            reservation_reservation_line AS l 
            ON l.reservation_id = r.id
            """
        pass 
    def _group_by(self):
        return """
            r.partner_id, r.state,r.name, r.id
            """
        pass


    def _where(self):
        pass

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE view %s as
                SELECT %s
                FROM %s
                GROUP BY %s
                """ % (self._table, self._select(), self._from(), self._group_by()))

        pass







    pass