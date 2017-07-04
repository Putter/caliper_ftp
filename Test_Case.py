#!/usr/bin/env python
#-*- encoding:UTF-8 -*-

from Tkinter import *


def donothing():
    filewin = Toplevel(master)
    button = Button(filewin, text="Do nothing button")
    button.pack()


master = Tk()
menubar = Menu(master)

#First menu
dimension_menu = Menu(menubar, tearoff=0)
dimension_menu.LATENCY = Menu(dimension_menu)
dimension_menu.MEMORY = Menu(dimension_menu)
dimension_menu.APPLICATION = Menu(dimension_menu)
dimension_menu.CPU_MULTICORE = Menu(dimension_menu)
dimension_menu.STORAGE = Menu(dimension_menu)
dimension_menu.CPU_SINCORE = Menu(dimension_menu)
dimension_menu.ALGORITHM = Menu(dimension_menu)
dimension_menu.NETWORK = Menu(dimension_menu)


dimension_menu.APPLICATION.TOOL = Menu(dimension_menu.APPLICATION)
dimension_menu.CPU_MULTICORE.TOOL = Menu(dimension_menu.CPU_MULTICORE)
dimension_menu.STORAGE.TOOL = Menu(dimension_menu.STORAGE)
dimension_menu.CPU_SINCORE.TOOL = Menu(dimension_menu.CPU_SINCORE)
dimension_menu.ALGORITHM.TOOL = Menu(dimension_menu.ALGORITHM)


#LATENCY menu
dimension_menu.LATENCY.Lmbench = Menu(dimension_menu.LATENCY)
dimension_menu.LATENCY.Lmbench.Context_Switch = Menu(dimension_menu.LATENCY.Lmbench)
dimension_menu.LATENCY.Lmbench.File_Latency = Menu(dimension_menu.LATENCY.Lmbench)
dimension_menu.LATENCY.Lmbench.Process_Latency = Menu(dimension_menu.LATENCY.Lmbench)
dimension_menu.LATENCY.add_cascade(label='Lmbench', menu=dimension_menu.LATENCY.Lmbench)

dimension_menu.LATENCY.Lmbench.add_cascade(label='Context Switch', menu=dimension_menu.LATENCY.Lmbench.Context_Switch)
dimension_menu.LATENCY.Lmbench.add_cascade(label='File/VM Latency', menu=dimension_menu.LATENCY.Lmbench.File_Latency)
dimension_menu.LATENCY.Lmbench.add_cascade(label='Process Latency', menu=dimension_menu.LATENCY.Lmbench.Process_Latency)


dimension_menu.LATENCY.Lmbench.Context_Switch.add_checkbutton(label='Case1')
dimension_menu.LATENCY.Lmbench.Context_Switch.add_checkbutton(label='Case2')
dimension_menu.LATENCY.Lmbench.Context_Switch.add_checkbutton(label='Case3')


# dimension_menu.LATENCY.Lmbench.add_checkbutton(label='Context Switch')
# dimension_menu.LATENCY.Lmbench.add_checkbutton(label='File/VM Latency')
# dimension_menu.LATENCY.Lmbench.add_checkbutton(label='Process Latency')

#NETWORK menu
dimension_menu.NETWORK.Netperf = Menu(dimension_menu.NETWORK)
dimension_menu.NETWORK.Iperf = Menu(dimension_menu.NETWORK)
dimension_menu.NETWORK.Qperf = Menu(dimension_menu.NETWORK)
dimension_menu.NETWORK.Lmbench = Menu(dimension_menu.NETWORK)
dimension_menu.NETWORK.add_cascade(label='Netperf', menu=dimension_menu.NETWORK.Netperf)
dimension_menu.NETWORK.add_cascade(label='Iperf', menu=dimension_menu.NETWORK.Iperf)
dimension_menu.NETWORK.add_cascade(label='Qperf', menu=dimension_menu.NETWORK.Qperf)
dimension_menu.NETWORK.add_cascade(label='Lmbench', menu=dimension_menu.NETWORK.Lmbench)

#MEMERY menu
dimension_menu.MEMORY.Cachebench = Menu(dimension_menu.MEMORY)
dimension_menu.MEMORY.Tinymembench = Menu(dimension_menu.MEMORY)
dimension_menu.MEMORY.Lmbench = Menu(dimension_menu.MEMORY)
#Tools
dimension_menu.MEMORY.add_cascade(label='Cachebench', menu=dimension_menu.MEMORY.Cachebench)
dimension_menu.MEMORY.add_cascade(label='Tinymembench', menu=dimension_menu.MEMORY.Tinymembench)
dimension_menu.MEMORY.add_cascade(label='Lmbench', menu=dimension_menu.MEMORY.Lmbench)
#Cachebench case
dimension_menu.MEMORY.Cachebench.add_checkbutton(label='Bandwidth (cachebench) ')
dimension_menu.MEMORY.Cachebench.add_checkbutton(label='Local Speed')
#Tinymembench case
dimension_menu.MEMORY.Tinymembench.add_checkbutton(label='Tiny Bandwidth')
dimension_menu.MEMORY.Tinymembench.add_checkbutton(label='Tiny Latency')
# Lmbench case
dimension_menu.MEMORY.Lmbench.add_checkbutton(label='lmbench stream bandwidth V1')
dimension_menu.MEMORY.Lmbench.add_checkbutton(label='lmbench stream bandwidth V2')
dimension_menu.MEMORY.Lmbench.add_checkbutton(label='lmbench local bandwidth - 1 ~ - 64 core')
dimension_menu.MEMORY.Lmbench.add_checkbutton(label='lmbench cross bandwidth - 1 ~ - 64 core')
dimension_menu.MEMORY.Lmbench.add_checkbutton(label='lmbench local latency - 1 ~ -  64 core')
dimension_menu.MEMORY.Lmbench.add_checkbutton(label='lmbench cross latency - 1 ~ - 64 core')


#second menu
dimension_menu.add_cascade(label='LATENCY',menu=dimension_menu.LATENCY)
dimension_menu.add_cascade(label='MEMORY',menu=dimension_menu.MEMORY)
dimension_menu.add_cascade(label='APPLICATION',menu=dimension_menu.APPLICATION)
dimension_menu.add_cascade(label='CPU_MULTICORE',menu=dimension_menu.CPU_MULTICORE)
dimension_menu.add_cascade(label='STORAGE',menu=dimension_menu.STORAGE)
dimension_menu.add_cascade(label='CPU_SINCORE',menu=dimension_menu.CPU_SINCORE)
dimension_menu.add_cascade(label='ALGORITHM',menu=dimension_menu.ALGORITHM)
dimension_menu.add_cascade(label='NETWORK',menu=dimension_menu.NETWORK)


menubar.add_cascade(label="Dimension", menu=dimension_menu)


case_menu = Menu(menubar, tearoff=0)
case_menu.add_command(label="hardware_info", command=donothing)
case_menu.add_command(label="tinymembench", command=donothing)
case_menu.add_command(label="openssl", command=donothing)
case_menu.add_command(label="coremark", command=donothing)
case_menu.add_command(label="scimark", command=donothing)

menubar.add_cascade(label="Case", menu=case_menu)

master.config(menu=menubar)
master.mainloop()