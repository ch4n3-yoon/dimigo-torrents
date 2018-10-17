#!/usr/bin/env python3
# coding: utf-8

# import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import json
import subprocess
from operator import itemgetter

def stringToDatetime(data):
    # datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    # Aug 8, 2018 1:17:54 AM
    local_tz = pytz.timezone('Asia/Seoul')
    cur_time = datetime.strptime(data, "%b %d, %Y %I:%M:%S %p")
    local_dt = cur_time.replace(tzinfo=pytz.utc).astimezone(tz=local_tz)
    return str(local_tz.normalize(local_dt)).replace("+09:00", " (KST)")

def getContents(url):
    # 한글 깨짐 현상 때문에 curl 라이브러리 이용
    response = subprocess.getoutput("curl \"%s\"" % (url))
    return response

def getTorrents(ip):
    url = 'https://iknowwhatyoudownload.com/en/peer/?ip=%s' % (ip)
    soup = BeautifulSoup(getContents(url), 'lxml')

    torrentFiles = soup.findAll('div', {'class': 'torrent_files'})
    torrentSizes = soup.findAll('td', {'class': 'size-column'})
    torrentTimes = soup.findAll('td', {'class': 'date-column'})

    results = []

    i = 0
    for torrentFile in torrentFiles:
        try:
            tmp_data = {
                'title': torrentFile.get_text().strip(),
                'size': torrentSizes[i].get_text().strip(),
                'firstTime': stringToDatetime(torrentTimes[i * 2].get_text().strip()),
                'lastTime': stringToDatetime(torrentTimes[i * 2 + 1].get_text().strip()),
            }
        except:
            pass

        results.append(tmp_data)
        i += 1

    return results

def jsonize(data):
    return json.dumps(data, sort_keys=True, indent=4)

def main():
    dimigo_ips = ['121.170.91.194', '121.170.91.130', '207.189.31.198']
    torrents = []
    for ip in dimigo_ips:
        tmp = getTorrents(ip)
        for t in tmp:
            torrents.append(t)

    torrents = sorted(torrents, key=itemgetter('firstTime'), reverse=True)
    print(jsonize(torrents))

if __name__ == '__main__':
    main()
