from pathlib import Path

PROJECT_PATH=Path(__file__).parent.parent.absolute()
BASE_DATA_PATH=PROJECT_PATH/ "general.json"
print(BASE_DATA_PATH)