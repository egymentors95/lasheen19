from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_journal_ids = fields.Many2many(
        'account.journal',
        'res_users_account_journal_rel', 'user_id',
        'journal_id', string='Allowed Journals',
        help='Select the journals that this user is allowed to see. If no journals are selected, the user will have access to all journals.')