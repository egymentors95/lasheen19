# Upgrade: rm_hr_attendance_sheet from Odoo 18 to Odoo 19

This document describes the upgrade flow and all changes applied to make the **HR Attendance Sheet And Policies** module compatible with Odoo 19.

---

## 1. Upgrade flow (high level)

1. **Manifest & version** – Bump version and ensure dependencies are valid.
2. **Core API changes** – Adapt to Odoo 19 imports, model renames, and deprecated APIs.
3. **hr.contract → hr.version** – Full migration to the new contract/version model.
4. **Security & groups** – Align with new `res.groups` / `res.groups.privilege` and `res.users` / `ir.ui.menu` fields.
5. **Views & UI** – Remove deprecated attributes and fix view inheritance.
6. **Data & salary rules** – Update salary rule Python code to use the new localdict variables.

---

## 2. Manifest and version

| File | Change |
|------|--------|
| `__manifest__.py` | `'version': '14.001'` → `'version': '19.0.1.0.0'` |

Dependencies (`base`, `hr`, `hr_payroll`, `hr_holidays`, `hr_payroll_holidays`, `hr_attendance`) were left unchanged; all are still valid in Odoo 19.

---

## 3. Core API and code changes

### 3.1 Imports and tools (Odoo 19 moved utilities to `odoo.tools`)

| File | Change |
|------|--------|
| `models/utils.py` | `from odoo.addons.resource.models.utils import float_to_time, float_round` → `from odoo.tools.date_utils import float_to_time` and `from odoo.tools.float_utils import float_round` |
| `models/resource.py` | `Intervals`: `from odoo.addons.resource.models.resource_resource import Intervals` → `from odoo.tools.intervals import Intervals` |
| `models/resource.py` | `float_to_time`: use `from odoo.tools.date_utils import float_to_time` |
| `models/resource.py` | `float_round`: use `from odoo.tools.float_utils import float_round` |

### 3.2 Resource calendar (resource.py)

- Fixed interval clamping bug: `min(dt1, dt1)` → `min(cache_dates[(tz, end_dt)], dt1)`.
- Overnight shifts (`hour_to >= 24`) kept in custom `_cds_attendance_intervals_batch`; `Intervals` constructor usage adjusted for Odoo 19.

### 3.3 Employee and batch

| File | Change |
|------|--------|
| `models/hr_employee.py` | Removed broken `_get_employee_contract()` (undefined `contract`). Later: added `att_policy_id` and `auto_attendance_sheet` as related from `current_version_id` for the form. |
| `models/att_sheet_batch.py` | `att_sheet_id.get_attendances()` → `att_sheet_id._action_get_attendance()`; `tools.ustr(...)` replaced by `format_date(...)`; removed `import babel`. |

### 3.4 Attendance sheet (hr_attendance_sheet.py)

- Logger: `logging.getLogger()` → `logging.getLogger(__name__)`.
- Removed debug `print(...)`.
- Removed obsolete `create_payslip()` that called removed `hr.payslip.onchange_employee_id()`.

---

## 4. hr.contract → hr.version (main breaking change)

In Odoo 19, **`hr.contract` was removed** and replaced by **`hr.version`** (community `hr` module). Payslips use **`version_id`** instead of **`contract_id`**. Contract dates are **`contract_date_start`** / **`contract_date_end`** (no `date_start`/`date_end` on version for contract period). There is no **`state`** (e.g. no `state='open'`); “active” is determined by date overlap.

### 4.1 Model and field mapping

| Old (Odoo 18) | New (Odoo 19) |
|----------------|---------------|
| `hr.contract` | `hr.version` |
| `contract_id` (on payslip) | `version_id` |
| `date_start` / `date_end` (contract period) | `contract_date_start` / `contract_date_end` |
| `state='open'` (active contract) | Date overlap: `contract_date_start <= end_month` and `contract_date_end >= start_month` (or no end) |
| Salary rule localdict `contract` | `version` |
| `payslip.dict.*` | Direct field on payslip, e.g. `payslip.no_diff_days` |

### 4.2 _get_contracts() return value

- **Before:** recordset of contracts.
- **After:** `defaultdict` keyed by `employee.id` → `hr.version` recordset.

Usage change: e.g. `contracts = employee._get_contracts(...); c = contracts[0]` → `d = employee._get_contracts(...); version = d.get(employee.id)` (then use first version if needed).

### 4.3 Files changed for hr.contract → hr.version

| File | Changes |
|------|--------|
| `models/hr_contract.py` | `_inherit = 'hr.contract'` → `_inherit = 'hr.version'`. Class renamed to `HrVersion`. Same custom fields: `att_policy_id`, `auto_attendance_sheet`. |
| `models/hr_employee.py` | Added related fields `att_policy_id` and `auto_attendance_sheet` from `current_version_id` so the employee form can show them. |
| `models/hr_attendance_sheet.py` | `contract_id`: `Many2one('hr.contract')` → `Many2one('hr.version')`. All contract date logic: `date_start`/`date_end` → `contract_date_start`/`contract_date_end`. `onchange_employee` and `action_create_payslip`: use `_get_contracts()` dict and assign `version`. Cron: search `hr.version` with date-domain instead of `hr.contract` with `state='open'`. Payslip creation: pass `version_id` (and `struct_id` from version). `_create_ab_lines`: use `contract_date_start`/`contract_date_end`. |
| `models/att_sheet_batch.py` | Use `contracts_dict.get(employee.id)` instead of treating result as a recordset. |
| `models/hr_payroll.py` | All `slip.contract_id` → `slip.version_id` (e.g. in `compute_sheet`, `_get_new_worked_days_lines`). |
| `views/hr_contract_view.xml` | Dropped inheritance of non-existent `hr_payroll.hr_contract_form_inherit`. Now inherit `hr.view_employee_form` and add `att_policy_id` and `auto_attendance_sheet` after `structure_type_id` (version fields shown on employee form). |
| `data/data.xml` | In salary rule Python: `contract.wage` → `version.wage`; `payslip.dict.no_diff_days` → `payslip.no_diff_days`. |

---

## 5. Security and groups (Odoo 19)

### 5.1 res.groups and res.groups.privilege

- **Before:** `res.groups` had `category_id` (Many2one to `ir.module.category`).
- **After:** `res.groups` has **`privilege_id`** (Many2one to **`res.groups.privilege`**). The privilege has `category_id` (to `ir.module.category`).

| File | Change |
|------|--------|
| `security/security.xml` | Keep `ir.module.category` record. Add **`res.groups.privilege`** record (e.g. `privilege_attendance_sheet`) with `category_id` ref. For each **`res.groups`** record, replace `<field name="category_id" .../>` with `<field name="privilege_id" ref="privilege_attendance_sheet"/>`. |

### 5.2 res.users and ir.ui.menu

- **res.users:** group membership field renamed from **`groups_id`** to **`group_ids`**.
- **ir.ui.menu:** access groups field is **`group_ids`** (not `groups_id`).

| File | Change |
|------|--------|
| `security/security.xml` | In `base.user_admin` record: `groups_id` → `group_ids`. |
| `views/hr_attendance_sheet_view.xml` | In menu record for `hr_attendance.menu_hr_attendance_root`: `groups_id` → `group_ids`. |

---

## 6. Views and UI

### 6.1 Deprecated / invalid view attributes

| Location | Change |
|----------|--------|
| `views/hr_attendance_sheet_view.xml` | Approve button: `invisible="'can_approve' == False or ..."` → `invisible="not can_approve or ..."`. Removed `class="oe_edit_only"` from label. |
| `views/hr_attendance_policy_view.xml` | Removed `class="oe_edit_only"` from label. |
| `views/hr_public_holiday_view.xml` | Removed `class="oe_edit_only"`; statusbar options `'clickable': '1'` → `'clickable': true`. |
| `wizard/change_att_data_view.xml` | Button: `string="_Apply"` → `string="Apply"`; `class="btn-default"` → `class="btn-secondary"`. |

### 6.2 Search view (invalid view definition)

In Odoo 19, the **`<group>`** element inside **`<search>`** must not use **`expand`** or **`string`**.

| File | Change |
|------|--------|
| `views/hr_attendance_sheet_view.xml` | In search view: removed `expand="0"` and `string="Group By"` from `<group>`, added `name="group_by"`, removed extra `<separator/>` inside the group. |

---

## 7. Data and salary rules

| File | Change |
|------|--------|
| `data/data.xml` | All salary rule `amount_python_compute` / `condition_python`: `contract.wage` → `version.wage`; `payslip.dict.no_diff_days` → `payslip.no_diff_days`. |

---

## 8. Summary checklist

- [x] Manifest version set to 19.0.1.0.0.
- [x] Imports updated (`float_to_time`, `float_round`, `Intervals`) to `odoo.tools.*`.
- [x] resource.py: interval bug fix and Odoo 19-compatible Intervals usage.
- [x] hr.contract replaced by hr.version everywhere (model, fields, cron, payslip, batch).
- [x] _get_contracts() dict usage and date fields (contract_date_start/end) applied.
- [x] Payslip uses version_id and payroll overrides use version_id.
- [x] Security: privilege_id on res.groups; group_ids on res.users and ir.ui.menu.
- [x] Views: search group without expand/string; oe_edit_only removed; button/labels and statusbar options fixed.
- [x] Salary rules: version.wage and payslip.no_diff_days (no contract, no payslip.dict).

---

## 9. Testing recommendations

After upgrade:

1. Install/upgrade the module and confirm no load/parse errors.
2. Create or open an employee record and set Attendance Policy and Auto Generate Attendance Sheet (on the version / employee form).
3. Create an attendance sheet for a period and run “Get Attendances”; confirm lines and totals.
4. Confirm batch generation and submission still work.
5. Create a payslip linked to an attendance sheet and run compute; check that attendance sheet data and salary rules (overtime, late, absence, etc.) compute correctly.
6. Check that access rights (Attendance Sheet User / Manager) and menus behave as expected.

---

## 10. Unit tests

The module includes unit tests under `tests/`:

| File | What is tested |
|------|----------------|
| `tests/common.py` | `AttendanceSheetTestCommon`: employee, hr.version, calendar, late/absence/diff/overtime rules, attendance policy. |
| `tests/test_attendance_sheet_utils.py` | `time_to_float`, `interval_to_float`, `tz_localize`. |
| `tests/test_attendance_policy.py` | Policy `get_overtime`, `get_late`, `get_diff`, `get_absence` (rates and thresholds). |
| `tests/test_attendance_sheet.py` | Sheet create, `_compute_sheet_total`, `_compute_diff_days`, `check_date` (overlap), `action_confirm`/`action_draft`/`action_approve`, `onchange_employee` (no contract). |

**Run tests (from project root):**

```bash
python odoo-bin -c odoo.conf -i rm_hr_attendance_sheet --test-enable --stop-after-init
```

Or for a single file:

```bash
python odoo-bin -c odoo.conf -i rm_hr_attendance_sheet --test-enable --stop-after-init --test-tags /rm_hr_attendance_sheet
```

---

*Document generated for the Odoo 18 → 19 upgrade of rm_hr_attendance_sheet.*
