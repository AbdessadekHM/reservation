from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request #type:ignore


class ReservationPortal(CustomerPortal):

    @http.route(["/my/reservations"], type="http", auth="user", website=True)
    def get_reservations(self):
        values = self._prepare_portal_layout_values()
        reservations = request.env["reservation.reservation"].search([
            ('create_uid','=',request.env.user.id)
        ])
        values.update({
            'reservations': reservations,
            'page_name': 'custom_records_page',
        })

        print("\n\n\n\n\n")
        print("request received from the controller")
        print(len(reservations))
        print(request.env.user.id)
        print(request.env.user.partner_id.id)
        print("\n\n\n\n\n")

        return request.render("reservation.portal_my_reservations", values)

        pass

    @http.route(["/my/reservations/<id>"], type="http", auth="user",website=True)
    def get_reservation(self, id):

        # values = self._prepare_portal_layout_values()
        reservation = request.env["reservation.reservation"].search([
            ('id','=', id)
        ])


        print("\n\n\n\n\n")
        print("request received from the controller id")
        print(len(reservation))
        print(reservation)
        print(reservation.name)
        print(request.env.user.id)
        print(request.env.user.partner_id.id)
        print("\n\n\n\n\n")
        # values.update({
        #     "reservation": reservation
        # })

        return request.render("reservation.portal_my_reservation_detail", {
            "reservation":reservation,
            "page_name": "reservation detail"
        })

        pass
    @http.route(["/my/reservations/pdf/<id>"], type="http")
    def get_pdf(self, id):
        reservation = request.env["reservation.reservation"].search([
            ('id', '=', id)
        ])

        pdf, _ = request.env["ir.actions.report"]._render_qweb_pdf(
            "reservation.action_report_reservation", [reservation.id]
        )

        http_headers = {
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf)),
            ('Content-Disposition', f'attachement; filename="Reservation_{reservation.name}.pdf"')
        }

        return request.make_response(pdf,headers=http_headers)



        pass

    pass
