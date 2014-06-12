#coding=utf-8
import os
import logging
import traceback
import urllib
import urllib2
import json

logging.getLogger(__name__)

class Wxinterface(object):

    def __init__(self, config):
        self.api = "https://api.weixin.qq.com/cgi-bin"
        self.tokenFile = "access_token"
        self.config = config
        self.cacheToken()

    def json_read(self, string):
        return json.loads(string)

    def json_write(self, sjson):
        return json.dumps(sjson)

    def getToken(self):
        self.config.update({"grant_type":"client_credential"})
        data = urllib.urlencode(self.config)
        api = self.api + "/token?" + data 
        res = urllib2.urlopen(api).read()
        if res:
            f = open(self.tokenFile, "w")
            f.write(res)
            f.close()
            logging.info("WRITE:%s:%s" % (self.tokenFile, res))
        self.cacheToken(True)

    def cacheToken(self, again=False):
        if os.path.isfile(self.tokenFile):
            f = open(self.tokenFile, "r")
            res = f.read()
            if res:
                jarr = self.json_read(res)
                self.access_token = jarr.get("access_token", "")
        else:
            if again == False:
                self.getToken()

    def get(self, method, post={}, again=False):
        try:
            string = urllib.urlencode({"access_token":self.access_token})
            api = "https://api.weixin.qq.com/cgi-bin%s?%s" % (method, string)
            if post:
                data = urllib.urlencode(post)
                req = urllib2.Request(api, data)
            else:
                req = api
            res = urllib2.urlopen(req).read()
            jres = self.json_read(res)
            if jres.get("errcode"):
                logging.error(res)
                if int(jres["errcode"]) == 40001:
                    self.getToken()
                    if again == False:
                        return self.get(method, post, again=True)
                    else:
                        logging.error("can't get token")
            else:
                return jres
        except Exception,e:
            logging.error(traceback.format_exc())

    def getgroup(self):
        return self.get("/groups/get")

    def getuser(self):
        return self.get("/user/get")

    def sendgroup(self):
        post = {   
            "filter":{
                "group_id":"0"
            },
            "text":{
                "content":"hello, Shamcle"
            },
            "msgtype":"text"
        }
        return self.get("/message/mass/sendall", post)

    def uploadnews(self):
        post = {}
        post["articles"] = [
        {
            "thumb_media_id":"11",
            "author":"gh_1c70ae5adbee",
            "title":"Hello1",
            "content_source_url":"http://www.500.com",
            "content":"<h1>Hello, Shamcle1</h1>",
            "digest":"digest",
            "show_cover_pic":"1"
        },
        {
            "thumb_media_id":"22",
            "author":"gh_1c70ae5adbee",
            "title":"Hello2",
            "content_source_url":"http://www.500.com",
            "content":"<h1>Hello, Shamcle2</h1>",
            "digest":"digest",
            "show_cover_pic":"1"
        }]
        self.get("/media/uploadnews", post)

def WxClient(config):
    return Wxinterface(config)
