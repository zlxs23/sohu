# _*_coding:utf-8_*_
import urllib
import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://m.sohu.com'
request = urllib2.Request(url)
try:
	response = urllib2.urlopen(request)
except urllib2.HTTPError, e:
	if hasattr(e, 'code'):
		print 'HTTPError\'s number: ', e.code
except urllib2.URLError, e:
	if hasattr(e, 'reason'):
		print 'URLError\'s reason: ', e.reason
content = response.read().decode('utf-8')
pattern = re.compile(r'<a href=(.*?)>', re.S)
href = re.findall(pattern, content)
for h in href:
	if 'class' in h:
		h = h[:h.find('class')]
	print h.rstrip()
print len(href)
# Success to GET a website's ALL link
# 2016年8月8日00:12:20