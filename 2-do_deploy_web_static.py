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

env.user = "ubuntu"
env.hosts = ['18.210.14.237', '54.237.112.158']


@task
@runs_once
def do_pack():
    """ archives the static files. """
    print("Loading 1-pack_web_static.py 2")
    # get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = f"web_static_{timestamp}.tgz"
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    file_dir = f"versions/{filename}"
    command = f'tar -czvf {file_dir} web_static'
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
    folder_path = f"/data/web_static/releases/{folder_name}/"
    success = False
    try:
        put(archive_path, f"/tmp/{file_name}")
        run("sudo mkdir -p {}".format(folder_path))
        run(f'sudo tar -xzvf /tmp/{file_name} {folder_path}')
        run(f'sudo rm -rf /tmp/{file_name}')
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {folder_path} /data/web_static/current")
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success
