from nonebot import on_command, CommandSession
import requests as reqs
import json
import datetime
from collections import Counter
from .pcrUtils import *

newLine = '\r\n'

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


async def get_msg(op) -> str:
    i = 0
    html = ''
    while i < 3:
        try:
            html = reqs.get("https://pcredivewiki.tw/static/data/event.json", timeout=5)
            print('爬取完成')
            break
        except reqs.exceptions.RequestException:
            i += 1
            print('超时，第 ' + str(i) + ' 次重新尝试')
    
    if html == '':
        return '超时了'

    msg = (json.loads(html.text))
    newLine = '\r\n'
    date_now = datetime.datetime.now()
    results = []
    for huodongItem in msg:
        end_time = datetime.datetime.strptime(huodongItem['end_time'],'%Y/%m/%d %H:%M')
        if (end_time - date_now).days > 0 :
            text = ''
            text += huodongItem['campaign_name'] + newLine
            text += 'S：' + huodongItem['start_time'] + newLine
            text += 'E：' + huodongItem['end_time'] + newLine
            text += '-------------------------' + newLine
            results.append(text)
    return results

# 人物名单
async def getRoleNames(op):
    names = getNames()
    results = []
    results.append('人物名单：' + newLine)
    for n in names:
        results.append(n + newLine)
    return results

# 详细信息
async def getRoleMsg(op):
    # 去左右空格
    name = op.strip()
    k = isTrueName(name)
    if k is not None :
        roleMsg = getData()['roleMsg']
        role = roleMsg[k]
        msg = ''
        msg += f'姓名 : {name}' + newLine
        msg += f'年龄 : {role["age"]}' + newLine
        msg += f'生日 : {role["birth_month"]}月{role["birth_day"]}日' + newLine
        msg += f'身高 : {role["height"]}' + newLine
        msg += f'体重 : {role["weight"]}' + newLine
        msg += f'血型 : {role["blood_type"]}' + newLine
        msg += f'座右铭 : {role["catch_copy"]}' + newLine
        msg += f'爱好 : {role["favorite"]}' + newLine
        msg += f'所属公会 : {role["guild"]}' + newLine
        msg += f'自我介绍 : {role["self_text"]}' + newLine
        msg += f'声优 : {role["voice"]}'
        return msg
    else:
        return '没有叫' + name + '的角色，名字要用繁体嗷，可以用[pcr 名单]查询，建议私聊'


# 帮助
async def getHelp(op):
    msg = '操作有 [] 中的是可选参数：' + newLine
    msg += '活动' + newLine
    msg += '人物详细 人物名' + newLine
    msg += '名单' + newLine
    msg += 'rank 人名 rank值 [rank值]' + newLine
    msg += '帮助' + newLine
    return msg

'''
输出多个rank信息进行比较
Rank 开始rank 结束rank
'''

def isRank(rank):
    if not rank.isdigit():
        return False
        
    r = int(rank)
    if r >= 2 and r <= 17:
        return True
        
    return False

# 如果名字存在返回 id_名字，否则返回None
def isTrueName(name):
    roleMsg = getData()['roleMsg']
    pid = findIdByName(name)
    k = f'{pid}_{name}'
    if k in roleMsg.keys():
        return k
    else:
        return None

'''
accuracy 命中
atk 物理攻击
def 物理防御
dodge 闪避
energy_recovery)rate tp上升
energy_reduce_rate tp减轻消耗
hp 生命
hp_recovery_rate 回复量上升
life_steal_hp吸收
magic_critical 魔法暴击
magic_def 魔法防御
magic_penetrate 魔法穿透
magic_str 魔法攻击
physical_critical 物理暴击
physical_penetrate 物理穿透
wave_energy_recovery tp自动恢复
wave_hp_recovery hp自动恢复

accuracy_growth 命中每级提升
atk_growth 物理攻击每级提升
def_growth 物理防御每级提升
dodge_growth 闪避每级提升
'''

attrs = {
    'accuracy': '命中',
    'atk' : '物理攻击',
    'def' : '物理防御',
    'dodge' : '闪避',
    'energy_recovery_rate' : '魔力上升',
    'energy_reduce_rate' : '魔力减轻消耗',
    'hp' : '生命',
    'hp_recovery_rate' : '回复量上升',
    'life_steal': '生命吸收',
    'magic_critical' : '魔法暴击',
    'magic_def' : '魔法防御',
    'magic_penetrate' : '魔法穿透',
    'magic_str' : '魔法攻击',
    'physical_critical' : '物理暴击',
    'physical_penetrate' : '物理穿透',
    'wave_energy_recovery' : '魔力自动恢复',
    'wave_hp_recovery' : '生命自动恢复'
}

def getARank(name, rank):
    if not isRank(rank):
        return 'rank值不对，请输入2-16的整数',None
    
    id_name = isTrueName(name)
    if id_name is None:
        return '没有叫' + name + '的角色，名字要用繁体嗷，可以用[pcr 名单]查询，建议私聊',None
    
    # 格式为id_name
    tmp = id_name.split('_')
    # 获取id
    pid = tmp[0]
    
    rank = int(rank)
    data = getData()
    roleRank = data["roleRankMsg"]
    k1 = f'{pid}_{rank}'
    k2 = f'{pid}_{rank+1}'
    
    # 当前rank强化满级 = 2 * (rank+1级总提升 - rank总提升)
    rankMax = (dictCalculate(
        roleRank[k2], 
        roleRank[k1], 
        roleRank[k1].keys(),
        lambda x1,x2 : 2 * (float(x1)-float(x2))))
        
    # 角色属性和属性提升
    rolePromotion = data['rolePromotion']
    kp = f'{pid}_5'
    
    def rolePromotionTotal(d, keys):
        nd = {}
        for k in keys:
            if k in d.keys():
                nd[k] = float(d[k])
            else:
                nd[k] = 0.0
            
            k_growth = f'{k}_growth'
            if  k_growth in d.keys():
                nd[k] += float(d[k_growth]) * config['max_level']
        return nd
    
    # 五星角色满级属性 
    roleValue = (rolePromotionTotal(rolePromotion[kp], roleRank[k1].keys()))
    
    result = {}
    for k in attrs.keys():
        result[k] = float(roleRank[k1][k]) + rankMax[k] + roleValue[k]
        
    return [result], result

# 获得一个范围内的rank
def getRanks(name, rank1, rank2):
    if not isRank(rank1) or not isRank(rank2):
        return None, 'rank值不对，请输入2-16的整数'
        
    rank1 = int(rank1)
    rank2 = int(rank2)
    rs = -1
    re = -1
    
    if rank1>rank2:
        rs = rank2
        re = rank1
    else:
        rs = rank1
        re = rank2

    results = []
    index = rs
    while(index <= re):
        r = getARank(name, str(index))
        if r[1] is None:
            return None, r[0]
            
        results.append(r[1])
        index += 1

    return results
    
async def getRank(op):
    # 去前后空格
    op = op.strip()
    # 分割
    args = op.split(' ', 2)
    l = len(args)
    if l >= 2:
        results = None
        if l == 2:
            # 只有一个Rank 直接返回
            results = getARank(args[0], args[1])
            if results[1] is None:
                return results[0]
            else:
                results = results[0]
        elif l == 3:
            # 有两个Rank 输出范围内的Rank
            results =  getRanks(args[0], args[1], args[2])
            if results[0] is None:
                return results[1]

         
        if results is not None:
            rs = []
            for attr in attrs:
                msg = '{0:{1}<7}'.format(attrs[attr],chr(12288))
                for r in results:
                    msg += '{0:<10.1f}'.format(r[attr])
                msg += newLine
                rs.append(msg)
            rs.append(f'五星，装备满强，无专武，无羁绊，满级LV{config["max_level"]}')
            return rs
    # 参数数量错误
    return '参数错了嗷， 要输入名字和一个或两个Rank值'


# 字典运算
def dictCalculate(d1, d2, keys, cal):
    d = {}
    for k in keys:
        d[k] = cal(d1[k], d2[k])
    return d

hDict = {
    '活动':get_msg,
    '人物详细':getRoleMsg,
    '名单':getRoleNames,
    '帮助':getHelp,
    'rank':getRank
}

async def handleOp(op) -> str:
    # 去除前后空格
    op = op.strip()
    args = op.split(' ', 1)

    # 如果没有第二个参数就添加一个，保持数据一致
    if len(args) < 2:
        args.append('')
    msg = None
    
    if args[0] in hDict.keys():
        # 初始化数据
        initData()
        msg = await hDict[args[0]](args[1])
    else:
        msg="没有这个操作，请确认后重试"
    return msg