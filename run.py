#!/usr/bin/env python2
# coding: utf-8

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import json
import commands

def stringToDatetime(data):
    # datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    # Aug 8, 2018 1:17:54 AM
    local_tz = pytz.timezone('Asia/Seoul')
    cur_time = datetime.strptime(data, "%b %d, %Y %I:%M:%S %p")
    local_dt = cur_time.replace(tzinfo=pytz.utc).astimezone(tz=local_tz)
    return str(local_tz.normalize(local_dt)).replace("+09:00", " (KST)")

def getContents(url):
    (exitstatus, result) = commands.getstatusoutput("curl \"%s\"" % (url))
    # print result
    return result

month = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}



url = 'https://iknowwhatyoudownload.com/en/peer/?ip=121.170.91.194'

r = requests.get(url)
# print(r.text)
soup = BeautifulSoup(getContents(url), 'lxml')

torrentFiles = soup.findAll('div', {'class': 'torrent_files'})
torrentSizes = soup.findAll('td', {'class': 'size-column'})
torrentTimes = soup.findAll('td', {'class': 'date-column'})

results = []

i = 0
for torrentFile in torrentFiles:

    try:
        tmpData = {
            'title': torrentFile.get_text().strip(),
            'size': torrentSizes[i].get_text().strip(),
            'firstTime': stringToDatetime(torrentTimes[i * 2].get_text().strip()),
            'lastTime': stringToDatetime(torrentTimes[i * 2 + 1].get_text().strip()),
        }
    except:
        pass

    results.append(tmpData)

    i += 1

print(json.dumps(results, sort_keys=True, indent=4))
