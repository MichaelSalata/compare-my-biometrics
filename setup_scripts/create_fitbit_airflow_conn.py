import os
import json
import urllib.parse
from typing import Optional, Dict, Any
from dotenv import load_dotenv, set_key
import argparse
import logging

# Constants
DEFAULT_JSON_PATH = 'fitbit_tokens.json'
DEFAULT_DOTENV_PATH = '.env'
CONN_NAME = "AIRFLOW_CONN_FITBIT_HTTP"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_tokens(json_file_path: str) -> Dict[str, Any]:
    logger.info(f"Loading tokens from {json_file_path}")
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"Token file not found: {json_file_path}")
    with open(json_file_path, 'r') as f:
        return json.load(f)

# LEGACY: This function is not used in the current script, but it can be useful for generating a URI for Fitbit API connections.
def make_fitbit_uri(token_data: Dict[str, Any], host: str = "api.fitbit.com") -> str:
    login = urllib.parse.quote(token_data["client_id"])
    passwd = urllib.parse.quote(token_data["client_secret"])

    extras = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "token_type": token_data.get("token_type", "Bearer"),
        "user_id": token_data["user_id"],
        "expires_at": token_data.get("expires_at")
    }
    # Scope list -> comma string
    scope = token_data.get("scope")
    if scope:
        extras["scope"] = ",".join(scope)

    # URL‑encode each param
    query = urllib.parse.urlencode(extras)
    return f"http://{login}:{passwd}@{host}?{query}"

def update_dotenv(env_var_name: str, env_string: str, dotenv_path: str = DEFAULT_DOTENV_PATH):
    logger.info(f"Setting {env_var_name} in {dotenv_path}")
    load_dotenv(dotenv_path)  # Load existing .env
    set_key(dotenv_path, env_var_name, env_string)

def main(
    json_file_path: Optional[str] = None,
    token_dict: Optional[Dict[str, Any]] = None,
    dotenv_path: str = DEFAULT_DOTENV_PATH
):
    # Determine source of tokens
    if token_dict:
        logger.info("Using token_dict provided via argument")
        tokens = token_dict
    else:
        path = json_file_path or DEFAULT_JSON_PATH
        tokens = load_tokens(path)

    conn_json = json.dumps(tokens, indent=4)
    update_dotenv(CONN_NAME, conn_json, dotenv_path)
    logger.info(f"{CONN_NAME} successfully set.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Create or update {CONN_NAME} in .env")
    parser.add_argument("--json", type=str, help="Path to the Fitbit token JSON file")
    parser.add_argument("--dotenv", type=str, default=DEFAULT_DOTENV_PATH, help="Path to the .env file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        main(json_file_path=args.json, dotenv_path=args.dotenv)
    except Exception as e:
        logger.error(f"Failed to create Airflow connection: {e}")
