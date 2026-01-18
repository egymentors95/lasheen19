from odoo import fields, models, api


class FamilyInsurance(models.Model):
    _name = 'family.insurance'
    _description = 'Family Insurance'


    employee_id = fields.Many2one(comodel_name='hr.employee', string='employee')
    family_member_name = fields.Char()
    relation_id = fields.Many2one(comodel_name='medical.relation', string='Relation')
    insurance_number = fields.Char(string='Insurance Number')
    insurance_provider_id = fields.Many2one(comodel_name='insurance.provider', string='Insurance Provider')
    medical_network_id = fields.Many2one(comodel_name='medical.network', string='Medical Network')
    insurance_category_id = fields.Many2one(comodel_name='insurance.category', string='Insurance Category')
    insurance_start_date = fields.Datetime(string='Insurance Start Date')
    insurance_end_date = fields.Datetime(string='Insurance End Date')
    company_share = fields.Float(string='Company Share')
    employee_share = fields.Float(string='Employee Share')
    monthly_contribution = fields.Float(string='Monthly Contribution', compute='_get_monthly_contribution', store=True)
    company_discount = fields.Float()


    @api.depends('company_share', 'employee_share')
    def _get_monthly_contribution(self):
        for rec in self:
            rec.monthly_contribution = rec.company_share + rec.employee_share