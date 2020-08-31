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


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    moyenne_resident = fields.Float('Moyenne du resident', compute='_calc_moyenne', default=0.0)

    @api.depends('x_studio_cursus_1')
    def _calc_moyenne(self):
        for rec in self:
            rec.moyenne_resident = 0.0
            if rec.x_studio_cursus_1:
                total = sum(line.x_studio_note for line in rec.x_studio_cursus_1 if line.x_studio_note != 0)
                total_elements = len(rec.x_studio_cursus_1)
                rec.moyenne_resident = total / total_elements
