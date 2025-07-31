from cr_utils import ApiManager

from asyncio import run
import json


async def main():
    a = await ApiManager.getPlayerBattleLog("CP2C0Y9Y2")

    with open("./data/clashroyale.json", "w", encoding="utf-8") as json_file:
        json.dump(a, json_file, ensure_ascii=False)


run(main())


