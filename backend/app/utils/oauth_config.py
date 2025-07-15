# app/utils/oauth_config.py
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.config.loader import ConfigLoader

config_data = ConfigLoader().config.get("google", {})

config = Config(environ={
    "GOOGLE_CLIENT_ID": config_data.get("client_id"),
    "GOOGLE_CLIENT_SECRET": config_data.get("client_secret"),
})

oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=config_data.get("client_id"),
    client_secret=config_data.get("client_secret"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",  # ✅ Required
    client_kwargs={
        "scope": "openid email profile"
    }
)
