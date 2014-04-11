#coding=utf8

'''
	批量下载豆瓣图片
'''
import urllib
import urllib2
import re

for i in xrange(10):
	url = "http://www.douban.com/photos/album/121138964/?start=%d" % (i*18)
	
	res = urllib2.urlopen(url).read()

	img = re.compile(r'http:\/\/img\d\.douban\.com\/view\/photo\/thumb\/public\/p\d+\.jpg')
	for i in img.findall(res):
		name = "img/%s" % (i.split("/")[-1])
		urllib.urlretrieve(i, name)