import os
import logging
import time
import pandas as pd

from src.config import RABOTA_RU_APP_ID, RABOTA_RU_CODE_TOKEN, RABOTA_RU_APP_SECRET
from src.sources.source import Source
from src.utils.rabota_ru_mapper import parse_json_list_to_dataframe
from src.utils.signature import get_signature

log = logging.getLogger(__name__)


class RabotaRuSource(Source):
    def __init__(self):
        self.output_file = "rabota_ru_vacancies_1.csv"
        self.checkpoint_file = "checkpoint_1.txt"

    async def search(self) -> pd.DataFrame:
        log.info("Parsing rabota.ru source")

        if os.path.exists(self.output_file):
            log.info("Loading existing vacancies from file")
            df = pd.read_csv(self.output_file)
            vacancies = df.to_dict("records")
        else:
            vacancies = []

        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, "r") as f:
                last_processed_id = int(f.read().strip())
        else:
            last_processed_id = 46955330

        token = await self._get_auth_token()

        for idx in range(last_processed_id, 46960440):
            try:
                log.info(f"Parsing vacancy for id: {idx}")
                response = await self._get_vacancy(token, idx)
                vacancy = response['response']
                vacancies.append(vacancy)

                if idx % 10 == 0:
                    self._save_vacancies(vacancies)
                    self._save_checkpoint(idx)

            except Exception as e:
                log.error(f"Error parsing vacancy for id: {idx}")

        self._save_vacancies(vacancies)
        log.info("Parsing completed and data saved successfully")

        return parse_json_list_to_dataframe(vacancies)

    def _save_vacancies(self, vacancies):
        """Сохраняет текущие данные в файл."""
        df = parse_json_list_to_dataframe(vacancies)
        df.to_csv(self.output_file, index=False)
        log.info(f"Vacancies saved to {self.output_file}")

    def _save_checkpoint(self, last_id):
        """Сохраняет последний обработанный ID в файл."""
        with open(self.checkpoint_file, "w") as f:
            f.write(str(last_id))
        log.info(f"Checkpoint saved: last processed ID = {last_id}")

    async def _get_auth_token(self) -> str:
        log.info("Getting rabota.ru auth token")

        url = "https://api.rabota.ru/oauth/token.json"

        current_time = str(int(time.time()))

        params = {
            "app_id": RABOTA_RU_APP_ID,
            "time": current_time,
            "code": RABOTA_RU_CODE_TOKEN,
        }

        signature = get_signature(params, RABOTA_RU_APP_SECRET)

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
            "app_id": RABOTA_RU_APP_ID,
            "scope": "profile,vacancies",
            "display": "page",
            "redirect_uri": "http://www.example.com/oauth"
        }

        url = "https://api.rabota.ru/oauth/authorize.html"
        response = await self.make_request(url=url, method="GET", params=params)
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
