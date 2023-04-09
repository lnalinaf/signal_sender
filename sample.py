import asyncio

from src.models.algorithms import ishimoku_strategy_1
from src.models.memcache_manager.handler import sender_to_memcache
from src.utils.connector import consume_stream
from src.utils.handler import get_window_data
from src.utils.log_module import setup_logger

logger = setup_logger()


async def main():
    queue_stream_exchange = asyncio.Queue()
    queue_window_data = asyncio.Queue()
    queue_resolution = asyncio.Queue()

    consume_task = asyncio.create_task(
        consume_stream(
            queue_stream_exchange, maxLenghtQueue=60, typeconnect="kline_1s"
        )
    )
    window_26 = asyncio.create_task(
        get_window_data(
            queue_stream_exchange, queue_window_data, window_size=53
        )
    )
    result = asyncio.create_task(
        ishimoku_strategy_1(queue_window_data, queue_resolution)
    )
    sender = asyncio.create_task(sender_to_memcache(queue_resolution))

    await asyncio.gather(window_26, consume_task, result, sender)


asyncio.run(main())
