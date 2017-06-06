#!/usr/bin/env python
#-*- encoding:UTF-8 -*-
# from subprocess import Popen, PIPE
# import paramiko
#
#
# def connect_to_host(ip, port, name, password):
#     # ssh = paramiko.SSHClient()
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#     ssh.connect("192.168.65.108",22,"test", "123")
#     stdin, stdout, stderr = ssh.exec_command('caliper -w')
#
#
#     print 'test'
#     print stdin.readlines()
#     print stdout.readlines()
#     print stderr.readlines()
#     print 'after'
#
#     # adb_pipe = Popen('ls', stdin=PIPE, stdout=PIPE, bufsize=1)
#     #
#     # for line in iter(adb_pipe.stdout.readline, ''):
#     #     print line
#     ssh.close()
#
# def run_command(command):
#     adb_pipe = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=1)
#     if (command != ""):
#         for line in iter(adb_pipe.stdout.readline, ''):
#             print line
#
# connect_to_host('', '', '', '')

from os.path import abspath, expanduser, isfile
import re
import socket
from threading import Event, Lock

# from .error import GerritError

from paramiko import SSHClient, SSHConfig
from paramiko.ssh_exception import SSHException


def _extract_version(version_string, pattern):
    """ Extract the version from `version_string` using `pattern`.

    Return the version as a string, with leading/trailing whitespace
    stripped.

    """
    if version_string:
        match = pattern.match(version_string.strip())
        if match:
            return match.group(1)
    return ""


class GerritSSHCommandResult(object):
    """ Represents the results of a Gerrit command run over SSH. """

    def __init__(self, command, stdin, stdout, stderr):
        self.command = command
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        return "<GerritSSHCommandResult [%s]>" % self.command


class GerritSSHClient(SSHClient):
    """ Gerrit SSH Client, wrapping the paramiko SSH Client. """

    def __init__(self, hostname, username=None, port=None):
        """ Initialise and connect to SSH. """
        super(GerritSSHClient, self).__init__()
        self.remote_version = None
        self.hostname = hostname
        self.username = username
        self.key_filename = None
        self.port = port
        self.connected = Event()
        self.lock = Lock()

    def _configure(self):
        """ Configure the ssh parameters from the config file. """
        configfile = expanduser("~/.ssh/config")
        if not isfile(configfile):
            print "ssh config file '%s' does not exist" %configfile

        config = SSHConfig()
        config.parse(open(configfile))
        data = config.lookup(self.hostname)
        if not data:
            pass
            # raise GerritError("No ssh config for host %s" % self.hostname)
        if not 'hostname' in data or not 'port' in data or not 'user' in data:
            print "Missing configuration data in %s" % configfile
        self.hostname = data['hostname']
        self.username = data['user']
        if 'identityfile' in data:
            key_filename = abspath(expanduser(data['identityfile'][0]))
            if not isfile(key_filename):
                print "Identity file '%s' does not exist" % key_filename
            self.key_filename = key_filename
        try:
            self.port = int(data['port'])
        except ValueError:
            pass
            # raise GerritError("Invalid port: %s" % data['port'])

    def _do_connect(self):
        """ Connect to the remote. """
        self.load_system_host_keys()
        if self.username is None or self.port is None:
            self._configure()
        try:
            self.connect(hostname = "192.168.65.108",port= 22,username = "test", password ="123",allow_agent=False,look_for_keys=False)
            print 'connect'
            # self.connect(hostname=self.hostname,
            #              port=self.port,
            #              username=self.username,
            #              key_filename=self.key_filename)
        except socket.error as e:
            print "Failed to connect to server: %s" % e

        try:
            version_string = self._transport.remote_version
            pattern = re.compile(r'^.*GerritCodeReview_([a-z0-9-\.]*) .*$')
            self.remote_version = _extract_version(version_string, pattern)
        except AttributeError:
            self.remote_version = None

    def _connect(self):
        """ Connect to the remote if not already connected. """
        if not self.connected.is_set():
            try:
                self.lock.acquire()
                # Another thread may have connected while we were
                # waiting to acquire the lock
                if not self.connected.is_set():
                    self._do_connect()
                    self.connected.set()
            except:
                raise
            finally:
                self.lock.release()

    def get_remote_version(self):
        """ Return the version of the remote Gerrit server. """
        if self.remote_version is None:
            result = self.run_gerrit_command("version")
            version_string = result.stdout.read()
            pattern = re.compile(r'^gerrit version (.*)$')
            self.remote_version = _extract_version(version_string, pattern)
        return self.remote_version

    def get_remote_info(self):
        """ Return the username, and version of the remote Gerrit server. """
        version = self.get_remote_version()
        return (self.username, version)

    def run_gerrit_command(self, command):
        """ Run the given command.

        Make sure we're connected to the remote server, and run `command`.

        Return the results as a `GerritSSHCommandResult`.

        Raise `ValueError` if `command` is not a string, or `GerritError` if
        command execution fails.

        """
        if not isinstance(command, basestring):
            raise ValueError("command must be a string")
        gerrit_command = "gerrit " + command

        self._connect()
        try:
            stdin, stdout, stderr = self.exec_command(gerrit_command,
                                                      bufsize=1,
                                                      timeout=None,
                                                      get_pty=False)

            print stdout.read()

        except SSHException as err:
            pass
            # raise GerritError("Command execution error: %s" % err)
        return GerritSSHCommandResult(command, stdin, stdout, stderr)



if __name__ == "__main__":
    print 'run'
    from paramiko import SSHClient
    c = GerritSSHClient("192.168.65.108","test",22)
    c.run_gerrit_command('ls')