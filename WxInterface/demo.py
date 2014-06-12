#coding=utf-8
from WxInterface import WxClient

config = {"appid":"wx0cb6649ff52bba7d", "secret":"21018fb1693aeda3fe5d62bcaabb8426"}

client = WxClient(config)
print client.getgroup()
