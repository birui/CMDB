#coding=utf-8
from xmlrpclib import ServerProxy, Fault
from urlparse import urlparse

class Server(object):
    def __init__(self, connection_string):
        self.name = urlparse(connection_string).hostname
        self.connection = ServerProxy(connection_string)
        self.dic = {}
        # self.id = id

    def refresh(self):
        # print 'test'
        for i in self.connection.supervisor.getAllProcessInfo():

            self.dic["%s:%s" % (i['group'], i['name'])] = i 

            # self.dic['statename']=i['statename']
            # self.dic['description']=i['description']
            # self.dic['name']=i['name']
            # self.dic['logfile']=i['logfile']
            # print self.dic["%s:%s" % (i['group'], i['name'])]['description']
            # print self.dic.keys()
            # print self.dic.values()

    def stop(self, name):
        try:
            return self.connection.supervisor.stopProcess(name)
        except Fault, e:
            if e.faultString.startswith('NOT_RUNNING'):
                return False
            raise

    def start(self, name):
        try:
            return self.connection.supervisor.startProcess(name)
        except Fault, e:
            if e.faultString.startswith('ALREADY_STARTED'):
                return False
            raise

    def start_all(self):
        return self.connection.supervisor.startAllProcesses()

    def restart(self, name):
        self.stop(name)
        return self.start(name)

#======test========

# test = Server('http://192.168.11.10:8899')
# test.refresh()
# test.stop('beanstalk-11304')

# stat = test.dic
# # statues = stat.values()
# testkey = stat.keys()

# for i in testkey:
#     print stat[i]['description']



