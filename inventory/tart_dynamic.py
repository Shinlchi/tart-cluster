#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from glob import glob

try:
    import yaml
except Exception:
    print("Missing dependency: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

INV_DIR = os.path.join(os.path.dirname(__file__))

def load_yaml_file(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def collect_hosts_from_obj(obj):
    hosts = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "hosts":
                # hosts can be mapping or list
                if isinstance(v, dict):
                    hosts.extend(list(v.keys()))
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            hosts.append(item)
                        elif isinstance(item, dict) and "name" in item:
                            hosts.append(item["name"])
                elif isinstance(v, str):
                    hosts.append(v)
            elif k == "vms" and isinstance(v, list):
                for item in v:
                    if isinstance(item, dict) and "name" in item:
                        hosts.append(item["name"])
            else:
                hosts.extend(collect_hosts_from_obj(v))
    elif isinstance(obj, list):
        for item in obj:
            hosts.extend(collect_hosts_from_obj(item))
    return hosts

def collect_hostvars_from_obj(obj):
    hostvars = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "hosts" and isinstance(v, dict):
                for h, hv in v.items():
                    if isinstance(hv, dict):
                        hostvars[h] = hv
            else:
                hostvars.update(collect_hostvars_from_obj(v))
    elif isinstance(obj, list):
        for item in obj:
            hostvars.update(collect_hostvars_from_obj(item))
    return hostvars

def tart_ip(name):
    try:
        out = subprocess.run(["tart", "ip", name], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return None

def main():
    files = glob(os.path.join(INV_DIR, "*.yml")) + glob(os.path.join(INV_DIR, "*.yaml"))
    seen = []
    hostvars = {}
    for f in files:
        data = load_yaml_file(f)
        hosts = collect_hosts_from_obj(data)
        hv = collect_hostvars_from_obj(data)
        for h, v in hv.items():
            hostvars.setdefault(h, {}).update(v)
        for h in hosts:
            if h and h not in seen:
                seen.append(h)

    # fallback: try group_vars/all.yml vms
    gv = os.path.join(INV_DIR, "group_vars", "all.yml")
    if os.path.exists(gv):
        data = load_yaml_file(gv)
        for item in data.get("vms", []):
            if isinstance(item, dict) and "name" in item:
                if item["name"] not in seen:
                    seen.append(item["name"])

    meta = {"hostvars": {}}
    for h in seen:
        # if inventory already provided ansible_host, keep it
        if hostvars.get(h, {}).get("ansible_host"):
            meta["hostvars"][h] = {"ansible_host": hostvars[h]["ansible_host"], **hostvars.get(h, {})}
            continue
        ip = tart_ip(h)
        if ip:
            meta["hostvars"][h] = {"ansible_host": ip, **hostvars.get(h, {})}
        else:
            meta["hostvars"][h] = hostvars.get(h, {})

    output = {
        "tart": {"hosts": seen, "vars": {}},
        "_meta": meta
    }
    print(json.dumps(output))

if __name__ == "__main__":
    main()