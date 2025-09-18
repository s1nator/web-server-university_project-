import yaml


with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

quantity_workers = cfg["database"]["quantity_workers"]
working_directory = cfg["database"]["working_dir"]
host = cfg["database"]["host"]
port = cfg["database"]["port"]
date_logs_delete = cfg["database"]["date_logs_delete"]
PROXY_PASS_HOST = cfg["database"]["proxy_pass_host"]
PROXY_PASS_PORT = cfg["database"]["proxy_pass_port"]
