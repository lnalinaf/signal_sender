import json

import aiomcache
from loguru import logger

ENV_SERVER_MEMCACHE = "memcached"


async def set_value(key_name: str, value_dict: dict, exptime: int = 0):
    json.dumps(value_dict)

    client = aiomcache.Client(ENV_SERVER_MEMCACHE, 11211)
    await client.set(
        key_name.encode(), json.dumps(value_dict).encode(), exptime=exptime
    )
    logger.debug(
        f"MEMCACHE: SET Key: {key_name}\n Values: {value_dict},"
        + f"\n exptime:{exptime}"
    )
    return None


async def get_value(key_name: str):
    client = aiomcache.Client(ENV_SERVER_MEMCACHE, 11211)
    json_bytes = await client.get(key_name.encode())
    json_value = json.loads(json_bytes.decode())
    logger.info(f"MEMCACHE: GET Key: {key_name}\n Values: {json_value}")
    return json_value


# z=asyncio.run(set_value("bas",{'c':'1'}))
# x=asyncio.run(get_value("bas"))

# logger.info(z)
# logger.info(x)
