from nonebot import on_command, CommandSession


@on_command('hapi', aliases=('哈批'))
async def hapi(session: CommandSession):
    hapi = session.get('hapi', prompt='谁是哈批？')
    weather_report = await get_hapi(hapi)
   
    await session.send(weather_report)


@hapi.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['pcr'] = stripped_arg
        return

    if not stripped_arg:

        session.pause('要查询的城市名称不能为空呢，请重新输入')
    session.state[session.current_key] = stripped_arg


async def get_hapi(hapi: str) -> str:
    return f'{hapi}是哈批'