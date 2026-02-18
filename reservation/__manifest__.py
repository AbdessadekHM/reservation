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
        "data/ir_action_server_data.xml",
        "report/reservation_reservation_template.xml",
        "report/reservation_reservation_pdf_report.xml",
        "security/reservation_groups.xml",
        "security/reservation_reservation_security.xml",
        "security/ir.model.access.csv",
        "views/reservation_reservation_view.xml",
        "report/reservation_reservation_report.xml",
        "views/reservation_date_filter.xml",
        "views/reservation_menu.xml",
    ]
}