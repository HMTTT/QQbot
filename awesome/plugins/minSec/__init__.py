from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('interval', minutes=1)
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        with open('./awesome/plugins/data/log.txt', 'a+', encoding='utf-8') as f:
            f.write(str(now))
    except Exception:
        pass
