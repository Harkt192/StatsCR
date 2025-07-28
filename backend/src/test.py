from asyncio import run
import json

from request_utils import ApiManager


async def main():
    json_data = await ApiManager.getPlayerInfo("CP2C0Y9Y2")

    with open("./data/clashroyale.json", "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


run(main())
