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
                    return {"status_code": str(response.status_code)}

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

        request: str = f"/{player_tag}/battlelog"

        return await self.__create_request__(request)


ApiManager: CrApiManager = CrApiManager(
    apikey=settings.APIKEY,
    address="https://api.clashroyale.com/v1"
)