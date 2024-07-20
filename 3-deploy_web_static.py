#!/usr/bin/python3
"""
Fabfile to create and distribute an archive to a web server
using the function deploy:
"""
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["18.210.14.237", "54.237.112.158"]


def do_pack():
    """ archives the static files. """
    print("Loading 1-pack_web_static.py 2")
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
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
