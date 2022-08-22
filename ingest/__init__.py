from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://nyc3.digitaloceanspaces.com/edm-recipes/datasets"
BASE_PATH = Path(__file__).parent / ".cache"

# if not os.path.isdir(BASE_PATH):
#     os.makedirs(BASE_PATH, exist_ok=True)
#     # create .gitignore so that files in this directory aren't tracked
#     with open(f"{BASE_PATH}/.gitignore", "w") as f:
#         f.write("*")
