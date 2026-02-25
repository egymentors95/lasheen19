# -*- coding: utf-8 -*-
# Part of rm_hr_attendance_sheet. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.tests import common
from odoo.addons.mail.tests.common import mail_new_test_user


class AttendanceSheetTestCommon(common.TransactionCase):
    """Common setup for attendance sheet tests: employee, version (contract), calendar, policy and rules."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.calendar = cls.env.ref('resource.resource_calendar_std', raise_if_not_found=False)
        if not cls.calendar:
            cls.calendar = cls.env['resource.calendar'].create({
                'name': 'Standard 40h',
                'attendance_ids': [
                    (0, 0, {'name': 'Monday', 'dayofweek': '0', 'hour_from': 8, 'hour_to': 16}),
                    (0, 0, {'name': 'Tuesday', 'dayofweek': '1', 'hour_from': 8, 'hour_to': 16}),
                    (0, 0, {'name': 'Wednesday', 'dayofweek': '2', 'hour_from': 8, 'hour_to': 16}),
                    (0, 0, {'name': 'Thursday', 'dayofweek': '3', 'hour_from': 8, 'hour_to': 16}),
                    (0, 0, {'name': 'Friday', 'dayofweek': '4', 'hour_from': 8, 'hour_to': 16}),
                ],
            })

        # Late rule with one line: rate type, time >= 0.5 -> rate 1.0
        cls.late_rule = cls.env['hr.late.rule'].create({
            'name': 'Test Late Rule',
        })
        cls.env['hr.late.rule.line'].create({
            'late_id': cls.late_rule.id,
            'type': 'rate',
            'time': 0.5,
            'rate': 1.0,
            'first': 1,
            'second': 1,
            'third': 1,
            'fourth': 1,
            'fifth': 1,
        })

        # Absence rule: first time rate 1.0
        cls.absence_rule = cls.env['hr.absence.rule'].create({
            'name': 'Test Absence Rule',
        })
        cls.env['hr.absence.rule.line'].create({
            'absence_id': cls.absence_rule.id,
            'rate': 1.0,
            'counter': '1',
        })

        # Diff rule: one line rate 1.0
        cls.diff_rule = cls.env['hr.diff.rule'].create({
            'name': 'Test Diff Rule',
        })
        cls.env['hr.diff.rule.line'].create({
            'diff_id': cls.diff_rule.id,
            'type': 'rate',
            'time': 0.5,
            'rate': 1.0,
            'first': 1,
            'second': 1,
            'third': 1,
            'fourth': 1,
            'fifth': 1,
        })

        # Overtime rule (workday)
        cls.overtime_rule = cls.env['hr.overtime.rule'].create({
            'name': 'Test OT Rule',
            'type': 'wd',
            'active_after': 0,
            'rate': 1.5,
        })

        # Attendance policy
        cls.policy = cls.env['hr.attendance.policy'].create({
            'name': 'Test Policy',
            'late_rule_id': cls.late_rule.id,
            'absence_rule_id': cls.absence_rule.id,
            'diff_rule_id': cls.diff_rule.id,
            'overtime_rule_ids': [(4, cls.overtime_rule.id)],
        })

        # Structure type (required by hr.version); use module's if available so payslip can be created
        cls.structure_type = cls.env.ref(
            'rm_hr_attendance_sheet.structure_type_attendance_sheet',
            raise_if_not_found=False,
        )
        if not cls.structure_type:
            cls.structure_type = cls.env['hr.payroll.structure.type'].search([], limit=1)
        if not cls.structure_type:
            cls.structure_type = cls.env['hr.payroll.structure.type'].create({
                'name': 'Test Structure Type',
            })
        if not cls.structure_type.default_struct_id:
            struct = cls.env['hr.payroll.structure'].search(
                [('type_id', '=', cls.structure_type.id)], limit=1
            )
            if struct:
                cls.structure_type.default_struct_id = struct.id

        # Employee
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Test Employee',
            'company_id': cls.company.id,
        })

        # Employee version (replaces contract in Odoo 19) with policy and calendar
        cls.today = date.today()
        cls.version_start = cls.today.replace(day=1) - relativedelta(months=1)
        cls.version_end = cls.version_start + relativedelta(months=2, days=-1)
        cls.version = cls.env['hr.version'].create({
            'employee_id': cls.employee.id,
            'name': 'Test Version',
            'date_version': cls.version_start,
            'contract_date_start': cls.version_start,
            'contract_date_end': cls.version_end,
            'resource_calendar_id': cls.calendar.id,
            'structure_type_id': cls.structure_type.id,
            'wage': 3000.0,
            'att_policy_id': cls.policy.id,
            'auto_attendance_sheet': False,
        })

        cls.user_hr_manager = mail_new_test_user(
            cls.env,
            login='att_sheet_manager',
            groups='rm_hr_attendance_sheet.group_attendance_sheet_manager,hr.group_hr_manager,hr_payroll.group_hr_payroll_user',
            name='Attendance Sheet Manager',
        )
