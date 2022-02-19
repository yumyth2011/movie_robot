from abc import ABCMeta, abstractmethod

"""
消息通知发送的父类
"""


class Notify(metaclass=ABCMeta):
    @abstractmethod
    def send(self, message_template: str, context: dict):
        """
        发送通知
        :param message_template: 消息模版名称，notify_config中message_template配置项的定义，建议所有通知都可以用用户自由配置内容格式
        :param context: 消息模版使用的上下文变量
        :return:
        """
        pass
