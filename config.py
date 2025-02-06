# config.py
import os
import logging
from dotenv import load_dotenv

# 1. Load environment variables from .env file
load_dotenv()

# 2. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

# 3. Retrieve the OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# 4. Warn if the key is missing
if not OPENAI_API_KEY:
    logging.warning("OpenAI API Key is not set. Check your .env file or environment.")
else:
    logging.info("OpenAI API Key successfully loaded.")
