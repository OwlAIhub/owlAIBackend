import yaml
from pathlib import Path

def get_response_config(intent: str, tone: str, language: str) -> str:
    yaml_path = Path("config/response_control.yaml")
    
    if not yaml_path.exists():
        return "You are OwlAI, a helpful UGC NET mentor. Please assist the student with kindness and clarity."

    try:
        with open(yaml_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return (
            data.get(intent, {})
                .get(f"tone_{tone}", {})
                .get(language.lower(), "You are OwlAI, a kind UGC NET mentor. Please explain clearly and helpfully.")
        )
    except Exception as e:
        print("[YAML CONFIG ERROR]", str(e))
        return "You are OwlAI, a warm and clear UGC NET mentor. Please respond helpfully."
