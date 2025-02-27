"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 27.02.2025
"""
import logging
import time

import pandas as pd

from src.config import APP_ID, CODE_TOKEN, APP_SECRET
from src.sources.source import Source
from src.utils.signature import get_signature

log = logging.getLogger(__name__)


class RabotaRuSource(Source):
    async def search(self) -> pd.DataFrame:
        log.info(f"Parsing rabota.ru source")

        # Uncomment for unknown device
        # await self._get_auth_permission()

        token = await self._get_auth_token()
        response = await self._get_vacancies(token, 46950440, 46950460)

        # TODO: parse into dataframe

        print(response)

    async def _get_auth_token(self) -> str:
        log.info("Getting rabota.ru auth token")

        url = "https://api.rabota.ru/oauth/token.json"

        current_time = str(int(time.time()))

        params = {
            "app_id": APP_ID,
            "time": current_time,
            "code": CODE_TOKEN,
        }

        signature = get_signature(params, APP_SECRET)

        data = {**params, "signature": signature}

        headers = {
            "content-type": "application/x-www-form-urlencoded",
        }

        response = await self.make_request(
            method="POST",
            url=url,
            headers=headers,
            body=data,
        )

        if "access_token" in response:
            log.info("Token received successfully")
            return response["access_token"]
        else:
            log.error("Failed to get token")
            raise ValueError("Failed to get token: Invalid response")

    async def _get_auth_permission(self):
        log.info("Getting rabota.ru auth permission")
        params = {
            "app_id": APP_ID,
            "scope": "profile,vacancies",
            "display": "page",
            "redirect_uri": "http://www.example.com/oauth"
        }

        url = "https://api.rabota.ru/oauth/authorize.html"
        response = await self.make_request(url=url, method="GET", params=params)
        return response

    async def _get_vacancies(self, token, min_id, max_id):
        log.info("Getting rabota.ru vacancies")
        ids_to_find = [i for i in range(min_id, max_id + 1)]
        url = "https://api.rabota.ru/v6/vacancies.json"
        headers = {
            "Content-Type": "application/json",
            "X-Token": token
        }
        json = {
            "request": {
                "vacancy_ids": ids_to_find
            }
        }

        response = await self.make_request("POST", url, headers=headers, body=json)
        return response
