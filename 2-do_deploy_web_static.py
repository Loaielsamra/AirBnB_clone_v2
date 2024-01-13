#!/usr/bin/python3
"""Fabric script for compressing and deploying a web static package."""
from fabric.api import *
from datetime import datetime
from os import path

# Set the remote server hosts, user, and SSH key file
env.hosts = ['35.175.128.200', '34.229.254.68']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """
    Deploy web files to the server.

    Args:
        archive_path (str): The path to the compressed web static package.

    Returns:
        bool: True if deployment succeeds, False otherwise.
    """
    try:
        # Check if the archive file exists
        if not path.exists(archive_path):
            return False

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the target directory on the server using the timestamp
        timestamp = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(timestamp))

        # Uncompress the archive and delete the .tgz file
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'
            .format(timestamp, timestamp))

        # Remove the uploaded archive from the /tmp/ directory
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move the contents into the host's web_static directory
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* '
            '/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove the extraneous web_static directory
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'
            .format(timestamp))

        # Delete the pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish the symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'
            .format(timestamp))

    except Exception as e:
        # Return False on failure and print the exception
        print(e)
        return False

    # Return True on successful deployment
    return True
