from nonebot import on_command, CommandSession
import requests as reqs
import json
import datetime
from collections import Counter
from .data_source import *


@on_command('pcr', aliases=('公主链接台服'))
async def pcr(session: CommandSession):
    # 获取op
    op = session.get('op', prompt='你想pcr执行哪些操作？')
    # 获取返回
    msg = await handleOp(op)
    # 发送消息
    if type(msg) is list:
        text = ''
        flag = True
        for m in msg:
            if (len(text) + len(m)) > 200:
                await session.send(text)
                flag = True
                text = m
            else:
                flag = False
                text += m
        print(len(text))
        await session.send(text)
                
    else:
        await session.send(msg)
    


@pcr.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    
    # 该命令第一次运行（第一次进入命令会话）
    if session.is_first_run:
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：pcr 活动
            session.state['op'] = stripped_arg
        return
    
    if not stripped_arg:
        # 用户没有发送有效操作
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('操作不能为空，请重新输入')
    
    session.state[session.current_key] = stripped_arg


