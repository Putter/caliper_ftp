#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

import os
import time
from Tkinter import *
import ttk
import threading
from subprocess import Popen, PIPE

class RunTest(threading.Thread):
    def __init__(self, run_command):
        threading.Thread.__init__(self)
        self.command = run_command

    def exec_log(self,command):
        print command
        try:
            if (command != ""):
                adb_pipe = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=1, shell=True)
                print adb_pipe
                for line in iter(adb_pipe.stdout.readline, ''):
                    print line.rstrip()
                    display_line(line)
        except OSError, e:
            display_line(e)

    def run(self):
        display_line(self.command)
        print os.getcwd()
        script_path = os.path.join(os.getcwd(), 'utils/automation_scripts/Scripts')
        os.chdir(script_path)
        print os.getcwd()
        self.exec_log(self.command)
        self.exec_log('scp %s@%s:~/target_dependency_dir/target_dependency_output_summary.txt target_dependency_output_summary.txt'%(target_user_value, target_ip_value))


def run():
    # get weight value
    global target_user_value, target_ip_value
    package_installation_choice_value = package_installation_choice.get()
    target_user_value = target_user.get()
    target_ip_value = target_ip.get()
    target_password_value = target_password.get()
    disk_name_value = disk_name.get()
    run_command = './target_dependency.exp' + ' ' + package_installation_choice_value + ' ' + target_user_value + ' ' + target_ip_value + ' ' + target_password_value + ' ' + disk_name_value
    #Thread
    Thread_test = RunTest(run_command)
    Thread_test.start()


master = Tk()
var = IntVar()
master.title('Install target')
Label(master, text="package_installation_choice: ").grid(sticky=W)
Label(master, text="target_user: ").grid(sticky=W)
Label(master, text="target_ip: ").grid(sticky=W)
Label(master, text="target_password: ").grid(sticky=W)
Label(master, text="disk_name: ").grid(sticky=W)

#value weight
cmbEditComboList = ['y','n']
package_installation_choice = ttk.Combobox(master, values=cmbEditComboList, width=29)
target_user = Entry(master, width=30)
target_ip = Entry(master, width=30)
target_password = Entry(master, width=30)
disk_name = Entry(master, width=30)
#weight layout
package_installation_choice.grid(row=0, column=1, sticky=W)
target_user.grid(row=1, column=1, sticky=W)
target_ip.grid(row=2, column=1, sticky=W)
target_password.grid(row=3, column=1, sticky=W)
disk_name.grid(row=4, column=1, sticky=W)

#run button
runbutton = Button(master, text='Run', command=run)
runbutton.grid(row=6, column=2)

#display exce log
display = Text(master, height=15, wrap=WORD)
def display_line(line):
    display.grid(row=7, column=0, columnspan=3, rowspan=3, sticky=W+E+N+S)
    display.insert(INSERT, "%s\n" % line)
    display.see(END)
    display.update()
#loop tk
mainloop()


