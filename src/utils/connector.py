import json
from asyncio import Queue, sleep

import websockets
from loguru import logger


async def consume_stream(
    queue_stream: Queue,
    tradePairs: list = ["btcusdt"],
    timeFrame: int = 1,
    typeconnect: str = "trade",
    maxLenghtQueue=52,
):
    queue_stream._maxsize = maxLenghtQueue

    subscription_msg = {
        "method": "SUBSCRIBE",
        "params": [pair.lower() + "@" + typeconnect for pair in tradePairs],
        "id": 1,
    }

    while True:
        try:
            async with websockets.connect(
                "wss://stream.binance.com:9443/ws"
            ) as websocket:
                await websocket.send(json.dumps(subscription_msg))
                logger.info(
                    f"Connect to websocket with params {subscription_msg}"
                )
                while True:
                    data = await websocket.recv()

                    await sleep(timeFrame)

                    if queue_stream.full():
                        logger.warning(
                            "Stream QUEUE if FULL, delete oldest value"
                        )
                        queue_stream.get_nowait()
                        queue_stream.task_done()

                    logger.debug(f" STREAM QUEUE:\n     {queue_stream}")
                    await queue_stream.put(json.loads(data))

        except websockets.exceptions.ConnectionClosedError:
            logger.exception(
                "WebSocket connection closed unexpectedly,"
                + "attempting to reconnect..."
            )
            await sleep(1)  # Wait 1 seconds before attempting to reconnect
