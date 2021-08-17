# !/usr/bin/python3
# -*- coding:utf-8 -*-
# author: Pan3a
# time: 2021/8/15
from prettytable import PrettyTable
from time import strftime,localtime,sleep
from base64 import b64encode
from requests import get
import sys
import os


class Fofa:
    def __init__(self):
        self.Headers = {
            'Authorization':'eyJhbGciOiJIUzUxMiIsImtpZ......',
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
        print(self.ORANGE +
            "python3 FoFaSearch.py --cookie=xxxx "
            "--query=app=\\\"thinkphp\\\" "
            "--start=1 "
            "--end=2 "
            "--number=1,3,5 "
            "--filepath=/home/pan3a/Desktop/thinkphp.txt"
            + self.ORANGE
              )
        print(table)

    def InitVar(self):
        if len(sys.argv) >=6:
            for v in sys.argv:
                if v[0:8] == '--cookie':
                    self.Headers['Authorization'] = v.split("=")[1]
                elif v[0:7] == '--query':
                    self.query = b64encode(v[8:].encode("UTF-8")).decode('UTF-8')
                elif v[0:7] == '--start':
                    self.start = int(v.split("=")[1])
                elif v[0:5] == '--end':
                    self.end = int(v.split("=")[1])
                elif v[0:8] == '--number':
                    self.tmp = []
                    if v[-1] == ',':
                        self.number = v[9:-1].split(',')
                    else:
                        self.number = v[9:].split(",")
                    for n in self.number:
                        self.tmp.append(self.assets[int(n)-1])
                elif v[0:10] == '--filepath':
                    self.filepath = v.split("=")[1]
                else:
                    self.filepath = ""
        # elif len(sys.argv) < 7:
        #     exit(self.RED + "参数过少!!" + self.RED)
        else:
            exit(self.RED + "参数不对!!" + self.RED)

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
                    if self.filepath != "":
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
