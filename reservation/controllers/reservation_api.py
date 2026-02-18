from odoo import http
from odoo.http import request #type:ignore


class ReservationController(http.Controller):

    @http.route(['/api/test'], methods=['GET'], type='jsonrpc', auth="user" )
    def test(self):
        return {"message": "hello world"}
    

    @http.route(['/api/reservation/create'], methods=['POST'], type='jsonrpc', auth="user", csrf=False )
    def create_reservation(self, **kwargs):

        data=request.get_json_data()

        print("\n\n\n\n\n\n\n")
        print("request received")
        print("partner_id")
        print(data)
        print(kwargs)



        request.env["reservation.reservation"].create(data)



    @http.route(['/api/reservation/<id>'], methods=['GET'], type='jsonrpc', auth="user", csrf=False)
    def get_reservation(self, id):
        reservation = request.env["reservation.reservation"].search([
            ('id', '=', id)
        ])
        print("\n\n\n")
        print(reservation)
        data = {
            "name" : reservation.name,
            "partner_id": reservation.partner_id.name,
            "reservation_start_date": reservation.reservation_start_date,
            "reservation_end_date": reservation.reservation_end_date
            
        }
        # return request.make_json_response(data)
        return {"data":data}


    @http.route(['/api/reservations'], methods=['GET'], type='jsonrpc', auth="user" )
    def get_reservations(self):
        reservations = request.env["reservation.reservation"].search([
            (1,'=',1)
        ])
        data = list()
        for reservation in reservations:

            data.append({
                "name" : reservation.name,
                "partner_id": reservation.partner_id.name,
                "reservation_start_date": reservation.reservation_start_date,
                "reservation_end_date": reservation.reservation_end_date
            })

        return {"data":data} 


    @http.route(['/api/reservation/<id>/confirm'], methods=['GET'], type='jsonrpc', auth="user" )
    def confirm_reservation(self, id):
        reservation = request.env["reservation.reservation"].search([
            ('id', '=', id)
        ])
        
        if len(reservation) == 0:
            return
        
        reservation.confirm()


        pass

    @http.route(['/api/reservation/<id>/cancel'], methods=['GET'], type='jsonrpc', auth="user" )
    def cancel_reservation(self, id):
        reservation = request.env["reservation.reservation"].search([
            ('id', '=', id)
        ])
        
        if len(reservation) == 0:
            return
        
        reservation.cancel()







