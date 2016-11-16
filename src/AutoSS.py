# coding=gbk
'''
Created on 2016年10月20日

@author: dqd
'''
import Log
import Network  #module class different
import Spider 
import sys
import json
import time
import os
import win32com.client
import subprocess 

def selectAccount(accountInfos):
    lostRate = []
    avgTime = []
    for account in accountInfos:
        netinfo = Network._runping(account[0])
        lostRate.append(netinfo[0])
        if len(netinfo) > 1:
            avgTime.append(netinfo[1])
        else:
            avgTime.append(sys.maxsize)
    minRate = min(lostRate)
    minAvgTime = sys.maxsize
    minIndex = -1
    for i in range(len(lostRate)):
        if lostRate[i] == minRate:
            if avgTime[i] < minAvgTime:
                minAvgTime = avgTime[i]
                minIndex = i
    accountInfos[minIndex].append(minAvgTime)
    return accountInfos[minIndex]
    
def checkJson(logFile, filePath, account):
    with open (filePath, 'r') as fp:
        content = json.load(fp)
        if content['configs'][0]['server'] == account[0] and content['configs'][0]['password'] == account[2]:
            Log.writeLog(logFile, "account info have not changed:'"+account[0]+"'")
            return True
        return False

def updateJson(logFile, filePath, account):
    with open(filePath, "r") as fr:
        content = json.load(fr)
        content['configs'][0]['server'] = account[0]
        content['configs'][0]['server_port'] = int(account[1])
        content['configs'][0]['password'] = account[2]
        content['configs'][0]['method'] = account[3]
        content['enabled'] = True
        content['isDefault'] = True
        changeStr = json.dumps(content)
        with open(filePath, "w") as fw:
            result = fw.write(changeStr)
            if result > 0:
                initlogcontent = "success updating account info:'"+account[0]+"'"
                logcontent =  initlogcontent+" : "+str(account[4])+"ms"
                Log.writeLog(logFile, logcontent)
                return 
            Log.writeLog(logFile, "fail to update account info:'"+account[0]+"'")
            return

def readConfig(argList):
    #create or read config file
    if not os.path.exists('../config.json'):   
        with open('../config.json', 'w') as fp:
            content = {}
            content['url'] = argList[0]
            content['ssConfigPath'] = argList[1]
            content['logPath'] = argList[2]
            content['exePath'] = argList[3]
            content['interval'] = argList[4]
            contentStr = json.dumps(content)
            fp.write(contentStr)
    else:
        with open('../config.json', 'r') as fp:
            content = json.load(fp)
            argList[0] = content['url']
            argList[1] = content['ssConfigPath']
            argList[2] = content['logPath']
            argList[3] = content['exePath']
            argList[4] = content['interval']

#check thread exist, if not boot up soft
def bootup(logFile, softPath):
    starttime = 3
    while starttime > 0:
        if not checkExeStatus(logFile):
            starttime -= 1
            subprocess.Popen(softPath,
                             stdin = subprocess.PIPE,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             shell = False)
            time.sleep(15)
        else:
            Log.writeLog(logFile, "success booting up shadowsocks")
            return
            
    Log.writeLog(logFile, "fail to boot up shadowsocks")
    return

def reboot(logFile, softPath):
    if checkExeStatus(logFile):
        os.system('taskkill /im  Shadowsocks.exe /f')
        time.sleep(5)
    subprocess.Popen(softPath,
                     stdin = subprocess.PIPE,
                     stdout = subprocess.PIPE,
                     stderr = subprocess.PIPE,
                     shell = False)
    time.sleep(15)
    Log.writeLog(logFile, "reboot shadowsocks")
    return
    
def checkExeStatus(logFile):
    processName = 'Shadowsocks.exe'
    try:
        WMI = win32com.client.GetObject('winmgmts:') 
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % processName)
    except Exception as e:
        Log.writeLog(logFile, e)
        
    if len(processCodeCov) == 0:
        Log.writeLog(logFile, "shadowsocks is  down, trying to bootup")
        return False
    return True
    
if __name__ == "__main__":
    
    url = "http://www.ishadowsocks.org/"
    jsonFile = '../Shadowsocks-2.5.8/gui-config.json'
    logFile = '../runtime.log'
    exeFile = '../Shadowsocks-2.5.8/Shadowsocks.exe'
    interval = 300 #s
    argList = [url, jsonFile, logFile, exeFile, interval]
    readConfig(argList) 
    url = argList[0]
    jsonFile = argList[1]
    logFile = argList[2]
    exeFile = argList[3]
    interval = argList[4]  
    bootup(logFile, exeFile)           
    
    while True:
        if not checkExeStatus:
            bootup(logFile, exeFile)
        readConfig(argList)
        accountInfos = Spider.getAccountInfo(url)
        selectedAccount = selectAccount(accountInfos)
        if not checkJson(logFile, jsonFile, selectedAccount):
            updateJson(logFile, jsonFile, selectedAccount)
            reboot(logFile, exeFile)
        time.sleep(interval)
    
            
            
    
    
    
    
    
    
    
    
        
    