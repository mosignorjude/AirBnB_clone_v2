#!/usr/bin/python3
"""
Fabric script
 - that generates a .tgz archive
 - distributes an archive to your web servers, using the function do_deploy

"""
# imports necessary modules
from fabric.api import local, runs_once, task, env, put, run
from datetime import datetime
import os

# env.user = "ubuntu"
env.hosts = ['18.210.14.237', '54.237.112.158']


@task
@runs_once
def do_pack():
    """ archives the static files. """
    # get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = "web_static_{}.tgz".format(timestamp)
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    file_dir = "versions/{}".format(filename)
    command = 'tar -czvf {} web_static'.format(file_dir)
    output = ''
    try:
        print("Loading 1-pack_web_static.py 3")
        print("Packing web_static to {}".format(file_dir))
        local(command)
        output = file_dir
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = ''
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("sudo mkdir -p {}".format(folder_path))
        run('sudo tar -xzvf /tmp/{} -C {}'.format(file_name, folder_path))
        run('sudo rm -rf /tmp/{}'.format(file_name))
        run("sudo mv {}web_static/* {}".format(folder_path, folder_path))
        run("sudo rm -rf {}web_static".format(folder_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success
