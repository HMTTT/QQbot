# 公主链接的一些工具类，用来辅助读取数据
import json

# 配置文件
config = {
    "max_level" : 157,
    "rolePromotionPath" : "./data/pcr/角色属性.txt",
    "roleMsgPath" : "./data/pcr/角色详细信息.txt",
    "roleRankMsgPath" : "./data/pcr/角色Rank总提升.txt"
}

global data 
data = {}

# 获取数据
def getJsonFromPath(path):
    tmp = None
    with open(path, 'r', encoding='utf-8') as f:
        tmp = json.load(f)
    return tmp

# 辅助initData的方法
def formatData(data, f) -> dict:
    newData = {}
    for d in data:
        k,v = f(d)
        newData[k] = v
    return newData

# 初始化数据
def initData():
    data["rolePromotion"] = getJsonFromPath(config['rolePromotionPath'])
    data["roleMsg"] = getJsonFromPath(config['roleMsgPath'])
    data["roleRankMsg"] = getJsonFromPath(config['roleRankMsgPath'])
    
    def initRankMsg(d):
        # id rank
        return d['unit_id'] + '_' + d['promotion_level'], d
    
    def initMsg(d):
        # id 名字
        return d['unit_id'] + '_' + d['unit_name'],d
        
    def initPromotion(d):
        # id 星级
        return d['unit_id'] + '_' + d['rarity'], d
    
    def initNameToId(d):
        strs = d.split('_')
        # id
        return strs[1], strs[0]
    
    data["rolePromotion"] = formatData(data["rolePromotion"], initPromotion)
    data["roleMsg"] = formatData(data["roleMsg"], initMsg)
    data["roleRankMsg"] = formatData(data["roleRankMsg"], initRankMsg)
    data["nameToId"] = formatData(data["roleMsg"].keys(), initNameToId)

# 用名字查找id，需要繁体
def findIdByName(name):
    nameToId = data["nameToId"]
    if name in nameToId.keys():
        return nameToId[name]
    else:
        return None

# 角色Rank总提升
def getRankMsg(pid, rank):
    k = f"{pid}_{rank}"
    return (data["roleRankMsg"][k])

# 角色属性提升 
def getPromotion(pid, star):
    k = f"{pid}_{star}"
    return data["rolePromotion"][k]
    
# 角色详细信息
def getMsg(pid, pname):
    k = f"{pid}_{pname}"
    return data["roleMsg"][k]

# 获取所有名字，繁体
def getNames():
    return data["nameToId"].keys()

# 获取data
def getData():
    if len(data.keys()) <= 0:
        print('初始化data')
        initData()
    return data

if __name__ == "__main__":
    print(getData())