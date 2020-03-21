from lxml import etree
import time
import requests

from queue import SimpleQueue


class NewPostSelector:
    def __init__(self, queue, session):
        self.q = queue
        self.s = session
        self.histo = set()
        self.loadHistoFromFile()

    def select(self):
        groupUrl = 'https://www.douban.com/group/groupID/'
        time.sleep(5)
        items = self.getItems(groupUrl)
        self.putItems(items)

        return self.q

    def getItems(self, url):
        xpExp = "//table[@class='olt']/tr"
        r = self.s.get(url)
        items = self.parseHtml(r, xpExp)
        return items

    def putItems(self, items):
        length = 0
        for tup in items:
            # tup = i.get('title'), i.get('href')
            title = tup[0]

            cnt = tup[2]
            try:
                href = tup[1].split('/')[5]
                if cnt > 20 or href in self.histo:
                    continue
                length += 1
                if length > 12:
                    return
                self.histo.add(href)
                # file.write(href+'\n')
                self.q.put((tup[0], tup[1], tup[3]))
                # print("Put in: ", tup[0])
            except AttributeError:
                print(tup)

    def loadHistoFromFile(self, fileName='resources/histo.txt'):
        with open(fileName, "r", encoding='utf-8') as file:
            lines = file.readlines()
            for l in lines:
                l = l.strip()
                if (len(l) == 0):
                    continue
                self.histo.add(l)

    def loadHistoFromWeb(self, url='https://www.douban.com/group/groupID/'):
        newSet = set()
        time.sleep(5)
        r = self.s.get(url)

        items = self.parseHtml(r)
        items = items[20:]
        for tup in items:
            href = tup[1].split('/')[5].strip()
            newSet.add(href)

        # self.persistHisto(newSet)
        self.histo.update(newSet)

    def persistHisto(self, setToWrite, fileName='resources/histo.txt'):
        with open(fileName, "a", encoding='utf-8') as file:
            for href in setToWrite:
                file.write(str(href) + '\n')

    def parseHtml(self, html, xpExp="defaultExp"):
        eles = etree.HTML(html.text).xpath(xpExp)
        eles = eles[len(eles) - 50:]
        items = []
        for ele in eles:
            li = ele.getchildren()
            cnt = li[2].text
            pair, cnt, userID = li[0].getchildren()[0].attrib, li[2].text, \
                               li[1].getchildren()[0].attrib['href'].split('/')[4]
            if cnt is None:
                cnt = 0
            else:
                cnt = int(cnt)
            tup = pair.get('title'), pair.get('href'), cnt, userID
            items.append(tup)

        return items


if __name__ == '__main__':
    q = SimpleQueue()
    s = requests.session()
    s.headers.update({
        'Host': 'www.douban.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    n = NewPostSelector(q, s)
    # n.loadHistoFromWeb()
    bigQ = n.select()
    while bigQ.qsize() > 0:
        print(bigQ.get(timeout=3))
