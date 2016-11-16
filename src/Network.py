# coding=gbk
'''
Created on 2016年10月20日

@author: dqd
'''
import subprocess
import re

lost_rate_match = re.compile('(\d+)%')
time_match = re.compile('=\s(\d+)ms')
        
def _runping(ip):
    ping_ori_result = _getping(ip).decode("gbk")
    temp = _getresult(ping_ori_result)
    result = []
    if len(temp) > 0:
        result.append(int(temp[0][0]))
    if len(temp) > 1 and len(temp[1]) > 2:
        result.append(int(temp[1][2])) 
    return result

def _getping(ip):
    ping_command = 'ping  %s' % (ip)
    ping = subprocess.Popen(ping_command,
                            stdin = subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE,
                            shell = True)
    return ping.stdout.read()   

def _getresult(context):
    lost_rate = lost_rate_match.findall(context)
    time_result = time_match.findall(context)
    return [lost_rate,time_result] 
 
if __name__ == '__main__':
    ip = 'JPA.ISS.TF'
    result = _runping(ip)
    print(result)       