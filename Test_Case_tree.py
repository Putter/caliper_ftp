import os
import Tkinter as tk
import ttk


class App(object):
    def __init__(self, master, path):
        self.nodes = dict()
        frame = tk.Frame(master)
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Project tree', anchor='w')

        self.tree.grid()
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        frame.grid()

        abspath = os.path.abspath(path)
        self.insert_node('', abspath, abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        # if os.path.isdir(abspath):
        self.nodes[node] = abspath
        self.tree.insert(node, 'end')

    def open_node(self, event):
        item = self.tree.selection()[0]
        print "you clicked on ", self.tree.item(item, "values")
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                print '**********%s*****************'%p
                # if not os.path.isdir(p):
                #     f = open(p)
                #     print p
                self.insert_node(node, p, os.path.join(abspath, p))

# Install caliper
#         display_line(host_text, 'Install caliper......')
#         setup.run()
        # caliper_install = pexpect.spawn('sudo python setup.py install', timeout=5)
        # install_caliper = caliper_install.expect(["[sudo]", pexpect.TIMEOUT])
        # if install_caliper == 0:
        #     print 'password'
        #     try:
        #         caliper_install.sendline(host_pc_password_value)
        #         display_line(host_text, caliper_install.after)
        #     except pexpect.EOF , e:
        #         display_line(host_text, e)
        #
        # elif install_caliper == 1:
        #     pass

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root, path='/home/hansy/caliper_gui/test_cases_cfg')
    root.mainloop()