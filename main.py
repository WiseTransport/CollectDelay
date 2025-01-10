import asyncio
import json
import logging
import logging.config
from datetime import datetime

import aiohttp
import redis
from pydantic import BaseModel, Field

logging.config.dictConfig({
    'version': 1,
    'handlers': {
        'telegram': {
            'class': 'telegram_handler.TelegramHandler',
            'token': '7300288725:AAFuyPyNHiW5CCHFzE5kknn1_eMxTfjLsTQ',
            'chat_id': '1370280956'
        }
    },
    'loggers': {
        'tg': {
            'handlers': ['telegram'],
            'level': 'DEBUG'
        }
    }
})
logger = logging.getLogger("tg")


class TrainData(BaseModel):
    id: int = Field(alias="train")
    delay: int
    TimePlanned: datetime
    date: datetime


async def parse_trains(trains: str) -> list[TrainData]:
    return [TrainData(**{
        k: v
        for k, v in item.items()
    }) for item in json.loads(trains)]


async def fetch_train_data() -> str:
    session = aiohttp.ClientSession()
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=60, sock_read=60)
    url = "https://radar.bdz.bg/bg"

    async with session.get(url, timeout=timeout) as resp:
        content = (await resp.content.read()).decode("utf-8")

    # content = open("test.html", mode="r", encoding="utf-8").read()
    search_start = "var trains = "
    start_i = content.find(search_start)
    end_i = content[start_i:].index("]") + len(content[:start_i]) + 1

    await session.close()

    return content[start_i+len(search_start):end_i]


async def main():
    # data = await fetch_train_data()
    # open("test.html", mode="w+", encoding="utf-8").write(data)
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    
    prev_id_to_data = None
    while True:
        curr_trains = await parse_trains(await fetch_train_data())

        id_to_data: dict[int, TrainData] = {train.id: train for train in curr_trains}
        curr_train_ids = set(id_to_data.keys())
        print("current trains riding: ", curr_train_ids)

        if prev_id_to_data and (ended := set(prev_id_to_data.keys()) - curr_train_ids):
            print(f"{ended} writing")
            for t_id in ended:
                train = prev_id_to_data[t_id]
                print("saving train: ", prev_id_to_data[t_id].model_dump(mode="json"))

                r.hset(f"trains:{t_id}-{train.date.timestamp()}", mapping=train.model_dump(mode="json"))

            print(f"{ended} written")

        prev_id_to_data = id_to_data

        await asyncio.sleep(30)

try:
    asyncio.run(main())
except Exception as e:
    logger.exception(e)
