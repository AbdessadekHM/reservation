from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request #type:ignore


class ReservationPortal(CustomerPortal):
    def _prepare_searchbar_sortings(self):
        return {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }

    @http.route(["/my/reservations"], type="http", auth="user", website=True)
    def get_reservations(self, search=None, filterby=None,sortby=None, search_in='content'):
        values = self._prepare_portal_layout_values()

        filters = {
            'all': {'label': 'All', 'domain': [('create_uid', '=',request.env.user.id)]},
            'draft': {'label': 'Draft', 'domain': [('state', '=', 'draft')]},
            'done': {'label': 'Done', 'domain': [('state', '=', 'done')]},
        }

        searchbar_sortings = self._prepare_searchbar_sortings()

        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']



        if not filterby:
            filterby = 'all'
        domain = filters.get(filterby, filters['all'])['domain']

        if search:
            domain += [('name', 'ilike', search)]

        print("\n\n\n\n\n")
        print(domain)
        print("\n\n\n\n\n")

        reservations = request.env["reservation.reservation"].search(domain,order=order)
        values.update({
            'reservations': reservations,
            'page_name': 'my reservations',
            'search': search,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'search_in': search_in
        })

        return request.render("reservation.portal_my_reservations", values)


    @http.route(["/my/reservations/<id>"], type="http", auth="user",website=True)
    def get_reservation(self, id):

        reservation = request.env["reservation.reservation"].search([
            ('id','=', id)
        ])

        return request.render("reservation.portal_my_reservation_detail", {
            "reservation":reservation,
            "page_name": "reservation detail"
        })

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




