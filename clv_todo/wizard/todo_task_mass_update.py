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
from odoo import exceptions
import logging


_logger = logging.getLogger(__name__)


class TodoTaskMassUpdate(models.TransientModel):
    _name = 'clv.todo.task.mass_update'
    _description = 'To-do Task Mass Assignment'

    todo_task_ids = fields.Many2many(
        comodel_name='clv.todo.task',
        string='To-do Tasks')
    new_deadline = fields.Date(string='Deadline to Set')
    new_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible to Set')

    @api.model
    def default_get(self, field_names):
        defaults = super(TodoTaskMassUpdate, self).default_get(field_names)
        defaults['todo_task_ids'] = self.env.context['active_ids']
        return defaults

    @api.multi
    def do_count_tasks(self):
        Task = self.env['clv.todo.task']
        count = Task.search_count([('is_done', '=', False)])
        raise exceptions.Warning(
            'There are %d active tasks.' % count)

    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # this model
            'res_id': self.id,  # the current wizard record
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new'}

    @api.multi
    def do_populate_tasks(self):
        self.ensure_one()
        Task = self.env['clv.todo.task']
        all_tasks = Task.search([('is_done', '=', False)])
        # Fill the wizard Task list with all tasks
        self.todo_task_ids = all_tasks
        # reopen wizard form on same wizard record
        return self._reopen_form()

    @api.multi
    def do_mass_update(self):
        self.ensure_one()
        if not (self.new_deadline or self.new_user_id):
            raise exceptions.ValidationError('No data to update!')
        # Logging debug messages
        _logger.info(
            'Mass update on Todo Tasks %s',
            self.todo_task_ids.ids)
        vals = {}
        if self.new_deadline:
            vals['date_deadline'] = self.new_deadline
        if self.new_user_id:
            vals['user_id'] = self.new_user_id.id
        # Mass write values on all selected tasks
        if vals:
            _logger.info('>>>>> vals: %s, todo_task_ids: %s', vals, self.todo_task_ids)
            self.todo_task_ids.write(vals)
        return True
