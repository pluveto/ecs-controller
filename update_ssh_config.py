
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import ecs
from dotenv import load_dotenv

load_dotenv()

host = "lbdev-ali-hk"
host_name = ecs.Server().public_ip_address
user = "root"
identity_file = "~/.ssh/id_rsa"
ssh_config_path = os.path.expanduser("~") + "/.ssh/config"


def build_config(host, host_name, user, identity_file):
    return f"""Host {host}
    HostName {host_name}
    User {user}
    IdentityFile {identity_file}"""

if host_name == None or len(host_name) == 0:
    ecs.logger.error("ip address is empty")
    exit(1)

ssh_config_text = open(ssh_config_path, 'r', encoding="utf-8").read()

start_delim = "# START " + host
end_delim = "# END " + host
pattern = re.compile(start_delim + r"\n([\w\W]*)" + end_delim + "\n", re.DOTALL)

new_config = build_config(host, host_name, user, identity_file)
new_config = start_delim + "\n" + new_config + "\n" + end_delim + "\n"

ssh_config_text, replace_count = re.subn(pattern, new_config, ssh_config_text)

if replace_count == 0:
    ssh_config_text = ssh_config_text + new_config

# write back
open(ssh_config_path, 'w', encoding="utf-8").write(ssh_config_text)
