from datetime import datetime

import time

import requests


class timeTaobao(object):
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    timeNum = int(x['data']['t'])
    rush_buying_time = 1696649220000

    def funcname(self):
        # 初始时间
        initital_time = int(time.time() * 1000)
        while True:
            # 当前时间
            current_time = int(time.time() * 1000)
            diff_time = current_time - initital_time
            print(f'初始时间: ========={datetime.fromtimestamp(current_time / 1000)}')
            if diff_time >= 20000:
                taobao_time = self.timeNum
                print(f'淘宝时间: ========={datetime.fromtimestamp(taobao_time / 1000)}')
                local_time = int(time.time() * 1000)
                if local_time - taobao_time > 0:
                    current_time = local_time - (local_time - taobao_time)
                else:
                    current_time = local_time + (local_time - taobao_time)
                initital_time = int(time.time() * 1000)
            if current_time > self.rush_buying_time:
                print(f'已提交: ========={datetime.fromtimestamp(current_time / 1000)}')
                break


t = timeTaobao()
t.funcname()
