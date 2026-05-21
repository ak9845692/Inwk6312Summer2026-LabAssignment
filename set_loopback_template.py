import yaml
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# -----------------------------
# Load YAML files
# -----------------------------
with open("hosts.yml", "r") as f:
    hosts = yaml.load(f, Loader=yaml.SafeLoader)

with open("interfaces.yml", "r") as f:
    interfaces = yaml.load(f, Loader=yaml.SafeLoader)

# -----------------------------
# Setup Jinja2 environment
# -----------------------------
env = Environment(
    loader=FileSystemLoader("."),
    trim_blocks=True,
    autoescape=False
)

template = env.get_template("interfaces_config_template.j2")

# Render configuration from YAML data
config_rendered = template.render(data=interfaces)

# Convert rendered template into list of CLI commands
config_commands = config_rendered.strip().split("\n")

# -----------------------------
# Push configuration to devices
# -----------------------------
for host in hosts["hosts"]:
    print(f"\nConnecting to {host['name']}...")

    net_connect = Netmiko(
        host=host["name"],
        username=host["username"],
        password=host["password"],
        port=host["port"],
        device_type=host["type"]
    )

    print(f"Logged into {host['name']} successfully")

    output = net_connect.send_config_set(config_commands)

    print(f"Pushed configuration to {host['name']} successfully")
    print(output)

    net_connect.disconnect()

print("\nDONE - All devices configured successfully")
