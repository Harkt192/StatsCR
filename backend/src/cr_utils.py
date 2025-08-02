import aiohttp
import json
import os

from fastapi import HTTPException

from log import logger
from settings import settings


class CrApiManager:
    """
    Объект для обращения к данным об игроках из Clash Royale Api.

    Методы:
    __create_request__ - создание и исполнение запроса;
    getPlayerInfo - данные об игроке;
    getPlayerBattleLog - данные об истории боев игрока;
    и ещё что-то, позже добавлю.

    """

    def __init__(
            self,
            apikey: str,
            address: str = "https://api.clashroyale.com/v1"
    ):
        self.apikey: str = apikey
        self.address: str = address

        self.headers: dict = {
            "Authorization": f"Bearer {self.apikey}",
        }
        logger.info("CR Api manager inititializing")

    async def __create_request__(self, request: str) -> dict:
        request_address: str = self.address + request


        async with aiohttp.ClientSession() as http_session:
            async with http_session.get(
                    url=request_address,
                    headers=self.headers
            ) as response:
                if response.status != 200:
                    logger.critical(f"CrApi bad request, status: {response.status}")
                    logger.critical(f"Request address: {request_address}")
                    raise HTTPException(
                        status_code=403,
                        detail="Ip address blocked."
                    )

                logger.debug("CrApi good request")
                json_response = await response.json()
                return json_response

    async def getPlayerInfo(self, player_tag: str) -> dict:
        if "#" in player_tag:
            player_tag = player_tag.replace("#", "%23")
        elif "%23" not in player_tag:
            player_tag = "%23" + player_tag

        request: str = f"/players/{player_tag}"

        return await self.__create_request__(request)

    async def getPlayerBattleLog(self, player_tag: str) -> dict:
        if "#" in player_tag:
            player_tag = player_tag.replace("#", "%23")
        elif "%23" not in player_tag:
            player_tag = "%23" + player_tag

        request: str = f"/players/{player_tag}/battlelog"

        return await self.__create_request__(request)


def reformat_player_data(
        player: dict
) -> dict:
    player_data = dict()
    player_data["tag"] = player["tag"]
    player_data["name"] = player["name"]
    player_data["expLevel"] = player["expLevel"]
    player_data["trophies"] = player["trophies"]
    player_data["wins"] = player["wins"]
    player_data["losses"] = player["losses"]
    if "clan" in player.keys():
        player_data["clan"] = player["clan"]["name"]
    else:
        player_data["clan"] = None
    player_data["currentFavouriteCard"] = reformat_card_data(card=player["currentFavouriteCard"])
    player_data["currentDeck"] = []
    for i, card in enumerate(player["currentDeck"]):
        player_data["currentDeck"].append(reformat_card_data(card=card, i=i))
    player_data["currentDeckSupportCard"] = {
        "name": player["currentDeckSupportCards"][0]["name"],
        "iconUrl": player["currentDeckSupportCards"][0]["iconUrls"]["medium"]
    }
    return player_data


def reformat_player_in_battle_data(player: dict) -> dict:
    player_data = dict()
    player_data["tag"] = player["tag"]
    player_data["name"] = player["name"]
    player_data["crowns"] = player["crowns"]
    if "clan" in player.keys():
        player_data["clan"] = player["clan"]["name"]
    else:
        player_data["clan"] = None
    player_data["cards"] = []
    for i, card in enumerate(player["cards"]):
        player_data["cards"].append(reformat_card_data(card=card, i=i))
    if player["supportCards"]:
        player_data["supportCard"] = {
            "name": player["supportCards"][0]["name"],
            "iconUrl": player["supportCards"][0]["iconUrls"]["medium"]
        }

    return player_data


def reformat_battlelog_data(
        full_battlelog_data: list
) -> list:
    battlelog_data = []
    for battle in full_battlelog_data:
        battle_data = reformat_battle_data(battle)
        battlelog_data.append(battle_data)
    return battlelog_data


def download_json(data: dict | list):
    with open("./data/test.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def reformat_battle_data(battle: dict) -> dict:
    battle_data = dict()
    battle_data["type"] = battle["type"]
    battle_data["isLadderTournament"] = battle["isLadderTournament"]
    battle_data["gameMode"] = battle["gameMode"]["name"]

    battle_data["team"] = []
    for player in battle["team"]:
        player_data = reformat_player_in_battle_data(player)
        battle_data["team"].append(player_data)

    battle_data["opponent"] = []
    for player in battle["opponent"]:
        player_data = reformat_player_in_battle_data(player)
        battle_data["opponent"].append(player_data)

    return battle_data


def define_url(card: dict) -> str:
    if "evolutionLevel" in card:
        url = card["iconUrls"]["evolutionMedium"]
    else:
        url = card["iconUrls"]["medium"]
    return url


def reformat_card_data(card: dict, i: int = 0) -> dict:
    card_data = dict()
    card_data["name"] = card["name"]
    if card_data["name"] != "Mirror":
        card_data["elixirCost"] = card["elixirCost"]
    if i < 2:
        card_data["iconUrl"] = define_url(card)
    else:
        card_data["iconUrl"] = card["iconUrls"]["medium"]
    return card_data


ApiManager: CrApiManager = CrApiManager(
    apikey=settings.APIKEY,
    address="https://api.clashroyale.com/v1"
)
