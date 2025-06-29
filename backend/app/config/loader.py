import os
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

class ConfigLoader:
    def __init__(self):
        self.env = os.getenv("ENV", "dev")
        self.region = os.getenv("AWS_REGION", "ap-south-1")
        self.parameter_name = f"/messmate/config/{self.env}"

        if self.env == "local" and os.path.exists("app/config/local.config"):
            self._config = self._load_from_local_file()
        else:
            self._config = self._load_from_ssm()

    def _load_from_local_file(self) -> dict:
        path = "app/config/local.config"
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load local.config: {e}")

    def _load_from_ssm(self) -> dict:
        try:
            ssm = boto3.client("ssm", region_name=self.region)
            response = ssm.get_parameter(Name=self.parameter_name, WithDecryption=True)
            return json.loads(response["Parameter"]["Value"])
        except Exception as e:
            raise RuntimeError(f"Failed to fetch from SSM: {e}")

    @property
    def config(self):
        return self._config
    
    def get_database_config(self):
        return self._config["database"]

    def get_database_url(self) -> str:
        db = self._config["database"]
        return f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"
