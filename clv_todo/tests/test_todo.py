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

import logging

from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class TestTodo(TransactionCase):

    def setUp(self, *args, **kwargs):
        result = super(TestTodo, self).setUp(*args, **kwargs)
        user_demo = self.env.ref('base.user_demo')
        self.env = self.env(user=user_demo)
        return result

    def test_create(self):
        "Create a simple Todo"
        TodoTask = self.env['clv.todo.task']
        task = TodoTask.create({'name': 'Test Task'})
        self.assertEqual(task.is_done, False)
        _logger.info(u'%s %s', '>>>>>>>>>>', 'Test was succesfull!')

    def test_clear_done(self):
        "Clear Done sets to non active"
        TodoTask = self.env['clv.todo.task']
        task = TodoTask.create({'name': 'Test Task', 'is_done': True})
        task.do_clear_done()
        self.assertFalse(task.active)
        _logger.info(u'%s %s', '>>>>>>>>>>', 'Test was succesfull!')

    def test_record_rule(self):
        "Test per user record rules"
        TodoTask = self.env['clv.todo.task']
        task = TodoTask.sudo().create({'name': 'Admin Task'})
        with self.assertRaises(AccessError):
            TodoTask.browse([task.id]).name
        _logger.info(u'%s %s', '>>>>>>>>>>', 'Test was succesfull!')
