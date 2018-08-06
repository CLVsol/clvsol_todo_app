# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, fields, models


class TodoTaskStage(models.Model):
    _description = 'To-do Stage'
    _name = 'clv.todo.task.stage'
    _order = 'sequence,name'
    _rec_name = 'name'  # the default

    name = fields.Char(
        string='Name',
        copy=False,
        default='New',
        groups='base.group_user,base.group_no_one',
        help='The title for the stage.',
        index=True,
        readonly=False,
        required=True,
        states={'done': [('readonly', False)]},
        translate=True,
    )

    desc = fields.Text(string='Description')
    state = fields.Selection(
        [('draft', 'New'),
         ('open', 'Started'),
         ('done', 'Closed')
         ], string='State', default='draft', readonly=True, required=True
        # selection_add= When extending a Model, adds items to selection list
    )
    docs = fields.Html(string='Documentation')

    sequence = fields.Integer(string='Sequence')
    perc_complete = fields.Float(string='% Complete', digits=(3, 2))

    date_effective = fields.Date(string='Effective Date')
    date_created = fields.Datetime(
        string='Create Date and Time',
        default=lambda self: fields.Datetime.now())

    fold = fields.Boolean(string='Folded?')
    image = fields.Binary(string='Image')

    task_ids = fields.One2many(
        comodel_name='clv.todo.task',
        inverse_name='stage_id',
        string='Tasks in this stage')


class TodoTask(models.Model):
    _inherit = 'clv.todo.task'

    stage_id = fields.Many2one(comodel_name='todo.task.stage', string='Stage')

    state = fields.Selection(
        related='stage_id.state',
        string='Stage State',
        store=True,  # optional
    )

    stage_fold = fields.Boolean(
        string='Stage Folded?',
        compute='_compute_stage_fold',
        search='_search_stage_fold',
        inverse='_write_stage_fold',
        store=False,  # the default
    )

    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        for todo in self:
            todo.stage_fold = todo.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        for todo in self:
            todo.stage_id.fold = todo.stage_fold
