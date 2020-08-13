# -*- coding: utf-8 -*-
import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

from odoo.tools.translate import _
import math


class DailyActivitySheet(models.Model):
    _name = "daily.activity"
    _rec_name = 'name'

    name = fields.Char('Nom de l\'activité')


class DailyActivity(models.Model):
    _name = "daily.activity.sheet"
    _rec_name = 'name'

    name = fields.Char('Description')
    medecin = fields.Many2one('hr.employee', string="Médecin")
    in_date = fields.Datetime('Heure d\'entrée')
    out_date = fields.Datetime('Heure de sortie')
    activity_ids = fields.One2many('daily.activity.line', 'daily_activity_sheet_id')
    total_hours = fields.Float('Nombre d\'heures total', compute='_compute_activities', store=True)
    activity_counts = fields.Float('Nombre d\'activités total', compute='_compute_activities', store=True)

    def in_date_now(self):
        self.in_date = datetime.now()

    def out_date_now(self):
        self.out_date = datetime.now()

    @api.depends('activity_ids')
    def _compute_activities(self):
        self.total_hours = self.activity_counts = 0
        if self.activity_ids:
            self.total_hours = sum(activity.num_hours for activity in self.activity_ids)
            self.activity_counts = len(self.activity_ids)


class ActivityLine(models.Model):
    _name = "daily.activity.line"

    activity_id = fields.Many2one('daily.activity')
    daily_activity_sheet_id = fields.Many2one('daily.activity.sheet')
    num_hours = fields.Integer('Nombre d\'heures')
    description = fields.Char('Description')



