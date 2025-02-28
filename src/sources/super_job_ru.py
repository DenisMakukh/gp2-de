"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 28.02.2025
"""
import logging
import time

import pandas as pd

from src.config import SUPERJOB_SECRET
from src.sources.source import Source
from src.utils.superjob_mapper import extend_vacancies_from_response

log = logging.getLogger(__name__)


class SuperJobSource(Source):
    def __init__(self):
        self.base_url = "https://api.superjob.ru/2.0"
        self.default_headers = {
            "X-Api-App-Id": SUPERJOB_SECRET
        }

    async def search(self) -> pd.DataFrame:
        log.info("Parsing superjob.ru source")
        vacancies = []

        # попарсим по ключевым словам
        keyword_to_find = [
            "разработчик", "аналитик данных", "BI-аналитик", "программист", "it", "аналитик",
            "devops", "junior", "middle", "senior", "lead", "доставка", "банк", "курьер", "цветы",
            "backend", "frontend", "fullstack", "web", "mobile", "android", "ios", "qa", "тестировщик",
            "системный администратор", "сетевой инженер", "data scientist", "машинное обучение",
            "искусственный интеллект", "big data", "базы данных", "sql", "nosql", "python", "java",
            "javascript", "c#", "c++", "php", "ruby", "go", "scala", "kotlin", "swift", "html",
            "css", "react", "angular", "vue", "node.js", "docker", "kubernetes", "aws", "azure",
            "google cloud", "linux", "windows", "cybersecurity", "кибербезопасность", "сеть",
            "хостинг", "сервер", "администрирование", "техническая поддержка", "helpdesk",
            "проектный менеджер", "менеджер продукта", "scrum", "agile", "kanban", "бизнес-аналитик",
            "финансовый аналитик", "бухгалтер", "экономист", "аудит", "налог", "юрист", "адвокат",
            "hr", "рекрутер", "кадры", "обучение персонала", "маркетинг", "smm", "seo", "контекстная реклама",
            "копирайтер", "контент-менеджер", "дизайнер", "графический дизайнер", "ui/ux", "иллюстратор",
            "видеомонтаж", "фотограф", "продажи", "менеджер по продажам", "торговый представитель",
            "ритейл", "логистика", "склад", "закупки", "снабжение", "производство", "инженер",
            "технолог", "механик", "электрик", "строительство", "архитектор", "дизайн интерьера",
            "недвижимость", "агент", "консультант", "оператор", "колл-центр", "обслуживание клиентов",
            "ресторан", "отель", "туризм", "спорт", "тренер", "медицина", "врач", "медсестра",
            "фармацевт", "лаборатория", "образование", "учитель", "преподаватель", "репетитор",
            "переводчик", "журналист", "редактор", "библиотекарь", "исследования", "наука",
            "лаборант", "эколог", "энергетика", "нефть", "газ", "химия", "биология", "физика",
            "математика", "статистика", "социология", "психология", "искусство", "музыка", "актер",
            "режиссер", "писатель", "блогер", "стример", "геймдев", "игры", "анимация", "3d", "vr",
            "ar", "робототехника", "дроны", "электроника", "телеком", "связь", "телевидение",
            "радио", "кино", "фото", "соцсети", "стартап", "предприниматель", "фриланс", "удаленная работа"
        ]
        for keyword in keyword_to_find:
            response = await self._get_vacancy_by_keyword(keyword)
            time.sleep(0.5)
            extend_vacancies_from_response(response, vacancies)
            log.info(f"New vacancies length: {len(vacancies)}")

        # попарсим по деньгам
        payment_order_response = await self._get_vacancy_by_salary_order()
        time.sleep(0.5)
        extend_vacancies_from_response(payment_order_response, vacancies)
        log.info(f"New vacancies length: {len(vacancies)}")

        # попарсим по москве
        moscow_response = await self._get_vacancy_by_param("town", "Москва")
        time.sleep(0.5)
        extend_vacancies_from_response(moscow_response, vacancies)
        log.info(f"New vacancies length: {len(vacancies)}")

        df = pd.DataFrame(vacancies)
        df.to_csv("superjob_ru_vacancies.csv", index=False)
        log.info("successfully saved vacancies data")
        return df

    async def _get_vacancy_by_keyword(self, keyword):
        log.info("Getting vacancies by keyword {}".format(keyword))

        params = {"keyword": keyword}
        endpoint = "/vacancies/"

        response = await self.make_request("GET", self.base_url + endpoint, params=params,
                                           headers=self.default_headers)
        return response

    async def _get_vacancy_by_salary_order(self):
        log.info("Getting vacancies by salary order")

        params = {"order_field": "payment"}
        endpoint = "/vacancies/"

        response = await self.make_request("GET", self.base_url + endpoint, params=params,
                                           headers=self.default_headers)
        return response

    async def _get_vacancy_by_param(self, key, value):
        log.info("Getting vacancies by kv")

        params = {key: value}
        endpoint = "/vacancies/"

        response = await self.make_request("GET", self.base_url + endpoint, params=params,
                                           headers=self.default_headers)
        return response
