# coding=gbk
'''
Created on 2016年10月20日

@author: dqd
'''

import urllib.request
from bs4 import BeautifulSoup


def getAccountInfo(url):
    fp = urllib.request.urlopen(url)
    pagehtml = fp.read()
    bs = BeautifulSoup(pagehtml,"html.parser")
    divs = bs.find_all("div",class_="col-sm-4 text-center")
    result = []
    for div in divs[0:3]:
        i = 0
        item = []
        for child in div.children:
            if i < 8 and child.string.strip() != "":
                item.append(child.string.split(':')[1])
            i = i + 1
        result.append(item)
    return result
        
    
if __name__ == '__main__':
    url = "http://www.ishadowsocks.org/"
    result = getAccountInfo(url)
    print(result)
