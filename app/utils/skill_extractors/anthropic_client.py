import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("SKILL_EXTRACTORS_KEY")

client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
)