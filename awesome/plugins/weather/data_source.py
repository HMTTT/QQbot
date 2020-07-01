import requests as reqs
import json
import re

async def get_weather_of_city(city: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    zoneID = None
    with open('awesome\plugins\data\zoneID.json', 'r', encoding='utf-8') as f :
        zoneID = json.load(f, strict=False)
    
    msg = ''
    print('in')
    if city not in zoneID:
        msg = '没有这个城市嗷，只能查市，其他没有'
    else:
        html = reqs.get('http://www.weather.com.cn/weather/'+zoneID[city]+'.shtml')
        html.encoding = 'utf-8'
        tems = (re.findall('<li class="sky skyid.*?">.*?<h1>(.*?)</h1>.*?</big>.*?</big>.*?class="wea">(.*?)</p>.*?<p class="tem">(.*?)</p>.*?</li>',html.text, re.DOTALL+re.MULTILINE))
        newLine = '\r\n'
        
        def formatTem(tem):
            t1 = re.findall('<i>(.*?)</i>', tem)
            t2 = re.findall('<span>(.*?)</span>', tem)
            msg = t1[0]
            if len(t2) > 0:
                msg += '~' + t2[0]
            return msg
            
        msg += city + '七天天气来了嗷' + newLine
        for tem in tems:
            msg += tem[0] + '\t' + formatTem(tem[2]) +'\t' + tem[1] + newLine
    return msg