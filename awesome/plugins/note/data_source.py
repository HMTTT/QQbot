import json
import os
from awesome.plugins.utils.methods import *


def getQQ(session):
    return str(session.ctx['sender']['user_id'])

def getMsg(qq):
    path = './data/note/' + qq + '.json'
    if not os.path.exists(path):
        return {}
    else:
        tmp = {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                tmp = json.load(f)
        except Exception:
            pass
        return tmp

def writeMsg(qq, msg):
    path = './data/note/' + qq + '.json'
    try:
        with open(path,'w',encoding='utf-8') as f:
            json.dump(msg, f, ensure_ascii=False)
        return True
    except Exception:
        return False

def addNote(session, op):
    keys = ['addTitle', 'addContent']
    if op != '':
        setSessionArgs(op.split(' '), keys, session, True)
    addTitle = session.get('addTitle',prompt='输入要添加的标题[-c]取消:')
    
    if addTitle == '-c':
        return '操作已取消'
    
    addContent = session.get('addContent', prompt='输入想要添加的内容：')
    
    qq = getQQ(session)
    msg = getMsg(qq)
    msg[addTitle] = addContent
    print(msg)
    if writeMsg(qq, msg):
        return '添加成功'
    else:
        return '添加失败'

def delNote(session, op):
    msg = getMsg(str(session.ctx['sender']['user_id']))
    if len(msg.keys()) <= 0 :
        return '没有记录可以删除，请先添加'
        
    keys = ['delTitle']
    if op != '':
        setSessionArgs(op.split(' '), keys, session, True)
        
    delTitle = session.get('delTitle', prompt='请输入要删除的标题(输入[-c]可以取消此操作)：')
    
    delTitle = delTitle.strip()
    if delTitle == '-c':
        return '删除已取消'
        
    if delTitle in msg.keys():
        del msg[delTitle]
        try:
            writeMsg(getQQ(session), msg)
        except Exception:
            return '删除失败，请稍后重试'
            
        return '删除' + delTitle + '成功'
    else:
        return '没有这个记录，可以使用[note v]查看'
      
def insertNote(session, op):
    keys = ['addTitle', 'insertContent']
    if op != '':
        setSessionArgs(op.split(' '), keys, session, True)
        
    addTitle = session.get('addTitle', prompt='请输入要插入的标题，输入[-c]可取消操作:')
    if addTitle == '-c':
        return '操作已取消'
    msg = getMsg(getQQ(session))
    if addTitle not in msg.keys():
        flag = session.get('flag', prompt='未找到该标题，是否直接添加？(Y/N)')
        flag = flag.strip()
        if flag.lower() == 'y':
            return addNote(session, op)
        else:
            return '添加操作已取消'
    else:
        insertContent = session.get('insertContent', prompt='请输入要添加的内容(输入[-c]可以取消此操作)：')
        insertContent = insertContent.strip()
        if insertContent == '-c':
            return '操作已取消'
        
        if type(msg[addTitle]) is not  list:
            msg[addTitle] = [msg[addTitle]]
        msg[addTitle].append(insertContent)
        if writeMsg(getQQ(session), msg):
            return '信息插入成功'
        else:
            return '信息插入失败'
            
        

def viewNote(session, op):
    msg = getMsg(str(session.ctx['sender']['user_id']))
    op = op.strip()
    
    keys = ['viewTitle']
    if op != '':
        setSessionArgs(op.split(' '), keys, session, True)
    viewTitle = session.get('viewTitle',prompt='输入要查看的标题(输入[-all]可查看全部记录标题):')
    
    viewTitle = viewTitle.strip()
    if viewTitle == '-all':
        if len(msg.keys()) <= 0:
            return '没有记录，要先添加'
        return msg.keys()
    
    if viewTitle not in msg.keys():
        return '没有这个记录'
    else:
        return msg[viewTitle]

def helpNote(session, op):
    msg = []
    msg.append('note帮助([]表示可选参数)')
    msg.append('note add [记录名]\t添加记录')
    msg.append('note v [记录名]\t查看记录')
    msg.append('note del [记录名]\t删除记录')
    msg.append('note i [记录名]\t插入记录')
    msg.append('note 帮助\t功能帮助')
    return msg

hDict = {}

def initData():
    hDict['add'] = addNote
    hDict['v'] = viewNote
    hDict['del'] = delNote
    hDict['i'] = insertNote
    hDict['帮助'] = helpNote

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
    