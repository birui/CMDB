#!/usr/bin/python
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

# Creat a callback object so we can capture the output
class ResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok     = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

class playansible(object):
    """docstring for playansible"""
    def __init__(self, host, order):
        super(playansible, self).__init__()
        self.host = host
        self.order = order


    def runcmd(self):
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'remote_user',
                'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])

        # initialize needed objects
        variable_manager = VariableManager()
        loader = DataLoader()
        options = Options(connection='smart', module_path='/usr/local/bin/ansible', forks=100,
                remote_user='coohua', private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                become_user=None, verbosity=None, check=False)

        passwords = dict()

        # create inventory and pass to var manager
        inventory = Inventory(loader=loader, variable_manager=variable_manager,host_list='/Users/admin/python/ENV2.7/coohua_CMDB/CMDB/scripts/playbooks/hosts')
        variable_manager.set_inventory(inventory)

        # create play with tasks
        play_source =  dict(
                name = "Ansible Play",
                hosts = self.host,
                gather_facts = 'no',
                tasks = [ dict(action=dict(module='command', args=dict(cmd=self.order))) ]
            )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # actually run it
        tqm = None
        callback = ResultsCollector()
        try:
            tqm = TaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=options,
                    passwords=passwords,
                )
            tqm._stdout_callback = callback
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()



        print "===================== UP =========================>>"

        for host, result in callback.host_ok.items():
            return '{} ==>> {}'.format(host, result._result['stdout'])

        # print "xxxxxxxxxxxxxxxxxxxxx FAILED  xxxxxxxxxxxxxxxxxxxx!!"

        # for host, result in callback.host_failed.items():
        #     print '{} ==>> {}'.format(host, result._result['msg'])

        # print "====================== DOWN ======================>>"
        # for host, result in callback.host_unreachable.items():
        #     print '{} ==>> {}'.format(host, result._result['msg'])
        


# if __name__ == '__main__':
#     main()

# runansible = playansible('192.168.11.11','/app/coohua/publish/altair/get.sh 1.1')
# runansible.runcmd()
