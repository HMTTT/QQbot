from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('interval', minutes=30)
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        with open('./data/log.txt', 'a+', encoding='utf-8') as f:
            f.write(str(now) + '\r\n')
    except Exception:
        pass
