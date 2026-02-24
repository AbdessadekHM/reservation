from odoo import http
from odoo.http import request  # type: ignore
from odoo.exceptions import AccessError, ValidationError, UserError  # type: ignore


class ReservationController(http.Controller):

    @http.route(["/api/test"], methods=["GET"], type="jsonrpc", auth="user")
    def test(self):
        return {"message": "hello world"}

    @http.route(
        ["/api/reservation/create"],
        methods=["POST"],
        type="jsonrpc",
        auth="user",
        csrf=False,
    )
    def create_reservation(self, **kwargs):

        try:

            req = request.get_json_data()

            data = req["params"]["args"][5]
            print("\n\n\n\n\n\n")
            print(data)
            print("\n\n\n\n\n\n")
            request.env["reservation.reservation"].create(data)

            return {
                "stats": "success",
                "code": 200,
                "message": "Reservation Created Successfully",
            }
        except ValidationError as e:
            return {"status": "error", "code": 401, "message": e.args[0]}
        except AccessError:
            return {"status": "error", "code": 403, "message": "Access not allowed"}

    @http.route(
        ["/api/reservation/<id>"],
        methods=["GET"],
        type="jsonrpc",
        auth="user",
        csrf=False,
    )
    def get_reservation(self, id):
        try:
            reservation = request.env["reservation.reservation"].search(
                [("id", "=", id)]
            )
            data = {
                "name": reservation.name,
                "partner_id": reservation.partner_id.name,
                "reservation_start_date": reservation.reservation_start_date,
                "reservation_end_date": reservation.reservation_end_date,
            }
            return {"data": data}

        except ValidationError as e:
            return {"status": "error", "code": 401, "message": e.args[0]}
        except AccessError:
            return {"status": "error", "code": 403, "message": "Access not allowed"}

    @http.route(["/api/reservations"], methods=["GET"], type="jsonrpc", auth="user")
    def get_reservations(self):
        try:

            reservations = request.env["reservation.reservation"].search([(1, "=", 1)])
            data = list()
            for reservation in reservations:

                data.append(
                    {
                        "name": reservation.name,
                        "partner_id": reservation.partner_id.name,
                        "reservation_start_date": reservation.reservation_start_date,
                        "reservation_end_date": reservation.reservation_end_date,
                    }
                )

            return {"data": data}

        except ValidationError as e:
            return {"status": "error", "code": 401, "message": e.args[0]}
        except AccessError:
            return {"status": "error", "code": 403, "message": "Access not allowed"}

    @http.route(
        ["/api/reservation/<id>/confirm"], methods=["GET"], type="jsonrpc", auth="user"
    )
    def confirm_reservation(self, id):
        try:
            reservation = request.env["reservation.reservation"].search(
                [("id", "=", id)]
            )

            if len(reservation) == 0:
                return

            reservation.confirm()

            return {"status": 200, "message": "Reservation is comfirmed sucessfully"}

        except ValidationError as e:
            return {"status": "error", "code": 401, "message": e.args[0]}
        except AccessError:
            return {"status": "error", "code": 403, "message": "Access not allowed"}

    @http.route(
        ["/api/reservation/<id>/cancel"], methods=["GET"], type="jsonrpc", auth="user"
    )
    def cancel_reservation(self, id):
        try:
            reservation = request.env["reservation.reservation"].search(
                [("id", "=", id)]
            )

            reservation.cancel()

            return {"status": 200, "message": "Reservation is cancelled sucessfully"}
        except ValidationError as e:
            return {"status": "error", "code": 401, "message": e.args[0]}
        except AccessError:
            return {"status": "error", "code": 403, "message": "Access not allowed"}
