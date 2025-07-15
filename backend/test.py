import sys
import json
from dotenv import load_dotenv
import os
import requests

load_dotenv()

apikey: str = os.getenv("APIKEY")
address = "https://api.clashroyale.com/v1"

jwt_headers: dict = {
"Authorization": f"Bearer {apikey}",
}

request_address: str = address + f"/locations/global/seasons/2025-06/rankings/players"

response = requests.get(
    request_address,
    headers=jwt_headers
)

if response.status_code != 200:
    print(response.status_code)
    sys.exit(1)

json_response = response.json()
print(json_response)

with open("data/player.json", "w", encoding="utf-8") as file:
    json.dump(json_response, file)
