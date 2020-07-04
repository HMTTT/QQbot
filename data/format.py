import re
import json

def format():
    msg = ''
    with open('./zoneID.txt', 'r', encoding='utf-8') as f :
        msg = (f.readlines())
    
    zList = (re.findall('([\u4e00-\u9fa5]{2}):([0-9]*)', str(msg)))
    zDict = {}
    for z in zList:
        zDict[z[0]] = z[1]
    
    with open('./zoneID.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(zDict, indent=4,ensure_ascii=False))
    
if __name__ == "__main__":
    format()
    print('完成')