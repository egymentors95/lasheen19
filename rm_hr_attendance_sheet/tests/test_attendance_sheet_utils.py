# -*- coding: utf-8 -*-
# Part of rm_hr_attendance_sheet. See LICENSE file for full copyright and licensing details.

from datetime import datetime, time, timedelta

from odoo.tests import tagged
from odoo.addons.rm_hr_attendance_sheet.tests.common import AttendanceSheetTestCommon
from odoo.addons.rm_hr_attendance_sheet.models.utils import (
    time_to_float,
    interval_to_float,
    tz_localize,
)


@tagged('post_install', '-at_install')
class TestAttendanceSheetUtils(AttendanceSheetTestCommon):
    """Test utility functions: time_to_float, interval_to_float, tz_localize."""

    def test_time_to_float(self):
        self.assertEqual(time_to_float(time(0, 0, 0)), 0.0)
        self.assertEqual(time_to_float(time(12, 0, 0)), 12.0)
        self.assertEqual(time_to_float(time(8, 30, 0)), 8.5)
        self.assertEqual(time_to_float(time(9, 15, 0)), 9.25)
        self.assertEqual(time_to_float(time(17, 45, 0)), 17.75)

    def test_interval_to_float(self):
        base = datetime(2024, 1, 1, 8, 0, 0)
        end = base + timedelta(hours=2, minutes=30)
        self.assertEqual(interval_to_float((base, end)), 2.5)
        end2 = base + timedelta(hours=8)
        self.assertEqual(interval_to_float((base, end2)), 8.0)

    def test_tz_localize_returns_naive(self):
        import pytz
        utc_dt = datetime(2024, 6, 15, 12, 0, 0)
        tz = pytz.timezone('Europe/Brussels')
        result = tz_localize(utc_dt, tz)
        self.assertIsInstance(result, datetime)
        self.assertIsNone(result.tzinfo)
