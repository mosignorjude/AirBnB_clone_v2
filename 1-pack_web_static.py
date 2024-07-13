#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
"""
# imports necessary modules
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """ archives the static files. """
    # get current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = f"web_static_{timestamp}.tgz"
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    file_dir = f"versions/{filename}"
    command = f'tar -czvf {file_dir} web_static'
    output = ''
    try:
        print("Packing web_static to {}".format(file_dir))
        local(command)
        output = file_dir
        size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, size))
    except Exception:
        output = None
    return output
