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

from openerp import api, fields, models


class TodoTaskCategory(models.Model):
    _description = 'To-do Task Category'
    _name = 'clv.todo.task.category'
    _inherit = 'clv.abstract.category'

    code = fields.Char(string='Category Code', required=False)

    parent_id = fields.Many2one(
        comodel_name='clv.todo.task.category',
        string='Parent Category',
        index=True,
        ondelete='restrict'
    )

    child_ids = fields.One2many(
        comodel_name='clv.todo.task.category',
        inverse_name='parent_id',
        string='Child Categories'
    )

    todo_task_ids = fields.Many2many(
        comodel_name='clv.todo.task',
        relation='clv_todo_task_category_rel',
        column1='category_id',
        column2='todo_task_id',
        string='To-do Tasks'
    )


class TodoTask(models.Model):
    _inherit = "clv.todo.task"

    category_ids = fields.Many2many(
        comodel_name='clv.todo.task.category',
        relation='clv_todo_task_category_rel',
        column1='todo_task_id',
        column2='category_id',
        string='Categories',
        context={},
        domain=[],
        ondelete='restrict'
    )
    category_names = fields.Char(
        string='Category Names',
        compute='_compute_category_names',
        store=True
    )
    category_names_suport = fields.Char(
        string='Category Names Suport',
        compute='_compute_category_names_suport',
        store=False
    )

    @api.depends('category_ids')
    def _compute_category_names(self):
        for r in self:
            r.category_names = r.category_names_suport

    @api.multi
    def _compute_category_names_suport(self):
        for r in self:
            category_names = False
            for category in r.category_ids:
                if category_names is False:
                    category_names = category.complete_name
                else:
                    category_names = category_names + ', ' + category.complete_name
            r.category_names_suport = category_names
            if r.category_names != category_names:
                record = self.env['clv.todo.task'].search([('id', '=', r.id)])
                record.write({'category_ids': r.category_ids})
