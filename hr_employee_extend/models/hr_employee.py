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
    duree_stage = fields.Float('Durée de stage', default=0.0)
    cursus_ids = fields.One2many('hr.cursus', 'employee_id', 'Cursus Résident')
    travaux_ids = fields.One2many('hr.travaux', 'auteur', 'Titres et travaux scientifiques')
    cursus_ids_count = fields.Integer(compute="_compute_move_ids_count")
    travaux_ids_count = fields.Integer(compute="_compute_travaux_ids_count")
    issu_de_linternat = fields.Boolean('Issu de l\'intérnat')
    mode_de_recrutement = fields.Many2one('hr.mode.recrutement', string='Mode de recrutement')
    nom_arabe = fields.Char('Nom Arabe')
    ordre_de_mrite = fields.Integer('Ordre de mérite')
    promotion = fields.Char('Promotion')
    region = fields.Char('Région')

    @api.depends('cursus_ids')
    def _compute_move_ids_count(self):
        for record in self:
            record.cursus_ids_count = len(record.cursus_ids)

    @api.depends('travaux_ids')
    def _compute_travaux_ids_count(self):
        for record in self:
            record.travaux_ids_count = len(record.travaux_ids)

    @api.depends('cursus_ids')
    def _calc_moyenne(self):
        for rec in self:
            rec.moyenne_resident = rec.duree_stage = 0.0
            if rec.cursus_ids:
                total = sum(line.note for line in rec.cursus_ids)
                rec.duree_stage = sum(line.duree for line in rec.cursus_ids)
                total_elements = len(rec.cursus_ids)
                rec.moyenne_resident = total / total_elements


class HrCursus(models.Model):
    _name = 'hr.cursus'
    _inherit = 'mail.thread'
    _rec_name = 'service_id'

    employee_id = fields.Many2one('hr.employee')
    promotion = fields.Char('Promotion')
    type_de_service = fields.Char('Type de Service')
    stage = fields.Char('Stage')
    note = fields.Float('Note')
    duree = fields.Integer('Durée (Mois)', compute='_compute_duree')
    service_id = fields.Many2one('hr.department', string="Service")
    date_debut = fields.Date('Date Début')
    date_fin = fields.Date('Date fin')

    @api.depends('date_debut', 'date_fin')
    def _compute_duree(self):
        for rec in self:
            rec.duree = 0
            if rec.date_debut and rec.date_fin:
                rec.duree = (rec.date_fin - rec.date_debut).days / 30
                if rec.duree == 0:
                    rec.duree = 1


class HrModeRecrutement(models.Model):
    _name = 'hr.mode.recrutement'

    name = fields.Char('Mode de recrutement')


class HrTravaux(models.Model):
    _name = 'hr.travaux'

    name = fields.Char('Description')
    article_pdf = fields.Binary('Article (PDF)')
    article_pdf_filename = fields.Char('Article (PDF) filename')
    auteur = fields.Many2one('hr.employee', string='Auteur')
    co_auteur = fields.Many2many('res.partner', string='Co-auteurs')
    date_publication = fields.Date('Date de publication')
    revue_id = fields.Many2one('travaux.revue', string='Revue')


class TravauxRevue(models.Model):
    _name = 'travaux.revue'

    name = fields.Char('Description')
    impact_facteur = fields.Float('Impact Facteur')
    siteweb = fields.Char('Site Web')


