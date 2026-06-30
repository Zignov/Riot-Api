import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("DEV_API")
HEADERS = {"X-Riot-Token": API_KEY}
REGION = "europe"


def print_api_error(function_name, response):
    print(f"[{function_name}] Error: {response.status_code}")
    print(response.text)