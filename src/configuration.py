import yaml
import os

class Config:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.BASE_DIR, "config.yaml")

        with open(self.config_path, "r") as f:
            cfg = yaml.safe_load(f)

        db = cfg.get("database", {})
        self.quantity_workers = db.get("quantity_workers") or 1
        self.working_directory = db.get("working_dir") or os.path.join(self.BASE_DIR, "public")
        self.host = db.get("host") or "127.0.0.1"
        self.port = db.get("port") or 8080
        self.date_logs_delete = db.get("date_logs_delete") or ""
        self.proxy_pass_host = db.get("proxy_pass_host")
        self.proxy_pass_port = db.get("proxy_pass_port") or 80

config = Config()
