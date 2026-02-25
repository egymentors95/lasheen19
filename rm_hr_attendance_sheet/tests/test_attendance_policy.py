# -*- coding: utf-8 -*-
# Part of rm_hr_attendance_sheet. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo.tests import tagged
from odoo.addons.rm_hr_attendance_sheet.tests.common import AttendanceSheetTestCommon


@tagged('post_install', '-at_install')
class TestAttendancePolicy(AttendanceSheetTestCommon):
    """Test hr.attendance.policy logic: get_overtime, get_late, get_diff, get_absence."""

    def test_get_overtime_wd(self):
        base = datetime(2024, 1, 1, 16, 0, 0)
        end = base + timedelta(hours=2)
        act_ot, calc_ot = self.policy.get_overtime('wd', [(base, end)])
        self.assertEqual(act_ot, 2.0)
        self.assertEqual(calc_ot, 2.0 * 1.5)

    def test_get_overtime_below_threshold(self):
        self.overtime_rule.active_after = 3.0
        base = datetime(2024, 1, 1, 16, 0, 0)
        end = base + timedelta(hours=1)
        act_ot, calc_ot = self.policy.get_overtime('wd', [(base, end)])
        self.assertEqual(act_ot, 1.0)
        self.assertEqual(calc_ot, 0.0)

    def test_get_late_zero(self):
        calc_late, cnt = self.policy.get_late(0, [])
        self.assertEqual(calc_late, 0)
        self.assertEqual(cnt, [])

    def test_get_late_rate(self):
        calc_late, cnt = self.policy.get_late(1.0, [])
        self.assertEqual(calc_late, 1.0)
        self.assertIn([0.5, 2], cnt)

    def test_get_diff_zero(self):
        res, cnt = self.policy.get_diff(0, [])
        self.assertEqual(res, 0)
        self.assertEqual(cnt, [])

    def test_get_diff_rate(self):
        res, cnt = self.policy.get_diff(1.0, [])
        self.assertEqual(res, 1.0)
        self.assertIn([0.5, 2], cnt)

    def test_get_absence(self):
        res = self.policy.get_absence(8.0, 1)
        self.assertEqual(res, 8.0)
        res0 = self.policy.get_absence(8.0, 0)
        self.assertEqual(res0, 0.0)
