#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

import os
import sys
import pexpect
import subprocess
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

class download():
    def __init__(self):
        pass

    '''creat caliper_outpt folder for collect caliper log and result'''
    def create_dir(self, mode=0755):
        CALIPER_TMP_DIR = os.path.join(os.environ['HOME'], 'caliper_output')
        if not os.path.exists(CALIPER_TMP_DIR):
            os.makedirs(CALIPER_TMP_DIR, mode)

    '''check os version, caliper only support 16.04 and 14.04'''
    def check_version(self):
        version = os.popen('cat /etc/issue').read()
        if '16.04' or '14.04' in version:
            pass
        else:
            print 'fail'

    '''download caliper code'''
    def clone(self):
        os.system('git clone https://github.com/TSestuary/caliper.git')

    '''install caliper'''
    def install_caliper(self):
        os.chdir('caliper')
        os.system('git branch -a')
        os.popen('git checkout capliper_deploy_gui')
        caliper_install = pexpect.spawn('sudo python setup.py install', timeout=5)
        install_caliper = caliper_install.expect(["[sudo]", pexpect.TIMEOUT])
        if install_caliper == 0:
            try:
                caliper_install.sendline(sys.argv[1])
                print caliper_install.readlines()
            except pexpect.EOF , e:
                 print e
        elif install_caliper == 1:
            pass

    def judge_tool_installed(self, tool):
        try:
            output = subprocess.Popen('which %s'%tool, shell=True, stdout=subprocess.PIPE)
        except Exception:
            return 0
        else:
            if output.stdout.readlines():
                return 1
            else:
                return 0

    def judge_dependent_installed(self, tool):
        try:
            output = os.popen("dpkg-query -W -f='${Status}' %s | grep -c "+'"ok installed"'%tool).read()
        except Exception:
            return 0
        else:
            if '0' in output:
                return 0
            else:
                return 1

    def install_python(self):
        os.system('sudo apt-get update')
        os.system('sudo apt-get -f install python-dev')

    def install_git(self):
        os.system('sudo apt-get update')
        os.system('sudo apt-get -f install git')

    def run(self):
        version = os.popen('cat /etc/issue').read()
        print version
        if '16.04' or '14.04' in version:
            print version
            tool_list = ['python', 'git']
            for tool in tool_list:
                flag = self.judge_tool_installed(tool)
                print flag
                if flag != 1:
                    try:
                        update_apt = pexpect.spawn('sudo apt-get update', timeout=5)
                        input_password = update_apt.expect(["[sudo]", pexpect.TIMEOUT])
                        if input_password == 0:
                            try:
                                update_apt.sendline(sys.argv[1])
                            except pexpect.EOF, e:
                                print e
                        elif input_password == 1:
                            pass
                        if tool == 'python':
                            os.system('sudo apt-get -f install python-dev')
                        else:
                            os.system('sudo apt-get -f install %s'%tool)
                    except OSError,e:
                        print e
                        # sys.exit()
            self.clone()
            self.install_caliper()
        else:
            print 'fail'


if __name__ == '__main__':
    download = download()
    download.run()