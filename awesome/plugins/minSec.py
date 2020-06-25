from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('interval', minutes=1)
async def _():
    print('一分钟经过')
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=864648168,
                                 message=f'一分钟经过，' + str(now.hour) + ":" + str(now.minute))
    except CQHttpError:
        pass