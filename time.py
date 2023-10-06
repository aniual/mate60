from datetime import datetime

import time

import requests


class timeTaobao(object):
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    timeNum = int(x['data']['t'])

    def funcname(self):
        taobao_time = datetime.fromtimestamp(self.timeNum / 1000)
        # timeStamp = float(timeTaobao.timeNum / 1000)
        # timeArray = time.localtime(timeStamp)
        # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        local_time = int(round(time.time() * 1000))
        diff_time = self.timeNum - local_time
        print(diff_time)
        print(datetime.now())
        return taobao_time

t = timeTaobao()
print(t.funcname())
