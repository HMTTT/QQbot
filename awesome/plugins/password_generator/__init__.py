from nonebot import on_command, CommandSession
from .pwd_generator import *

@on_command('generate_pwd', aliases=('生成密码', '密码'))
async def generate_pwd(session:CommandSession):
    op = session.get('op', prompt='请输入你用于生成密码的短句（仅包含字母数字）'+
                                  '，长度不短于5')
    msg='为你生成的密码为：'+ pwd_generator(op, session) +'\r\n'+\
        '你用于生成密码的短语为'+op+',请记住他，\r\n' +\
        '你可以随时用该短语再次获得你的此密码。'
    await session.send(msg)



@generate_pwd.args_parser
async def _(session: CommandSession):
    # 去空格
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            if len(stripped_arg) < 5 and not juge_op(stripped_arg):
                # 用户没有发送有效的短句（而是发送了空白字符或短于5或包含字母与数字外的内容），
                # 则提示重新输入
                # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
                session.pause('输入无效，可能是你输入的短句太短，请重新输入')
            # 第一次运行参数不为空，意味着用户直接将短句跟在命令名后面，作为参数传入
            # 例如用户可能发送了：密码 aaa111
            session.state['op'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('输入无效，请重新输入s')


    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg
