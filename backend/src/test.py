# from cr_utils import ApiManager
#
# from asyncio import run
# import json
#
#
# async def main():
#     a = await ApiManager.getPlayerBattleLog("CP2C0Y9Y2")
#
#     with open("./data/clashroyale.json", "w", encoding="utf-8") as json_file:
#         json.dump(a, json_file, ensure_ascii=False)
#
#
# run(main())
#
#

async def async_func():
    pass


class Monster:
    def __init__(
            self,
            height: int,
            weight: int
    ):
        self.height = height
        self.weight = weight

    # def __setattr__(
    #         self,
    #         key: str,
    #         value: int
    # ):
    #     if key == "height":
    #         self.height = value
    #     elif key == "weight":
    #         self.weight = value
    #     else:
    #         raise AttributeError
    #     return

    def __eq__(self, other):
        if self.height == other.height and self.weight == other.weight:
            return True
        return False


spunchbob = Monster(1, 300)

belka = Monster(1, 300)

demon = Monster(52, 500)

print(spunchbob == belka)
print(spunchbob == demon)

print(spunchbob.height)
setattr(spunchbob, "a", 2)
print(spunchbob.height)
print(spunchbob.a)

