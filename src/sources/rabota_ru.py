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
from src.utils.rabota_ru_mapper import parse_json_list_to_dataframe
from src.utils.signature import get_signature

log = logging.getLogger(__name__)


class RabotaRuSource(Source):
    async def search(self) -> pd.DataFrame:
        log.info(f"Parsing rabota.ru source")
        vacancies = []

        # Uncomment for unknown device
        # await self._get_auth_permission()

        token = await self._get_auth_token()
        count_errors = 0

        for idx in range(46950440, 46960440):
            try:
                log.info(f"Parsing vacancy for id: {idx}")
                response = await self._get_vacancy(token, idx)
                vacancy = response['response']
                vacancies.append(vacancy)
                count_errors = 0
            except Exception as e:
                count_errors += 1
                if count_errors > 5:
                    log.error("More than 5 error seq detected, breaking", e)
                    break
                log.error(f"Error parsing vacancy for id: {idx}")

        df = parse_json_list_to_dataframe(vacancies)

        log.info("Saving vacancies to rabota_ru_vacancies.csv")
        path = df.to_csv(f"rabota_ru_vacancies.csv", index=False)
        log.info(f"Saving vacancies to rabota_ru_vacancies.csv done successfully {path}")

        return df

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

    async def _get_vacancy(self, token, id: int):
        log.info("Getting rabota.ru vacancy")
        url = "https://api.rabota.ru/v6/vacancy.json"

        headers = {
            "Content-Type": "application/json",
            "X-Token": token
        }

        json = {
            "request": {
                "vacancy_id": id
            }
        }

        response = await self.make_request("POST", url, headers=headers, body=json)
        return response
