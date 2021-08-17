# !/usr/bin/python
# -*- coding:utf-8 -*-
# author: Pan3a
# time: 2021/8/15
from prettytable import PrettyTable
from time import strftime,localtime,sleep
from base64 import b64encode
from requests import get
import os

class Fofa:
    def __init__(self):
        self.Headers = {
            'Authorization':'eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6Mzk5OTQsIm1pZCI6MTAwMDI4Mjc2LCJ1c2VybmFtZSI6Iuaeq-mbqiIsImV4cCI6MTYyOTEzMzI1Ny45OTMwMzYsImlzcyI6InJlZnJlc2gifQ.RmvyaQV0aq3m3SheCu2_0hFk5XhqfkA2s-_yhbqcbSsLWTU1abvYPeB07IQYIj9MRGxYVs6SLLbxUCC8HN54Fg',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
        }
        self.URL = 'http://api.fofa.so/v1/search?'
        self.Color()
        self.Banner()
        self.InitVar()

    def Color(self):
        self.RED = "\033[0;31m"
        self.BLUE = "\033[94m"
        self.GREEN = "\033[32m"
        self.ORANGE = "\033[33m"

    def Banner(self):
        self.assets = ['asn_org','banner','city','country','domain','icp','ip','link','os','server','title','port',]
        self.explain = ['组织','banner','城市','国家','域名','ICP备案号','IP地址','链接','系统类型','容器类型','网站标题','端口',]
        table = PrettyTable(['编号','名称','解释'])
        for number,key in enumerate(self.assets):
            table.add_row([number+1,key,self.explain[number]])
        print(table)

    def InitVar(self):
        query = input(self.GREEN + "input query:" + self.GREEN)
        self.query = b64encode(query.encode("UTF-8")).decode('UTF-8')
        response = get(url=self.URL + "qbase64=" + self.query + "&ps=1&ps=10").json()
        self.Headers['Authorization'] = input(self.GREEN + "input auth:" + self.GREEN)
        total = response["data"]["page"]["total"]
        if total % 10 ==0:
            AllPage = total // 10
        else:
            AllPage = total // 10 +1
        print( self.NowTime() + "total:" + str(total) + "\t" + "AllPage:" + str(AllPage))
        self.start = int(input(self.GREEN + "input start:" + self.GREEN))
        self.end = int(input(self.GREEN + "input end:" + self.GREEN))
        self.number = input(self.GREEN + "input number:" + self.GREEN).split(',')
        self.tmp = []
        if self.number[-1] == "":
            self.number.pop(-1)
        for n in self.number:
            self.tmp.append(self.assets[int(n)-1])
        self.filepath = input(self.GREEN + "input filepath:" + self.GREEN)

    def Request(self):
        try:
            for page in range(self.start,self.end+1,1):
                print(self.GREEN +  self.URL + "qbase64=" + self.query + "&pn=" + str(page) + "&ps=10" + self.GREEN)
                response = get(url=self.URL + "qbase64=" + self.query + "&pn=" + str(page) + "&ps=10",headers=self.Headers)
                response.encoding = response.apparent_encoding
                jsondata = response.json()
                for i in range(len(jsondata["data"]["assets"])):
                    tmp = ''
                    print("-"*70)
                    for data in self.tmp:
                        if type(jsondata["data"]["assets"][i][data]) == type([]) and len(jsondata["data"]["assets"][i][data]) == 1:
                            print(self.BLUE + self.NowTime() + data + "\t" + jsondata["data"]["assets"][i][data][0]["name"] + self.BLUE)
                            tmp += jsondata["data"]["assets"][i][data][0]["name"]
                        else:
                            print(self.BLUE + self.NowTime() + data + "\t" + str(jsondata["data"]["assets"][i][data]) + self.BLUE)
                            tmp += str(jsondata["data"]["assets"][i][data]) + "\t"
                    # print(tmp)
                    if self.filepath:
                        self.WriteFile(tmp + "\n")
                sleep(2)
        except Exception as e:
            print(self.RED + str(e) + self.RED)

    def WriteFile(self,data):
        if os.path.exists(self.filepath):
            with open(self.filepath,'a') as file:
                file.write(data)
        else:
            files = open(self.filepath,'w')
            files.close()
            with open(self.filepath,'a') as file:
                file.write(data)

    def NowTime(self):
        return self.BLUE +  "[+] " + strftime("%H:%M:%S",localtime()) + "\t" + self.BLUE

if __name__ == '__main__':
    fofa = Fofa()
    fofa.Request()
