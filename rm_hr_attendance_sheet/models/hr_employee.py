# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (C) 2020.
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    website': https://www.linkedin.com/in/ramadan-khalil-a7088164
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
import pytz


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # Expose hr.version fields on the employee form for easy access
    att_policy_id = fields.Many2one(
        'hr.attendance.policy',
        string='Attendance Policy',
        related='current_version_id.att_policy_id',
        readonly=False,
        store=True,
    )
    auto_attendance_sheet = fields.Boolean(
        string='Auto Generate Attendance Sheet',
        related='current_version_id.auto_attendance_sheet',
        readonly=False,
        store=True,
    )

    def _get_employee_tz(self):
        self.ensure_one()
        tz = self.tz or self.env.user.tz or 'UTC'
        return pytz.timezone(tz)
