from nonebot import on_command, CommandSession
from .data_source import *
from collections import Iterable

@on_command('note', aliases=('记录', 'n'))
async def note(session: CommandSession):
    op = session.get('op', prompt='你想要使用note的哪些功能？')
    msg = await handleOp(op, session)
    
    newLine = '\r\n'
    if type(msg) is list or type(msg) is type({}.keys()):
        text = ''
        flag = True
        for m in msg:
            if (len(text) + len(m)) > 200:
                await session.send(text)
                flag = True
                text = m
            else:
                flag = False
                text += m + newLine
        await session.send(text)
    else:
        await session.send(msg)


@note.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['op'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('输入无效，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
