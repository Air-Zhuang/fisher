import requests


class HTTP:
    '''通过requests库发送HTTP请求'''

    def get(self, url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:                            # 兼容200的格式
            return {} if return_json else ''
        return r.json() if return_json else r.text()        # 将结果转换成json格式
