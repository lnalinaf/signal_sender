from asyncio import Queue

import pandas as pd
from ta import trend

from src.utils.log_module import setup_logger

logger = setup_logger()


in_position = 0
long_position = 0
short_position = 0


async def ishimoku_strategy_1(queue_window: Queue, resolution_queue: Queue):
    resolution_queue._maxsize = 5
    global in_position
    global long_position
    global short_position
    global count
    k = 0.3
    k_stop = 5

    while True:
        df_window = await queue_window.get()
        queue_window.task_done()

        if len(df_window) < 53:
            logger.info(len(df_window))
            continue

        ishimoku = trend.IchimokuIndicator(high=df_window.h, low=df_window.l)

        ishimoku_indicator = pd.DataFrame(
            {
                "red_line": ishimoku.ichimoku_base_line(),
                "blue_line": ishimoku.ichimoku_conversion_line(),
                "ishimoku_a": ishimoku.ichimoku_a(),
                "ishimoku_b": ishimoku.ichimoku_b(),
                "lag_span": df_window["c"].shift(-26),
                "close": df_window.c,
            }
        )
        strategy_resolution = None

        logger.debug(ishimoku_indicator)

        # Start LONG
        if not in_position != 0 and ishimoku_indicator.lag_span.iloc[
            -27
        ] - k > (
            ishimoku_indicator.ishimoku_a.iloc[-27]
            and ishimoku_indicator.ishimoku_b.iloc[-27]
            and ishimoku_indicator.close.iloc[-27]
        ):
            strategy_resolution = {
                "side": "LONG",
                "price": ishimoku_indicator.close.iloc[-1],
            }
            logger.info(
                "LONG by estimate"
                + f"price {ishimoku_indicator.close.iloc[-1]}"
            )

            in_position = 1
            long_position = 1

        # Start SHORT
        if not in_position != 0 and ishimoku_indicator.lag_span.iloc[
            -27
        ] + k < (
            ishimoku_indicator.ishimoku_a.iloc[-27]
            and ishimoku_indicator.ishimoku_b.iloc[-27]
            and ishimoku_indicator.close.iloc[-27]
        ):
            strategy_resolution = {
                "side": "SHORT",
                "price": ishimoku_indicator.close.iloc[-1],
            }
            logger.info(
                "SHORT by estimate"
                + f"price {ishimoku_indicator.close.iloc[-1]}"
            )

            in_position = 1
            short_position = 1

        # close LONG
        if long_position == 1:
            if ishimoku_indicator.lag_span.iloc[-27] + k < (
                ishimoku_indicator.red_line.iloc[-27]
                and ishimoku_indicator.blue_line.iloc[-27]
                and ishimoku_indicator.close.iloc[-27]
            ):
                strategy_resolution = {
                    "side": "CLOSE",
                    "price": ishimoku_indicator.close.iloc[-1],
                }
                logger.info(
                    "CLOSE LONG by estimate"
                    + f"price {ishimoku_indicator.close.iloc[-1]}"
                )
                in_position = 0
                long_position = 0

        # # close SHORT
        if short_position == 1:
            if ishimoku_indicator.lag_span.iloc[-27] - k > (
                ishimoku_indicator.red_line.iloc[-27]
                and ishimoku_indicator.blue_line.iloc[-27]
                and ishimoku_indicator.close.iloc[-27]
            ):
                strategy_resolution = {
                    "side": "CLOSE",
                    "price": ishimoku_indicator.close.iloc[-1],
                }
                logger.info(
                    "CLOSE SHORT by estimate"
                    + f"price {ishimoku_indicator.close.iloc[-1]}"
                )
                in_position = 0
                short_position = 0

        if strategy_resolution is not None:
            logger.debug(f"LAG {ishimoku_indicator.lag_span.iloc[-27]}")
            logger.debug(
                f"ISHIMOKU A {ishimoku_indicator.ishimoku_a.iloc[-27]}"
            )
            logger.debug(
                f"ISHIMOKU B {ishimoku_indicator.ishimoku_b.iloc[-27]}"
            )
            logger.debug(f"RED {ishimoku_indicator.red_line.iloc[-27]}")
            logger.debug(f"BLUE {ishimoku_indicator.blue_line.iloc[-27]}")
            logger.debug(f"CLOSE {ishimoku_indicator.close.iloc[-27]}")

        if resolution_queue.full():
            logger.warning("WINDOW QUEUE is FULL, delete oldest value")
            resolution_queue.get_nowait()
            resolution_queue.task_done()

        logger.debug(f" WINDOW QUEUE:\n     {resolution_queue}")
        await resolution_queue.put(strategy_resolution)
