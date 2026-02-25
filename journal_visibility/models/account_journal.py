from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    allowed_user_ids = fields.Many2many(
        'res.users',
        'res_users_account_journal_rel', 'journal_id',
        'user_id', string='Allowed Users',
        help='Select the users that are allowed to see this journal. If no users are selected, all users will have access to this journal.')

