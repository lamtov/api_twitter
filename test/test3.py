import os
#
#
#
import logging
logging.basicConfig(filename='log.log',level=logging.INFO)
import time
import requests
import re
import sys


def crawl(strat_i, end_i):
    for i in range(strat_i,end_i):
        print(i)
        logging.info(i)
        url = 'http://www.forum.hr/member.php?u='+str(i)
        # payload = {"node_id": "9", "management_ip": "172.16.29.194", "ssh_user": "root", "ssh_password": "1",
        #            "node_display_name": "ctr01"}

        headers_text = ["Host: www.forum.hr",
        "Connection: keep-alive",
        "Upgrade-Insecure-Requests: 1",
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding: gzip, deflate",
        "Accept-Language: en-US,en;q=0.9"]

        headers = {}
        for head in headers_text:
            a= head.split(":")[0]
            b= head.split(":")[1][1:]
            headers[a]=b
        # print(headers)
        # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.get(url,  headers=headers)
        # print(r.text)
        name = re.findall(r'<title>Forum.hr - Pogledaj profil: (.*?)</title>', r.text)
        try:
            if len(name) > 0:
                print(name[0])
                logging.info(name[0])
            else:
                print("invalid")
                logging.info("invalid")
        except:
            print("error")
        # # os.system('curl -X POST "http://172.16.29.194:4321/installation/runtask" -H  "accept: application/json" -H  "Content-Type: application/json"  --data "{\'task_id\':\'1\',\'method\':\'Install\' }"')
        # time.sleep(5)
import sys
import multiprocessing
from multiprocessing import Process
if __name__ == '__main__':
    # freeze_support()
    start = 200000
    end = 2000000

    manager = multiprocessing.Manager()
    res = manager.dict()
    proc = []

    dict=[]
    d = int((end-start)/12)
    for i in range(0,12):
        a1 = start+i*d
        a2 = start+(i+1)*d
        a2 = end if a2 >end else a2
        dict.append((a1,a2))
    print(dict)
    for d in dict:
        print("h1")
        func = getattr(sys.modules[__name__], 'crawl')
        p = Process(target=func, args=tuple(d, ))
        print("h3")
        p.start()
        proc.append(p)
    for p in proc:
        p.join()