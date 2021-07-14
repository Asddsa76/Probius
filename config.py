import os
from configparser import ConfigParser

from pathlib import Path

root = os.path.abspath(os.curdir)
path = Path(root.replace(os.sep, "/") + "/config.ini")
config = ConfigParser()
config.read(path)

servers = []
for entry in config["Servers"]:
    servers.append(int(config["Servers"][entry]))
    
owner = config.getint("Client", "Owner")
prefix = config.get("Client", "Prefix")
token = os.getenv(config.get("Client", "Token"))