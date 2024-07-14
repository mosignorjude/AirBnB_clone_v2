#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
"""
from fabric.api import local, runs_once, task
from datetime import datetime
import os
print("Loading 1-pack_web_static.py 1")
# imports necessary modules


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
