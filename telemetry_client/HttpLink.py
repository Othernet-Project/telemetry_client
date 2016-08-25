import urllib
import urllib2
import ssl
from netifaces import interfaces, AF_LINK, AF_INET, ifaddresses

class HttpLink:

    def __init__(self, conf):
	self.conf = conf
        self.iface = conf["interface"]
	self.endpoint = conf["endpoint"]
	self.headers = {"User-Agent": conf["useragent"]}
	if conf["sslnoverify"] == "True":
		self.ssl_context = ssl._create_unverified_context()
	else:
		self.ssl_context = ssl.create_default_context()
        self.macid = None
        self.ip = None

    def refresh_iface_status(self):
        self.macid = None
        self.ip = None
        if self.iface in interfaces():
            addresses = ifaddresses(self.iface)
            if addresses.has_key(AF_LINK):
                self.macid = addresses[AF_LINK][0]['addr']
	        if addresses.has_key(AF_INET):
		        self.ip = addresses[AF_INET][0]['addr']

    def submit(self,values):
        self.refresh_iface_status()
        if self.ip:
            ids = { "macid": self.macid, "lanip" : self.ip}
            values.update(ids)
            urldata = urllib.urlencode(values)
            full_url = self.endpoint + "?" + urldata
            print full_url
            try:
                req = urllib2.Request(full_url,headers=self.headers)
                urllib2.urlopen(req, context=self.ssl_context)
            except urllib2.URLError as e:
	            print e

