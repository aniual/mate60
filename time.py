from datetime import datetime

import time

import requests


class timeTaobao(object):
    rush_buying_time = 1696653120000

    def taobao_time(self):
        r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                          headers={
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
        x = eval(r1.text)
        timeNum = int(x['data']['t'])
        return timeNum

    def funcname(self):
        initital_time = int(time.time() * 1000)
        # 结账方法。
        while True:
            diff_time = self.rush_buying_time - initital_time
            print(diff_time)
            if diff_time > 0 and diff_time < 10000:
                time.sleep(1)
                print(f'时间为: =========={datetime.fromtimestamp(self.taobao_time() / 1000)}')
            time.sleep(1)
            initital_time = int(time.time() * 1000)
            print(f'现在的时间为: =========={datetime.fromtimestamp(initital_time / 1000)}')


t = timeTaobao()
t.funcname()
