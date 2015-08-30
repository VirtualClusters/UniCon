import ConfigParser
import datetime
import time
import urllib2

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DISCOVERY_ETCD_NEW = "http://discovery.etcd.io/new"

# Thanks to
# http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
class FakeSecHead(object):
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[asection]\n'
    def readline(self):
   
        if self.sechead:
            try: 
                return self.sechead
            finally: 
                self.sechead = None
        else:
            return self.fp.readline()

def configparser_no_header(filepath):
    cp = ConfigParser.SafeConfigParser()
    cp.readfp(FakeSecHead(open(filepath)))
    return dict(cp.items('asection'))

def current_time():
    return str(datetime.datetime.now().strftime(TIME_FORMAT))

def str_to_time(string, tformat=None):
    if not tformat:
        tformat = TIME_FORMAT
    return time.strptime(string, tformat)

def discovery_etcd():
    response = urllib2.urlopen(DISCOVERY_ETCD_NEW)
    return response.read()

# ALIAS
load_cred = configparser_no_header
