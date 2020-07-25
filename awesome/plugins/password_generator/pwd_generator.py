from awesome.plugins.utils.methods import *

pwd_code = 14159265354979
num=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
alphabet=('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
          'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
          's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A',
          'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
          'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
sign=('_','/','?','!')

def juge_op(op):
    flag = True
    words = list(op)
    _range = num + alphabet
    for word in words:
        if not word in _range:
            flag = False
            break
    return flag

def get_password_type(session):
    '''
    引导用户选择密码类型
    :param session:
    :return: str:x-y
    '''
    pwd_type = "请输入格式为x-y的短码表示你需要的密码类型\r\n" + \
               "其中x为一个整数代表你需要的密码长度\r\n" + \
               "y为一个的字母对应着一种密码类型\r\n" + \
               "密码类型有如下几种：\r\n" + \
               "n:只由数字组成\r\n" + \
               "a:只由数字和大小写字母组成\r\n" + \
               "b:由数字、大小写字母以及部分特殊符号（'_','/','?','!'）组成\r\n" + \
               "c:由数字和大小写字母组成并以字母开头\r\n" + \
               "d:由数字、大小写字母以及部分特殊符号（'_','/','?','!'）组成且由字母开头\r\n"
    password_type = session.get('password_type', prompt=pwd_type)
    return password_type

def explain_args_0(arg):
    '''
        :param arg: args[0] 用于生成密码的短语
        :return: 对应的十进制的值
        '''
    words = list(arg)
    words = words[::-1]
    _range = num + alphabet
    temperator = 0
    i = 0
    for word in words:
        temperator += _range.index(word) * (10 + 26 + 26) ** i
        i += 1
    return temperator

def explain_args_1(arg):
    '''
    解析args[1] 对应密码的类别
    :param arg:args[1] 密码的类别码，x-y
    :return: [x:int,y:str]
    '''
    arg=arg.split('-')
    return [int(arg[0]),arg[1]]


def generate(sentence,length,_range):
    '''
    :param sentence: 用于生成密码的短句转换的数值
    :param length: 所要求的密码的短句
    :param _range: 字符来源
    :return: pwd_list 目标密码对应的列表
    '''
    pwd_list = []
    sentence *= pwd_code
    # 初步生成密码
    while sentence > len(_range):
        pwd_list.append(_range[sentence%len(_range)])
        sentence = int(sentence / len(_range))
    pwd_list.append(_range[sentence%len(_range)])

    # 确保密码的长度
    while len(pwd_list) < length:
        pwd_list += pwd_list[::length%3]
    # 截取需要的长度
    pwd_list = pwd_list[:length]
    return pwd_list

def pwd_modification(pwd_list,length,pwd_type_code):
    '''
    对密码做最后的修饰、调整
    :param pwd_list:  密码列表（将密码按位拆分
    :param length: 密码的长度，辅助一些调整
    :param pwd_type_code: 一个字母，对应密码类型
    :return: str 最终的密码
    '''
    # 就当你密码长度大于4了
    if len(pwd_list) > 4:
        # 判断密码是否含有数字,如果没有，将第二位（1）修改为数字
        flag = True
        for word in pwd_list[4:]:
            if word in num:
                flag = False
                break
        if flag :
            pwd_list[1] = num[(length ^ pwd_code) % len(num)]

        # 判断密码是否需要含有字母
        if pwd_type_code in ['a','b','c','d']:
            # 判断是否含有字母，如无，将第三位（2）修改为字母
            flag = True
            for word in pwd_list[4:]:
                if word in alphabet:
                    flag = False
                    break
            if flag:
                pwd_list[2] = alphabet[(length ^ pwd_code) % len(alphabet)]

        # 判断密码是否需要含有特殊符号（'_','/','?','!'）
        if pwd_type_code in ['b','d']:
            # 判断密码里是否包含特殊符号，如无，将第四位（3）修改为特殊符号
            flag = True
            for word in pwd_list[4:]:
                if word in sign:
                    flag = False
                    break
            if flag:
                pwd_list[2] = sign[(length ^ pwd_code) % len(sign)]

        # 判断是否需要字母开头
        if pwd_type_code in ['c','d']:
            #判断是否是字母开头 如没有，改之
            if pwd_list[0] not in alphabet:
                pwd_list[0] = alphabet[(length * pwd_code) % len(alphabet)]

    # 将列表转换为字符串返回
    return ''.join(pwd_list)


def get_pwssword(args):
    '''
    :param args: [用于生成密码的短句,[长度,类型]]
    :return: pwd 生成的密码
    '''
    sentence = explain_args_0(args[0])
    val2 = explain_args_1(args[1])
    length = val2[0]
    _range = ''
    pwd=''
    pwd_list = []
    if val2[1] == 'n':
        # n:只由数字组成
        _range = num
        pwd_list = generate(sentence,length,_range)
        pwd = pwd_modification(pwd_list, length, val2[1])
    elif val2[1] == 'a':
        # a:只由数字和大小写字母组成
        _range = num + alphabet
        pwd_list = generate(sentence,length,_range)
        pwd = pwd_modification(pwd_list, length, val2[1])
    elif val2[1] == 'b':
        # b: 由数字、大小写字母以及部分特殊符号（'_', '/', '?', '!'）组成
        _range = num + sign + alphabet
        pwd_list = generate(sentence,length,_range)
        pwd = pwd_modification(pwd_list, length, val2[1])
    elif val2[1] == 'c':
        # c: 由数字和大小写字母组成并以字母开头
        _range = num + alphabet
        pwd_list = generate(sentence,length,_range)
        pwd = pwd_modification(pwd_list, length, val2[1])
    elif val2[1] == 'd':
        # d: 由数字、大小写字母以及部分特殊符号（'_', '/', '?', '!'）组成且由字母开头
        _range = num + sign + alphabet
        pwd_list = generate(sentence, length, _range)
        pwd = pwd_modification(pwd_list, length, val2[1])
    else: return False
    return pwd

def pwd_generator(op, session) -> str:
    '''
    用于生成一个符合要求的密码
    :param op: 字符串，用于生成密码的参数
    :param session: CommandSession
    :return:  pwd 返回生成的密码
    '''
    # remove ' '
    op = op.strip()
    args = op.split(' ', 1)

    # 封装用户输入的两个参数
    # 判断用户有没有选择密码类型，如没有，引导其选择
    if len(args) < 2:
        args.append(get_password_type(session))

    # 生成密码
    pwd = get_pwssword(args)
    return  pwd
