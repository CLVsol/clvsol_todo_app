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
