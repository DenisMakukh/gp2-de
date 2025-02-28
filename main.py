import asyncio
import logging

from src.sources.hh_ru import HHRuSource
from src.sources.rabota_ru import RabotaRuSource
from src.sources.super_job_ru import SuperJobSource
from src.utils.setup_logging import setup_logging

log = logging.getLogger(__name__)

if __name__ == '__main__':
    setup_logging()
    log.info("Logging setup successfully")
    rabota_ru = RabotaRuSource()
    # hh_ru = HHRuSource()
    super_job = SuperJobSource()
    asyncio.run(super_job.search())
    # asyncio.run(rabota_ru.search())
    # asyncio.run(hh_ru.search())
