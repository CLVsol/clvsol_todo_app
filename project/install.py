# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2016-Today  Carlos Eduardo Vercelino - CLVsol
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

import images

from odoo_client.cli import *
from odoo_client.db import *


class TodoApp(object):

    def __init__(
        self,

        server='http://localhost:8069',

        CompanyName='To-do App',
        Company_image=images.Company_image,
        website='https://github.com/CLVsol',

        admin_user_pw='admin',
        admin_user_email='admin@clvsol.com',
        Administrator_image=images.Administrator_image,

        demo_user_name='Demo User',
        demo_user='demo',
        demo_user_pw='demo',
        demo_user_email='demo.user@clvsol.com',
        Demo_User_image=images.Demo_User_image,

        data_admin_user_name='Data Administrator',
        data_admin_user='data.admin',
        data_admin_user_pw='data.admin',
        data_admin_user_email='data.admin@clvsol.com',
        DataAdministrator_image=images.DataAdministrator_image,

        dbname='todo_app',

        lang='pt_BR',
        tz='America/Sao_Paulo',

        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
    ):

        self.server = server

        self.CompanyName = CompanyName
        self.Company_image = Company_image
        self.website = website

        self.admin_user_pw = admin_user_pw
        self.admin_user_email = admin_user_email
        self.Administrator_image = Administrator_image

        self.demo_user_name = demo_user_name
        self.demo_user = demo_user
        self.demo_user_pw = demo_user_pw
        self.demo_user_email = demo_user_email
        self.Demo_User_image = Demo_User_image

        self.data_admin_user_name = data_admin_user_name
        self.data_admin_user = data_admin_user
        self.data_admin_user_pw = data_admin_user_pw
        self.data_admin_user_email = data_admin_user_email
        self.DataAdministrator_image = DataAdministrator_image

        self.dbname = dbname

        self.lang = lang
        self.tz = tz

        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade

    def install_upgrade_module(self, module, upgrade, group_name_list=[]):

        print('\n%s%s' % ('--> ', module))
        if module in self.modules_to_upgrade:
            new_module = db.module_install_upgrade(module, True)
        else:
            new_module = db.module_install_upgrade(module, upgrade)

        if new_module and group_name_list != []:

            user_name = 'Administrator'
            print('\n%s%s (%s) %s' % ('--> ', module, user_name, group_name_list))
            db.user_groups_setup(user_name, group_name_list)

            user_name = 'Data Administrator'
            print('\n%s%s (%s) %s' % ('--> ', module, user_name, group_name_list))
            db.user_groups_setup(user_name, group_name_list)

        return new_module

    def install(self):

        global upgrade

        print('--> create_database()')
        newDB = db.create()
        if newDB:
            print('\n--> newDB: ', newDB)
            print('\n--> my_company_setup()')
            db.my_company_setup(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            db.administrator_setup(self.admin_user_email, self.Administrator_image)
            print('\n--> demo_user_setup()')
            db.demo_user_setup(
                self.demo_user_name, self.demo_user_email, self.CompanyName,
                self.demo_user, self.demo_user_pw, self.Demo_User_image
            )
            print('\n--> data_administrator_user_setup()')
            db.data_administrator_user_setup(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )
        else:
            print('\n--> newDB: ', newDB)
            client = erppeek.Client(
                server=self.server,
                db=self.dbname,
                user='admin',
                password=self.admin_user_pw
            )
            print('\n--> Update Modules List"')
            IrModuleModule = client.model('ir.module.module')
            IrModuleModule.update_list()

        # ############################################################################################
        #
        # Odoo Addons
        #
        # ############################################################################################

        group_names = []
        self.install_upgrade_module('contacts', False, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons
        #
        # ############################################################################################

        # group_names = []
        # install_upgrade_module('clv_disable_web_access', upgrade, group_names)

        group_names = [
            'User (Base)',
            'Super User (Base)',
            'Annotation User (Base)',
            'Register User (Base)',
            'Log User (Base)',
            'Manager (Base)',
            'Super Manager (Base)',
        ]
        self.install_upgrade_module('clv_base', self.upgrade_all, group_names)

        group_names = [
            'User (Global Tag)',
            'Manager (Global Tag)',
            'Super Manager (Global Tag)',
        ]
        self.install_upgrade_module('clv_global_tag', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol To-Do Applicatio
        #
        # ############################################################################################

        group_names = [
            'User (To-Do)',
            'Manager (To-Do)',
            'Super Manager (To-Do)',
        ]
        self.install_upgrade_module('clv_todo', self.upgrade_all, group_names)


if __name__ == '__main__':

    from time import time

    cli = CLI(
        super_user_pw='*',
        admin_user_pw='*',
        data_admin_user_pw='*',
        dbname='*',
        demo_data=False,
        lang='pt_BR',
        tz='America/Sao_Paulo',
    )
    cli.argparse_db_setup()

    todo_app = TodoApp(
        # super_user_pw=cli.super_user_pw,
        admin_user_pw=cli.admin_user_pw,
        demo_user_pw='demo',
        data_admin_user_pw=cli.data_admin_user_pw,
        demo_data=cli.demo_data,
        upgrade_all=cli.upgrade_all,
        modules_to_upgrade=cli.modules_to_upgrade,
        lang=cli.lang,
        tz=cli.tz
    )

    db = DB(
        server=cli.server,
        super_user_pw=cli.super_user_pw,
        admin_user_pw=cli.admin_user_pw,
        data_admin_user_pw=cli.data_admin_user_pw,
        dbname=cli.dbname,
        demo_data=cli.demo_data,
        lang=cli.lang,
        tz=cli.tz
    )

    start = time()

    print('--> Executing install.py...\n')

    print('--> Executing install()...\n')
    todo_app.install()

    print('\n--> install.py')
    print('--> Execution time:', secondsToStr(time() - start), '\n')
