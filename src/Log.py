# coding=gbk
'''
Created on 2016��10��20��

@author: dqd
'''
import time
        
def writeLog(logPath, logContent):
    with open(logPath, "a+") as fp:
        fp.write('['+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+']')
        fp.write("  ")
        fp.write(logContent)
        fp.write('\n')

if __name__ == '__main__':
    path = '../../log.txt'
    writeLog(path,"this is a test")