from asyncio import Queue

from loguru import logger


async def get_window_data(
    queue_stream: Queue, queue_send: Queue, window_size: int = 10
):
    logger.info(f"Set window value = {window_size}")

    queue_send._maxsize = window_size

    data = []
    while True:
        item = await queue_stream.get()
        queue_stream.task_done()

        if "result" in item:
            continue

        data.append({"p": item["p"], "E": item["E"], "s": item["s"]})

        if len(data) > window_size:
            data.pop(0)

        if queue_send.full():
            logger.warning("WINDOW QUEUE is FULL, delete oldest value")
            queue_send.get_nowait()
            queue_send.task_done()

        logger.debug(f" WINDOW QUEUE:\n     {queue_send}")
        await queue_send.put(data)
