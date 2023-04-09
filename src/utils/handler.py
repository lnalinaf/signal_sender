import datetime
from asyncio import Queue

import aiohttp
import pandas as pd
from loguru import logger


async def get_window_data(
    queue_stream: Queue, queue_send: Queue, window_size: int = 10
):
    logger.info(f"Set window value = {window_size}")

    queue_send._maxsize = window_size

    # {'e': 'kline', 'E': 1680108672001, 's': 'BTCUSDT',
    # 'k': {'t': 1680108671000, 'T': 1680108671999,
    # 's': 'BTCUSDT', 'i': '1s', 'f': 3062960349,
    # 'L': 3062960380, 'o': '28312.78000000',
    # 'c': '28312.78000000', 'h': '28312.79000000',
    # 'l': '28312.78000000', 'v': '5.14839000',
    # 'n': 32, 'x': True, 'q': '145765.23367100',
    # 'V': '0.02468000', 'Q': '698.75965720', 'B': '0'}}

    df = pd.DataFrame(
        [[None, None, None, None]],
        columns=["T", "c", "l", "h"],
    )

    while True:
        item = await queue_stream.get()

        queue_stream.task_done()

        if "result" in item:
            continue

        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [
                        [
                            item["k"]["T"],
                            item["k"]["c"],
                            item["k"]["l"],
                            item["k"]["h"],
                        ]
                    ],
                    columns=["T", "c", "l", "h"],
                    dtype="float64",
                ),
            ],
            ignore_index=True,
        )

        if len(df) > window_size:
            df.drop(0, inplace=True)

        if queue_send.full():
            logger.warning("WINDOW QUEUE is FULL, delete oldest value")
            queue_send.get_nowait()
            queue_send.task_done()

        logger.debug(f" WINDOW QUEUE:\n     {queue_send}")
        await queue_send.put(df)


async def get_binance_server_time():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.binance.com/api/v3/time"
        ) as response:
            response_json = await response.json()
            dt_object = datetime.datetime.fromtimestamp(
                response_json["serverTime"] / 1000
            )
            utc_dt_object = dt_object.astimezone(datetime.timezone.utc)
            logger.info(utc_dt_object)
            return
