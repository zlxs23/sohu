# _*_coding:utf-8_*_
import urllib
import urllib2
import cookielib

# 2016年8月7日19:15:19 -- The afternoon my work let me del CAO
# http://cuiqingcai.com/947.html
# 1. GET the website's HTML Content
url = 'http://m.sohu.com'
response = urllib2.urlopen(url)
# print response.read() # --> m.sohu.com.html
# urlopen's use urlopen(url, data, timeout)
# 2. Build Request
request = urllib2.Request(url)
response = urllib2.urlopen(request)
# 3. HTTP GET, POST Method
# POST:
values = {'username': '111@qq.com', 'password': '111'}
'''
values = {}
values['username'] = '111@qq.com'
values['password'] = '111'
'''
data = urllib.urlencode(values)
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
# GET:
geturl = url + '?' + data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
# http://cuiqingcai.com/954.html
# 1. Set Headers
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = {'User-Agent':user_agent}
request = urllib2.Request(url, data, headers)
response = urllib2.urlopen(request)
# 反盗链
headers = {'User-Agent':user_agent, 'Referer':'http://m.sohu.com'}
'''
User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
application/json ： 在 JSON RPC 调用时使用
application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务
'''
# 2. Set Proxy
enable_proxy = True
proxy_handler = urllib2.ProxyHandler({'http': 'http://m.sohu.com:8080'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
	opener = urllib2.build_opener(proxy_handler)
else:
	opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)
# 3. Timeout Set
response = urllib2.urlopen(url, data=data, timeout=1000)
# 4. HTTP's PUT and DELETE method
'''
PUT：这个方法比较少见 HTML表单也不支持这个
本质上来讲 PUT和POST极为相似 都是向服务器发送数据 但它们之间有一个重要区别
PUT通常指定了资源的存放位置 而POST则没有 POST的数据存放位置由服务器自己决定。
DELETE：删除某一个资源 基本上这个也很少见
不过还是有一些地方比如amazon的S3云服务里面就用的这个方法来删除资源
'''
request = urllib2.Request(url)
request.get_method = lambda: 'PUT' # or 'POST'
response = urllib2.urlopen(request)
# 5. Use Debug Log
# 可使用 下面方法 open Debug Log, 这样收发 包 的内容 即可显示在屏幕上 方便调试
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
response = urllib2.urlopen(url)
# http://cuiqingcai.com/961.html
# 1. URLError
'''
URLError 产生 Reason:
    网络无连接，即本机无法上网
    连接不到特定的服务器
    服务器不存在
'''
# 在 Code 中 try-except 捕获错误 异常
url = 'http://hh.com' # this url isn't exist
request = urllib2.Request(url)
try:
	urllib2.urlopen(request)
except urllib2.URLError, e:
	print e.reason
# print: [Errno 11004] getaddrinfo failed
# 2. HTTPError
# HTTPError is URLError's subclass
'''
When use urlopen method to send a request and Server will give a response
其中它包含一个数字”状态码”
举个例子，假如response是一个”重定向”，需定位到别的地址获取文档，urllib2将对此进行处理
其他不能处理的, urlopen会产生一个HTTPError, 对应相应的状态码
HTTP状态码表示HTTP协议所返回的响应的状态。下面将状态码归结如下：
    100：继续  客户端应当继续发送请求。客户端应当继续发送请求的剩余部分，或者如果请求已经完成，忽略这个响应。
    101： 转换协议  在发送完这个响应最后的空行后，服务器将会切换到在Upgrade 消息头中定义的那些协议。只有在切换新的协议更有好处的时候才应该采取类似措施。
    102：继续处理   由WebDAV（RFC 2518）扩展的状态码，代表处理将被继续执行。
    200：请求成功      处理方式：获得响应的内容，进行处理
    201：请求完成，结果是创建了新资源。新创建资源的URI可在响应的实体中得到    处理方式：爬虫中不会遇到
    202：请求被接受，但处理尚未完成    处理方式：阻塞等待
    204：服务器端已经实现了请求，但是没有返回新的信 息。如果客户是用户代理，则无须为此更新自身的文档视图。    处理方式：丢弃
    300：该状态码不被HTTP/1.0的应用程序直接使用， 只是作为3XX类型回应的默认解释。存在多个可用的被请求资源。    处理方式：若程序中能够处理，则进行进一步处理，如果程序中不能处理，则丢弃
    301：请求到的资源都会分配一个永久的URL，这样就可以在将来通过该URL来访问此资源    处理方式：重定向到分配的URL
    302：请求到的资源在一个不同的URL处临时保存     处理方式：重定向到临时的URL
    304：请求的资源未更新     处理方式：丢弃
    400：非法请求     处理方式：丢弃
    401：未授权     处理方式：丢弃
    403：禁止     处理方式：丢弃
    404：没有找到     处理方式：丢弃
    500：服务器内部错误  服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。一般来说，这个问题都会在服务器端的源代码出现错误时出现。
    501：服务器无法识别  服务器不支持当前请求所需要的某个功能。当服务器无法识别请求的方法，并且无法支持其对任何资源的请求。
    502：错误网关  作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。
    503：服务出错   由于临时的服务器维护或者过载，服务器当前无法处理请求。这个状况是临时的，并且将在一段时间以后恢复。
'''
# HTTPError instance has a code attr, is Server 返回的 相关 错误号
# 捕获 の 异常 IS a HTTPError's code attr is a error number
url = 'http://blog.csdn.net/cqcre'
request = urllib2.Request(url)
try:
	urllib2.urlopen(request)
except urllib2.HTTPError, e:
	print e.code
	print e.reason
# print: HTTP Error 403: Forbidden Forbidden
'''
URLError is HTTPError's parent_class
parent_class's Error should set after subclass
IF can't catch subclass's Error, can catch parent_class's Error Errno
'''
url = 'http://blog.csdn.net/cqcre'
request = urllib2.Request(url)
try:
	urllib2.urlopen(request)
except urllib2.HTTPError, e:
	print 'HTTPError: ', e.code, e.reason
except urllib2.URLError, e:
	print 'URLError: ',e.code, e.reason
else:
	print 'OK'
# 可加入 hasattr Func to judge this object has? this attr
# 首先对异常的属性进行判断，以免出现属性输出报错的现象
url = 'http://blog.csdn.net/cqcre'
request = urllib2.Request(url)
try:
	urllib2.urlopen(request)
except urllib2.HTTPError, e:
	if hasattr(e, 'code'):
		print 'HTTPError\'s number: ', e.code
except urllib2.URLError, e:
	if hasattr(e, 'reason'):
		print 'URLError\'s reason: ', e.reason
else:
	print 'OK'
# http://cuiqingcai.com/968.html
# 1. opener
'''
When get a url by use a opener(a urllib2.OpenerDirector's instance)
在前面，我们都是使用的默认的opener 即 urlopen
它是一个特殊的opener，可以理解成opener的一个特殊实例，传入的参数仅仅是url，data，timeout
'''
# 2. Cookielib
'''
cookielib模块的主要作用是提供可存储cookie的对象 以便于与urllib2模块配合使用来访问Internet资源
Cookielib模块非常强大
我们可以利用本模块的CookieJar类的对象来捕获cookie并在后续连接请求时重新发送
比如可以实现模拟登录功能
该模块主要的对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar
其关系: CookieJar--派生-->FileCookieJar--派生-->MozillaCookieJar、LWPCookieJar
'''
	# 2.1 collect cookie AND save to variabl
# declare a CookieJar object to save cookie
cookie = cookielib.CookieJar()
# use urllib2's HTTPCookieProcessor object to create cookie processor
handler = urllib2.HTTPCookieProcessor(cookie)
# by handler to build opener
opener = urllib2.build_opener(handler)
# there is open method like as urlopen method also get a request
url = 'http://www.baidu.com'
response = opener.open(url)
for item in cookie:
	print 'Name: ' + item.name
	print 'Value: ' + item.value
	# 2.2 collect cookie AND save to file
# set a saved cookie file
filename = 'baidu_cookie.txt'
# declare a MozillaCookieJar object instance to save cookie then write to file
cookie = cookielib.MozillaCookieJar(filename)
# use urllib2's HTTPCookieProcessor object to create cookie processor
handler = urllib2.HTTPCookieProcessor(cookie)
# by handler to build opener
opener = urllib2.build_opener(handler)
# create a request like as urlopen
url = 'http://www.baidu.com'
response = opener.open(url)
# save cookie to file
cookie.save(ignore_discard=True, ignore_expires=True) # 忽略 被丢弃的 忽略 过期的
'''
ignore_discard的意思是即使cookies将被丢弃也将它保存下来
ignore_expires的意思是如果在该文件中cookies已经存在则覆盖原文件写入
在这里我们将这两个全部设置为True
'''
	# 3. From file to collect cookie AND visit this website
# create MozillaCookieJar instance object
cookie = cookielib.MozillaCookieJar()
cookie.load('baidu_cookie.txt', ignore_discard=True, ignore_expires=True)
# create a request like as urlopen
url = 'http://www.baidu.com'
response = urllib2.Request(url)
# use urllib2.HTTPCookieProcessor object to create cookie processor
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
response = opener.open(request)
print response.read()
# HTTPError: HTTP Error 403: Forbidden
# No username, password
# Try to 爬虫 教务处