import json
import os
import requests as reqs
from awesome.plugins.utils.methods import *

def getMsg():
    i = 0
    html = ''
    while i < 3:
        try:
            html = reqs.get("https://bangumi.bilibili.com/web_api/timeline_global", timeout=5)
            print('爬取新番完成')
            break
        except reqs.exceptions.RequestException:
            i += 1
            print('超时，第 ' + str(i) + ' 次重新尝试')
    
    if html == '':
        return [False, '超时了']
    
    return [True, json.loads(html.text)]
    
def getXinFanMsg(msg, days):
    # 最多显示7天
    if days > 7:
        days = 7
        
    i = 6
    l = i + days
    results = []
    while(i < l):
        obj = msg['result'][i]
        date = obj['date']
        results.append(f'{date} 号的新番:')
        
        # 如果没有新番
        if len(obj['seasons']) <= 0:
            results.append('本日无新番')
            
        for season in obj['seasons']:
            results.append(f'{season["pub_time"]} {season["title"][:8]} {season["pub_index"]}')
        results.append('\r\n')
        i += 1
    print(results)
    return results


def getXinFan(session, op):
    results = getMsg()
    if not results[0]:
        return results[1]
    
    keys = ['days']
    op = op.strip()
    if op != '':
        if not setSessionArgs(getOps(op), keys, session, False):
            return '参数过多，只需要输入一个正整数'
    
    # 天数默认为1
    days = 1
    if 'days' in session.state:
        # 字符串包含数字以外的字符或小于1
        if not session.state['days'].isdigit() or int(days) <= 0:
            return '参数错误，需要输入一个正整数'
        days = int(session.state['days'])
        
    return getXinFanMsg(results[1], days)

def helpMsg(session, op):
    msg = []
    msg.append('bili帮助([]表示可选参数)')
    msg.append('bili 新番 [查看天数]\t查看新番情况')
    msg.append('bili 帮助\t功能帮助')
    return msg

hDict = {}

def initData():
    hDict['新番'] = getXinFan
    hDict['帮助'] = helpMsg

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
    