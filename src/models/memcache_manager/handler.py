from asyncio import Queue

from loguru import logger

from src.models.memcache_manager.client import set_value

strategy_name = "ishimoku1"
pair = "BTCUSDT"
period = "1s"


async def sender_to_memcache(queue_resolution: Queue):
    storage_last_item = 0
    # deal_count = 0
    while True:
        item: dict = await queue_resolution.get()
        queue_resolution.task_done()
        if item != storage_last_item:
            storage_last_item = item
            # await set_value(
            # f"{strategy_name}_{pair}_{period}_{deal_count}", item
            # )
            logger.info(item)

        # set_value()
