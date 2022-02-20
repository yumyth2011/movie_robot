import logging
import urllib

from yee.core.httputils import RequestUtils
from yee.core.stringutils import StringUtils
from yee.notify.notify import Notify

"""
通知到Bark ios app
"""


class BarkNotify(Notify):
    req = RequestUtils(request_interval_mode=False)

    def __init__(self, **args):
        """
        args参数最终由notify_config.yml读取传递。具体可以参考这个配置文件，app配置项下的独立项obejct代表一种通知配置，其配置子项全部会传递到此args
        :param args:
        """
        self.push_url = args['push_url']
        self.message_template = args['message_template']
        self.args = args

    def send(self, message_template: str, context: dict):
        urls = self.push_url
        if urls is None or len(urls) == 0:
            return
        if message_template not in self.message_template:
            logging.error('找不到通知消息模版：%s' % (message_template))
            return
        mt = self.message_template[message_template]
        title = mt['title']
        message_pattern = mt['message']
        for url in urls:
            if url[-1] != '/':
                url = url + '/'
            url = f'{url}{urllib.parse.quote_plus(title)}/{urllib.parse.quote_plus(StringUtils.replace_var(message_pattern, context))}'
            params = ''
            if self.args is not None and len(self.args) > 0:
                for k in self.args['params'].keys():
                    params += f"{k}={self.args['params'][k]}&"
            if params:
                url = url + "?" + params.rstrip("&")
            res = self.req.get(url).json()
            if res["code"] != 200:
                logging.info('bark 推送失败 %s' % url)
