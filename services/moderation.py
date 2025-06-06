import yaml
import re
from pathlib import Path

# Load config once
CONFIG_PATH = Path("config/response_control.yaml")

def load_response_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

response_config = load_response_config()

# Run moderation on incoming query
def run_moderation_check(query: str) -> str:
    query = query.lower().strip()

    for tag, triggers in response_config.get("triggers", {}).items():
        for trigger in triggers:
            if re.search(rf"\b{re.escape(trigger)}\b", query):
                return response_config["fallbacks"].get(tag, None)

    return None  # If no issue
