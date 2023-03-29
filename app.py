import asyncio

from src.utils.connector import consume_stream
from src.utils.handler import get_window_data
from src.utils.log_module import setup_logger

logger = setup_logger()


async def main():
    queue_stream_exchange = asyncio.Queue()
    queue_window_data = asyncio.Queue()

    consume_task = asyncio.create_task(
        consume_stream(queue_stream_exchange, maxLenghtQueue=5)
    )
    window_26 = asyncio.create_task(
        get_window_data(
            queue_stream_exchange, queue_window_data, window_size=6
        )
    )

    await asyncio.gather(window_26, consume_task)


asyncio.run(main())
