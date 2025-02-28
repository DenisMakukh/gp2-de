"""
Module Description:
This module performs XYZ functionality.

Author: Denis Makukh
Date: 28.02.2025
"""
import logging
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.sources.source import Source

log = logging.getLogger(__name__)


class HHRuSource(Source):
    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Запуск без интерфейса для скорости
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Базовый URL для парсинга
        self.BASE_URL = "https://hh.ru/search/vacancy?text=&professional_role={role}&enable_snippets=true&order_by=relevance&items_on_page=100&page={page}"
        self.roles = [156, 10, 150, 165, 73, 96, 164, 107, 148, 126, 124]

    async def search(self) -> pd.DataFrame:
        log.info("Parsing hh.ru source")
        start_time = time.time()
        all_vacancies = []

        try:
            for role in self.roles:
                log.info("Current role: {}".format(role))
                total_pages = self.get_num_of_pages(role)
                log.info("Total pages: {}".format(total_pages))
                for page in range(total_pages):
                    vacancies = self.parse_vacancies(role, page)
                    log.info("Vacancies found in page: {}".format(vacancies))
                    if not vacancies:
                        break
                    all_vacancies.extend(vacancies)

            df = pd.DataFrame(all_vacancies)
            df.to_csv("hh_ru_vacancies.csv", index=False, encoding="utf-8-sig")
            log.info("Vacancies parsed in {} seconds".format(time.time() - start_time))
            print(df.head())
            return df
        finally:
            self.driver.quit()
            print(f"Всего вакансий: {len(all_vacancies)}")
            print(f"Время выполнения: {time.time() - start_time:.2f} секунд")

    def get_num_of_pages(self, role):
        """Определяет количество страниц вакансий для роли"""
        self.driver.get(self.BASE_URL.format(role=role, page=0))
        time.sleep(1.5)
        self.scroll_to_bottom()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        pages = soup.find_all("a", {"data-qa": "pager-page"})
        return int(pages[-1].get_text(strip=True)) if pages else 1

    def parse_vacancies(self, role, page):
        """Парсит вакансии с одной страницы"""
        self.driver.get(self.BASE_URL.format(role=role, page=page))
        time.sleep(1)
        self.scroll_to_bottom()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        vacancy_elements = soup.find_all("div", class_="magritte-redesign")
        vacancies = []

        for vacancy in vacancy_elements:
            title_tag = vacancy.find("a", {"data-qa": "serp-item__title"})
            title = title_tag.get_text(strip=True) if title_tag else "Не указано"
            link = title_tag["href"] if title_tag else ""

            location_tag = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
            location = location_tag.get_text(strip=True) if location_tag else "Не указано"

            salary_tag = vacancy.find("span", {
                "class": "magritte-text___pbpft_3-0-27 magritte-text_style-primary___AQ7MW_3-0-27 magritte-text_typography-label-1-regular___pi3R-_3-0-27"})
            salary = salary_tag.get_text() if salary_tag else "Не указано"
            if salary != "Не указано":
                salary = salary.replace("\u202f", " ")
                salary = salary.replace("\xa0до вычета налогов", " до вычета налогов")

            company_tag = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-employer-text"})
            company = company_tag.get_text(strip=True) if company_tag else "Не указано"

            description_tag = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy_snippet_responsibility"})
            description = description_tag.get_text(strip=True) if description_tag else "Не указано"

            requirements_tag = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy_snippet_requirement"})
            requirements = requirements_tag.get_text(strip=True) if requirements_tag else "Не указано"

            experience_tag = vacancy.find("div", class_="magritte-tag__label___YHV-o_3-1-3")
            experience = experience_tag.get_text(strip=True) if experience_tag else "Не указано"

            vacancies.append({
                "role_id": role,
                "title": title,
                "link": link,
                "location": location,
                "salary": salary,
                "company": company,
                "experience": experience,
                "description": description,
                "requirements": requirements
            })

        return vacancies

    def scroll_to_bottom(self):
        """Плавная прокрутка страницы вниз для подгрузки вакансий"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
