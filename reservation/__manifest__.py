{
    "name": "reservation",
    "version" : "1.0",
    "author": "Abdessadek Hmiddouch",
    "depends": ["base", "mail", "sale_management", "portal", "website"],
    "category": "Reservation",
    "description": "Reservation Module",
    "license": "LGPL-3",

    "data" : [
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv",
        "views/reservation_reservation_view.xml",
        "views/reservation_menu.xml"
    ]
}