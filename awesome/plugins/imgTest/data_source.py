import json
import os
import requests as reqs
from awesome.plugins.utils.methods import *


def helpMsg(session, op):
    msg = []
    msg.append('img 帮助\t功能帮助')
    return msg

def sendImg(session, op):
    return '[CQ:image,file=myImg/IMG_001.png]'

hDict = {}

def initData():
    hDict['img'] = sendImg
    
async def handleOp(op, session) -> str:
    initData()
    # 去除前后空格
    op = op.strip()
    args = op.split(' ', 1)

    # 如果没有第二个参数就添加一个，保持数据一致
    if len(args) < 2:
        args.append('')
    msg = None
    
    if args[0] in hDict.keys():
        msg = hDict[args[0]](session, args[1])
    else:
        msg="没有这个操作，请确认后重试"
    return msg
    