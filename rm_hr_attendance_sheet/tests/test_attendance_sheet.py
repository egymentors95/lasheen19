# -*- coding: utf-8 -*-
# Part of rm_hr_attendance_sheet. See LICENSE file for full copyright and licensing details.

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from odoo.tests import tagged
from odoo.exceptions import UserError, ValidationError
from odoo.addons.rm_hr_attendance_sheet.tests.common import AttendanceSheetTestCommon


@tagged('post_install', '-at_install')
class TestAttendanceSheet(AttendanceSheetTestCommon):
    """Test attendance.sheet: compute fields, constraints, workflow."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sheet_date_from = cls.version_start
        cls.sheet_date_to = cls.version_end

    def _create_sheet(self, employee=None, date_from=None, date_to=None, contract_id=None):
        employee = employee or self.employee
        date_from = date_from or self.sheet_date_from
        date_to = date_to or self.sheet_date_to
        cid = contract_id.id if hasattr(contract_id, 'id') else (contract_id or self.version.id)
        sheet = self.env['attendance.sheet'].create({
            'employee_id': employee.id,
            'date_from': date_from,
            'date_to': date_to,
            'contract_id': cid,
            'att_policy_id': self.policy.id,
        })
        return sheet

    def test_sheet_create_and_name(self):
        sheet = self._create_sheet()
        self.assertTrue(sheet.name)
        self.assertIn(self.employee.name, sheet.name)
        self.assertEqual(sheet.state, 'draft')
        self.assertEqual(sheet.contract_id, self.version)

    def test_compute_sheet_total_no_lines(self):
        sheet = self._create_sheet()
        self.assertEqual(sheet.no_overtime, 0)
        self.assertEqual(sheet.tot_overtime, 0)
        self.assertEqual(sheet.no_late, 0)
        self.assertEqual(sheet.tot_late, 0)
        self.assertEqual(sheet.no_absence, 0)
        self.assertEqual(sheet.tot_absence, 0)
        self.assertEqual(sheet.no_difftime, 0)
        self.assertEqual(sheet.tot_difftime, 0)
        self.assertEqual(sheet.unattended_days, 0)
        self.assertEqual(sheet.attendance_count, 0)

    def test_compute_sheet_total_with_lines(self):
        sheet = self._create_sheet()
        # Worked day: status left empty (no 'wd' in selection; only ab/weekend/ph/leave)
        self.env['attendance.sheet.line'].create({
            'att_sheet_id': sheet.id,
            'date': self.sheet_date_from,
            'day': '0',
            'overtime': 2.0,
            'late_in': 0.5,
            'diff_time': 0,
            'worked_hours': 8.0,
        })
        self.env['attendance.sheet.line'].create({
            'att_sheet_id': sheet.id,
            'date': self.sheet_date_from + timedelta(days=1),
            'day': '1',
            'overtime': 0,
            'late_in': 0,
            'diff_time': 2.0,
            'status': 'ab',
            'worked_hours': 0,
        })
        self.assertEqual(sheet.no_overtime, 1)
        self.assertEqual(sheet.tot_overtime, 2.0)
        self.assertEqual(sheet.no_late, 1)
        self.assertEqual(sheet.tot_late, 0.5)
        self.assertEqual(sheet.no_absence, 1)
        self.assertEqual(sheet.tot_absence, 2.0)
        self.assertEqual(sheet.attendance_count, 1)

    def test_compute_diff_days_full_period(self):
        sheet = self._create_sheet()
        self.assertEqual(sheet.no_diff_days, 0)

    def test_compute_diff_days_contract_starts_later(self):
        """Contract starts 5 days after sheet period: no_diff_days = 5."""
        sheet_date_from = self.version_start
        sheet_date_to = self.version_end
        # Use a second employee to avoid overlapping contract with existing version
        employee2 = self.env['hr.employee'].create({
            'name': 'Test Employee 2',
            'company_id': self.company.id,
        })
        version_later = self.env['hr.version'].create({
            'employee_id': employee2.id,
            'name': 'Version Later',
            'date_version': sheet_date_from + relativedelta(days=5),
            'contract_date_start': sheet_date_from + relativedelta(days=5),
            'contract_date_end': sheet_date_to,
            'resource_calendar_id': self.calendar.id,
            'structure_type_id': self.structure_type.id,
            'wage': 3000.0,
            'att_policy_id': self.policy.id,
        })
        sheet = self._create_sheet(
            employee=employee2,
            contract_id=version_later.id,
        )
        self.assertEqual(sheet.no_diff_days, 5)

    def test_check_date_overlap(self):
        self._create_sheet()
        with self.assertRaises(UserError):
            self._create_sheet(
                date_from=self.sheet_date_from + timedelta(days=5),
                date_to=self.sheet_date_to,
            )

    def test_action_confirm_and_draft(self):
        sheet = self._create_sheet()
        sheet.action_confirm()
        self.assertEqual(sheet.state, 'confirm')
        sheet.action_draft()
        self.assertEqual(sheet.state, 'draft')

    def test_action_approve(self):
        """Approve requires payroll structure (default_struct_id) to create payslip."""
        sheet = self._create_sheet()
        sheet.action_confirm()
        sheet.with_user(self.user_hr_manager).action_approve()
        self.assertEqual(sheet.state, 'done')

    def test_onchange_employee_no_contract_raises(self):
        emp_no_version = self.env['hr.employee'].create({
            'name': 'No Version Employee',
            'company_id': self.company.id,
        })
        sheet = self.env['attendance.sheet'].new({
            'employee_id': emp_no_version.id,
            'date_from': self.sheet_date_from,
            'date_to': self.sheet_date_to,
        })
        with self.assertRaises(ValidationError):
            sheet.onchange_employee()
