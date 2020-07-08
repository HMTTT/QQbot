from PIL import Image, ImageFont, ImageColor, ImageDraw
import re, time

def createImg(text):
    # 分解信息
    ts = re.findall('([^-]+)', text, re.MULTILINE)

    maxLen = -1
    maxIndex = -1
    for (i, v) in enumerate(ts):
        if len(v) > maxLen:
            maxLen = len(v)
            maxIndex = i
        if len(v) <= 0:
            ts.remove(v)

    items = []
    for t in ts:
        if not re.match(r'^[\n|\r\n]$', t): 
            items.append(re.findall('([^\r\n]+)', t))

    font_size = 60
    maxWidth = len(items[maxIndex][0]) * font_size
    font = ImageFont.truetype('simsun.ttc', font_size)

    height = 0
    ims = []
    
    # 生成单个活动图片
    for item in items:
        im = Image.new('RGBA', (maxWidth, font_size * len(item)), color=(255,255,255))
        draw = ImageDraw.Draw(im)
        for (i, v) in enumerate(item):
            draw.text((0, font_size * i + 1), v, (0,0,0) ,font=font)
        ims.append(im)
        height += im.size[1]

    # 合成活动图片
    h = 0
    span = 60 # 图片上下间隔
    img = Image.new("RGBA", (maxWidth, height + span * (len(ims) + 1)), color=(255,255,255))

    for im in ims:
        img.paste(im,(0, h + span))
        h += im.size[1] + span
    fname = 'myImg/pcr/' + time.strftime("%Y%m%d", time.localtime()) + '.png'
    img.save(f'../CQPro/data/image/{fname}')
    return fname