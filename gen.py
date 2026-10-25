import json
import sys
import urllib.request

URL = "https://controlplane.tailscale.com/derpmap/default"

with urllib.request.urlopen(URL, timeout=30) as resp:
    data = json.load(resp)

v4 = set()
v6 = set()
for region in data["Regions"].values():
    for node in region["Nodes"]:
        if node.get("IPv4"):
            v4.add(node["IPv4"])
        if node.get("IPv6"):
            v6.add(node["IPv6"])

if len(v4) < 50 or len(v6) < 50:
    sys.exit("derpmap looks broken, refusing to write")

v4 = sorted(v4, key=lambda ip: tuple(int(part) for part in ip.split(".")))
lines = [f"IP-CIDR,{ip}/32" for ip in v4]
lines += [f"IP-CIDR6,{ip}/128" for ip in sorted(v6)]

with open("tailscale.list", "w") as f:
    f.write("\n".join(lines) + "\n")
