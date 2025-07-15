import requests
import jwt
import json
import sys
import colorama

from common import logger


class CrApiManager:
    """
    Объект для обращения за данными к Clash Royale Api.

    Методы:
    __create_request__ - создание и исполнение запроса;
    getPlayerInfo - данные об игроке;
    getPlayerBattleLog - данные об истории боев игрока;
    и ещё что-то, позже добавлю.

    """
    def __init__(
            self,
            apikey: str,
            address="https://api.clashroyale.com/v1"
    ):
        self.apikey:str = apikey
        self.address:str = address

        self.jwt_headers:dict = {
            "Authorization": f"Bearer {self.apikey}",
        }
        logger.info("CR Api manager inititializes")

    def __create_request__(self, request: str) -> dict:
        request_address:str = self.address + request

        response = requests.get(
            request_address,
            headers=self.jwt_headers
        )

        if response.status_code != 200:
            return {"status_code": str(response.status_code)}

        json_response = response.json()

        return json_response


    def getPlayerInfo(self, player_tag: str) -> dict:
        if "#" in player_tag:
            player_tag = player_tag.replace("#", "%23")
        elif "%23" not in player_tag:
            player_tag = "%23" + player_tag

        request:str = f"/players/{player_tag}"

        return self.__create_request__(request)

    def getPlayerBattleLog(self, player_tag: str) -> dict:
        if "#" in player_tag:
            player_tag = player_tag.replace("#", "%23")
        elif "%23" not in player_tag:
            player_tag = "%23" + player_tag

        request:str = f"/{player_tag}/battlelog"

        return self.__create_request__(request)
