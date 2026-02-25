# -*- coding: utf-8 -*-

##############################################################################
#
#
#    Copyright (C) 2020-TODAY .
#    Author: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################

from odoo import models, fields, api


class HrVersion(models.Model):
    """Extends hr.version (the Odoo 19 replacement for hr.contract) to add
    attendance policy and auto-sheet generation fields."""
    _inherit = 'hr.version'

    att_policy_id = fields.Many2one('hr.attendance.policy',
                                    string='Attendance Policy')
    auto_attendance_sheet = fields.Boolean('Auto Generate Attendance Sheet')
