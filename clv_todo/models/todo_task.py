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
from odoo.exceptions import ValidationError
# from odoo.addons.base.res.res_request import referenceable_models


class TodoTask(models.Model):
    _description = 'To-do Task'
    _name = 'clv.todo.task'

    name = fields.Char(
        string='Description',
        help="What needs to be done?",
        required=True
    )
    is_done = fields.Boolean(string='Done')
    date_deadline = fields.Date('Deadline')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        default=lambda self: self.env.user)
    team_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Team'
    )

    active = fields.Boolean(string='Active', default=True)

    @api.multi
    def do_clear_done(self):
        for task in self:
            if task.is_done:
                task.active = False
        return True

    @api.multi
    def write(self, values):
        # Before write logic
        if 'active' not in values:
            values['active'] = True
        # return super(TodoTask, self).write(values) # keeping Python 2 compatibility
        return super().write(values)


class TodoTask_2(models.Model):
    _name = 'clv.todo.task'
    _inherit = ['clv.todo.task', 'mail.thread']

    effort_estimate = fields.Integer()
    name = fields.Char(help="What needs to be done?")

    refers_to = fields.Reference(
        # Set a Selection list, such as:
        [('res.users', 'User'), ('res.partner', 'Partner')],
        # Or use standard "Referencable Models":
        # referenceable_models,
        # 'Refers to',  # string= (title)
    )

    _sql_constraints = [(
        'todo_task_name_unique',
        'UNIQUE (name, active)',
        'Task title must be unique!'
    )]

    @api.constrains('name')
    def _check_name_size(self):
        for todo in self:
            if len(todo.name) < 5:
                raise ValidationError('Title must have 5 chars!')


class TodoTask_3(models.Model):
    _inherit = 'clv.todo.task'

    @api.onchange('user_id')
    def onchange_user_id(self):
        if not self.user_id:
            self.team_ids = None
            return {
                'warning': {
                    'title': 'Responsible User Reset',
                    'message': 'Please choose a new Team.',
                }
            }

    @api.model
    def create(self, vals):
        # Code before create: should use the `vals` dict
        new_record = super().create(vals)
        # Code after create: can use the `new_record` created
        return new_record

    @api.multi
    def write(self, vals):
        # Code before write: can use `self`, with the old values
        super().write(vals)
        # Code after write: can use `self`, with the updated values
        return True


class TodoTask_4(models.Model):
    _inherit = 'clv.todo.task'

    effort_estimate = fields.Integer(string='Effort Estimate')

    user_todo_count = fields.Integer(
        string='User To-Do Count',
        compute='_compute_user_todo_count')

    @api.multi
    def _compute_user_todo_count(self):
        for task in self:
            task.user_todo_count = task.search_count(
                [('user_id', '=', task.user_id.id)])
