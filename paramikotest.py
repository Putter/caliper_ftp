#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
import paramiko
import select


server = "192.168.65.108"
port = 22
name = "test"
password = "123"


def main():
    client = paramiko.SSHClient()
    client.load_system_host_keys()

    client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    client.connect(server, port, name, password)

    channel = client.get_transport().open_session()
    channel.exec_command("caliper -w 2>&1")

    while True:
        if channel.exit_status_ready():
            break

        r, w, x = select.select([channel], [], [])
        if len(r) > 0:
            print channel.recv(1024)

if __name__ == "__main__":
    main()