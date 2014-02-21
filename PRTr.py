#!/usr/bin/env python
# coding=utf-8


import urllib2,subprocess,sys

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def handle_entityref(self, name):
        self.fed.append('&%s;' % name)
    def get_data(self):
        return ''.join(self.fed)

def html_to_text(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


html=urllib2.urlopen('http://www.e-classical.com.tw/prtasp/prtcalander/ProgSongList2.asp').read().decode('big5').encode('utf-8')

programme = html.split('本時段節目:')[1].split('<')[0].strip()

programme = programme[:programme.rfind(' ')] #truncate off the substring like'3-1' 

intro = html_to_text( html.split('本時段節目:')[1].split('以下是本時段節目曲單')[0].strip() ).replace(' ','') 

copyright = intro[intro.find('-')+2:]



cmd='ffmpeg -i mmsh://bcr.media.hinet.net/RA000018  -acodec copy -metadata title="PRT rec:`date +"%F %R %a"`" ' +'  -metadata album="%s" -metadata comment="%s"  -metadata copyright="%s" '%(programme,intro, copyright) +'  -metadata author="台北爱乐电台"  -metadata genre="Classical" ' +  '`date +"%y%m%d_%H%M"`'+programme.replace(' ','')+'.wma'

print cmd

p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()






