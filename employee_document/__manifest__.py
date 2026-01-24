{
    "name": "Employee Document Management",
    "version": "19.0.0.1.0",
    "summary": "Manage employee documents efficiently",
    "description": """
        This module allows for the management of employee documents within the HR system.
        Features include uploading, categorizing, and tracking documents related to employees.
    """,
    "category": "Human Resources",
    "author": "LasheenTech",
    "website": "",
    "license": "LGPL-3",
    "depends": [
        "hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/document_type_views.xml",
        "views/hr_employee_views.xml",
        "views/document_report_view.xml",
        "reports/employee_document_template_views.xml",
        "reports/action_report_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}