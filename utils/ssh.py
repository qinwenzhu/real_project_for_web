#!/usr/bin/env python3

import contextlib
import os
import paramiko
from scp import SCPClient


class SSH(object):
    """ Basic methods for SSH operations.

    connect_to_server: connect to server.
    execute_command: execute command after connecting to server.

    Attributes:
        config: A dictionary of ssh settings.

    """

    def __init__(self, **config):
        self.config = config

    @contextlib.contextmanager
    def connect_to_server(self):
        """Connect to server.

        Connect to server according to initialized configuration.

        Returns:
            A client of connection to server.

        Raises:
            paramiko.SSHException: An error occurred connecting to server.
        """
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(**self.config)
            yield client
        except paramiko.SSHException as error:
            print(f"Unable to establish SSH connection: {error}")
        finally:
            client.close()

    def execute_command(self, command):
        """Execute command on server

        Execute command on server.

        Args:
            command: A single line shell code.
        """
        with self.connect_to_server() as ssh:
            _, stdout, _ = ssh.exec_command(command)
            channel = stdout.channel
            status = channel.recv_exit_status()
            if (status == 0):
                # print(f'Command "{command}" has been executed successfully.')
                return stdout.read().decode("utf-8")
            else:
                # print(f'Command "{command}" failed to be executed!')
                return None

    def scp_local_file(self, file_name, source, destination):
        """Copy local file to server

        Copy local file in specific path to specific path on server.

        Args:
            file_name: name of copying local file.
            source: path of copying local file.
            destination: path on server.
        """
        source_path = os.path.join(source, file_name)
        destination_path = os.path.join(destination, file_name)
        destination_host = self.config.get('hostname')

        with self.connect_to_server() as ssh:
            client = SCPClient(ssh.get_transport())
            if os.path.isfile(source_path):
                client.put(source_path, destination_path)
                print(
                    f'Local file "{file_name}" in "{source}" has been copyed to {destination_host} in "{destination}"!')
            else:
                print(f'Local file "{file_name}" is not found in "{source}"!')
