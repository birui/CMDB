#!/usr/bin/env python
# coding=utf-8
# 指定host_list，playbook_path，remote_user，variable_manager.extra_vars
import os
import sys
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

variable_manager = VariableManager()
loader = DataLoader()
inventory = Inventory(loader=loader, variable_manager=variable_manager,
                      host_list='/Users/admin/python/ENV2.7/coohua_CMDB/CMDB/scripts/playbooks/hosts')
playbook_path = '/Users/admin/python/ENV2.7/coohua_CMDB/CMDB/scripts/playbooks/test.yml'
if not os.path.exists(playbook_path):
    print '[INFO] The playbook does not exist'
    sys.exit()
Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                                 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user',
                                 'verbosity', 'check'])
options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None,
                  forks=100, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                  sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root',
                  verbosity=None, check=False)
variable_manager.extra_vars = {'hosts': 'asp'}  # This can accomodate various other command line arguments.`
passwords = {}
pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                        loader=loader, options=options, passwords=passwords)
results = pbex.run()
