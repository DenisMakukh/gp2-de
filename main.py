import asyncio
import logging

from src.sources.rabota_ru import RabotaRuSource
from src.utils.setup_logging import setup_logging

log = logging.getLogger(__name__)

if __name__ == '__main__':
    setup_logging()
    log.info("Logging setup successfully")
    rabota_ru = RabotaRuSource()
    asyncio.run(rabota_ru.search())
