#coding=utf-8
# 
# Author:       jingqq5210@gmail.com
# 
# Created Time: Wed 27 Mar 2013 11:02:32 PM CST
# 
# FileName:     indicator.py
# 
# Description:  
# 
# ChangeLog:


import sys, time, os

try:
    import pexpect
except ImportError:
    print """
        You must install pexpect module
    """
    sys.exit(1)


class SSH_Dynamic_Tunel:
    ""
    def __init__(self, user, host, password=None, dport=7070):
        self.user = user
        self.host = host
        self.password = password
       
        command = "ssh %s@%s -N -D %d" %(user, host, dport)

        self.expects = [
                'authenticity', # TODO what's this?
                'password:', # ask for password
                '@@@@@@@@@@', # identify changed
                'continue connecting (yes/no)?', # confirm
                'Write failed: Broken pipe', # proberly network error, retry
                'SSH permission denied (publickey)', # password or private key error, stop
                '$', # success, TODO complete more possibility
                pexpect.EOF, # except
                pexpect.TIMEOUT # except
                ]
        self.server = pexpect.spawn(command)
        while True:
            self._watch_server()
            time.sleep(3)
    
    def _watch_server(self):
        #wathch = -1

        watch = self.server.expect(self.expects, 3)
        if watch == 0:
            self.server.sendline('yes')
            watch = self.server.expect(self.expects)

        if watch == 1:
            if not self.password:
                print("no password\n")
                self.server.kill(0)

        if watch == 2:
            print(self.server.read())
            self.server.kill(1)

        if watch == 3:
            self.server.sendline('yes')
            watch = self.server.expect(self.expects)

        if watch == 4:
            self.server = pexpect.spawn(command)
            watch = self.server.expect(self.expects)

        if watch == 5:
            print(self.server.read())
            self.server.kill(2)
        if watch == 6:
            print('success')
            try:
                print(self.server.read()) 
                # to clear previous expet
                # TODO try to use a better way if U kown please DO tell me by E-mail

            except:
                pass
        if watch == 8:
            print('timeout')
            if self.server.isalive():
                # TODO update living status.
                print('living')
            else:
                print('dead')
                # TODO some thing deal with
            try:
                self.server.read() # TODO try not to use try
            except:
                pass

            #self._watch_server()



            


        
        
