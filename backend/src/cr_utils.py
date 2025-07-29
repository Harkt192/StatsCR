import aiohttp
import os

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
                request_address,
                headers=self.headers
            ) as response:
                if response.status != 200:
                    logger.critical(f"CrApi bad request, status: {response.status}")
                    logger.critical(f"Request address: {request_address}")
                    return {"status_code": str(response.status)}

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
        full_player_data: dict
) -> dict:
    player_data = dict()
    player_data["tag"] = full_player_data["tag"]
    player_data["name"] = full_player_data["name"]
    player_data["expLevel"] = full_player_data["expLevel"]
    player_data["trophies"] = full_player_data["trophies"]
    player_data["wins"] = full_player_data["wins"]
    player_data["losses"] = full_player_data["losses"]
    player_data["clan"] = full_player_data["clan"]["name"]
    player_data["currentFavouriteCard"] = reformat_card_data(card=full_player_data["currentFavouriteCard"])
    player_data["currentDeck"] = []
    for i, card in enumerate(full_player_data["currentDeck"]):
        player_data["currentDeck"].append(reformat_card_data(card=card, i=i))
    return player_data


def define_url(card: dict) -> str:
    if "evolutionLevel" in card:
        url = card["iconUrls"]["evolutionMedium"]
    else:
        url = card["iconUrls"]["medium"]
    return url


def reformat_card_data(card: dict, i: int = 0) -> dict:
    card_data = dict()
    card_data["name"] = card["name"]
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
