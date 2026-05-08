# %%
import os 
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent/"data"/".env"
load_dotenv(env_path)

model = os.getenv("model")
print(f"Model: {model}")
# %%