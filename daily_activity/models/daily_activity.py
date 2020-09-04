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
    medecin = fields.Many2one('hr.employee', string="Médecin", default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]))
    in_date = fields.Datetime('Heure d\'entrée')
    out_date = fields.Datetime('Heure de sortie')
    activity_ids = fields.One2many('daily.activity.line', 'daily_activity_sheet_id')
    total_hours = fields.Integer('Nombre d\'heures total', compute='_compute_activities', store=True)
    total_minutes = fields.Integer('Nombre de minutes total', compute='_compute_activities', store=True)
    activity_counts = fields.Float('Nombre d\'activités total', compute='_compute_travaux', store=True)
    is_manager = fields.Boolean('Has Group', compute='_compute_has_group')

    @api.depends('name')
    def _compute_has_group(self):
        self.is_manager = self.env.user.has_group('daily_activity.group_daily_activity_manager')

    def in_date_now(self):
        self.in_date = datetime.now()

    def out_date_now(self):
        self.out_date = datetime.now()

    @api.depends('activity_ids')
    def _compute_activities(self):
        for rec in self:
            rec.activity_counts = 0
            if rec.activity_ids:
                rec.activity_counts = sum(line.num_hours for line in rec.activity_ids)

    @api.depends('in_date', 'out_date')
    def _compute_travaux(self):
        for rec in self:
            rec.total_hours = rec.total_minutes = 0
            if rec.in_date and rec.out_date:
                if rec.in_date < rec.out_date:
                    diff = rec.out_date - rec.in_date
                    hours = int(diff.seconds / 3600)
                    minutes = int(((diff.seconds / 3600) % 1) * 60)
                    rec.total_hours = hours
                    rec.total_minutes = minutes
                else:
                    raise ValidationError('La date d\'entrée ne peut être suppérieure à la date de sortie')


class ActivityLine(models.Model):
    _name = "daily.activity.line"

    activity_id = fields.Many2one('daily.activity')
    daily_activity_sheet_id = fields.Many2one('daily.activity.sheet')
    medecin = fields.Many2one('hr.employee', related='daily_activity_sheet_id.medecin', store=True)
    date = fields.Datetime(related='daily_activity_sheet_id.in_date', store=True)
    num_hours = fields.Integer('Nombre de fois')
    description = fields.Char('Description')
    document = fields.Binary('Pièce Jointe')



