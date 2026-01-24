{
    "name": "Social Insurance",
    "version": "19.0.0.1.0",
    "summary": "Social Insurance",
    "description": """
Social Insurance    """,
    "category": "Human Resources",
    "author": "LasheenTech",
    "website": "",
    "license": "LGPL-3",
    "depends": [
        "hr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/insurance_office_views.xml",
        "views/job_title_views.xml",
        "views/social_category_views.xml",
        "views/hr_employee_views.xml",
        "views/social_report_view.xml",
        "reports/social_insurance_template_views.xml",
        "reports/action_report_views.xml",

    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}