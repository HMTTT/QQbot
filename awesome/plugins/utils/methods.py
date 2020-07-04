import re

'''
用来帮助设置参数
args：参数的值
keys：参数的名字
session：设置参数的对象
format_args：是否在当参数的值多于参数名时把多的参数进行合并
'''
def setSessionArgs(args, keys, session, format_args=True):
    len_args = len(args)
    len_keys = len(keys)
    if len_args > len_keys and not format_args:
        return False # 表示参数值数量多于参数名
    
    if len_args > len_keys:
        i = len_keys
        while(i < len_args):
            args[len_keys - 1] += ' ' + args[i]
            i += 1
        args = args[:len_keys]
        
    for index, arg in enumerate(args):
        session.state[keys[index]] = arg
        
    return True
    
def getOps(op):
    return re.findall('[^ ]+', op)