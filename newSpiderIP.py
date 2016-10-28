import requests
import sys
import lxml
from lxml import etree

class Spider:

	def __init__(self, baseUrl):
		self.baseUrl = baseUrl

	def getHtml(self, pageNum):
		cookieFile = 'cookie.txt'
		cookie = requests.session().cookies
		url = self.baseUrl + str(pageNum)
		header = {
					'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
					'Cookie': cookie
				}
		result = requests.get(url, headers=header)
		if not cookie:
			cookie = str(result.cookies)
			requests.session().cookies = result.cookies
		with open(cookieFile, 'w') as cf:
			cf.write(cookie)
		html = result.content
		typ = sys.getfilesystemencoding()
		html = unicode(html, typ).encode('utf-8')
		return html

	def writeHtmlToFile(self, filename, html):
		with open(filename, 'w') as cf:
			cf.write(html)


class AnalyseHtml:

	def __init__(self, html):
		self.page = etree.HTML(html)

	def getPages(self):
		pages = self.page.xpath(u'//div[@class="pagination"]/a[last()-1]')
		return pages[0].text

	def getTitles(self):
		titleTags = self.page.xpath(u"//tr/th")
		titles = []
		for title in titleTags:
			titles.append(title.text)
		return titles


	def getContent(self):
		contents = {}
		titles = self.getTitles()
		ipTags = self.page.xpath(u"//tr/td[2]")
		portTags = self.page.xpath(u"//tr/td[3]")
		serverAddresseTags = self.page.xpath(u"//tr/td[4]/a[1]")
		isAnonymouTags = self.page.xpath(u"//tr/td[5]")
		typeTags = self.page.xpath(u"//tr/td[6]")
		speedTags = self.page.xpath(u"//tr/td[7]/div[1]")
		connectTimeTags = self.page.xpath(u"//tr/td[8]/div[1]")
		surviveTimeTags = self.page.xpath(u"//tr/td[9]")
		validateTimeTags = self.page.xpath(u"//tr/td[9]")
		ips, ports, serverAddresses, isAnonymous, types, speeds, connectTimes, surviveTimes, validateTimes = [], [], [], [], [], [], [], [], []

		for i in range(len(ipTags)):
			ips.append(ipTags[i].text.strip())
			ports.append(portTags[i].text.strip())
			serverAddresses.append(serverAddresseTags[i].text.strip())
			isAnonymous.append(isAnonymouTags[i].text.strip())
			types.append(typeTags[i].text.strip())
			speeds.append(speedTags[i].text.strip())
			connectTimes.append(connectTimeTags[i].text.strip())
			surviveTimes.append(surviveTimeTags[i].text.strip())
			validateTimes.append(validateTimeTags[i].text.strip())
		tables = [ips, ports, serverAddresses, isAnonymous, types, speeds, connectTimes, surviveTimes, validateTimes]

		for j in xrange(1, len(titles)):
			contents[titles[j]] = tables[j - 1]
		return contents

spider = Spider('http://www.xicidaili.com/nn/')
html = spider.getHtml(1)
spider.writeHtmlToFile('ip.html', html)
analyse = AnalyseHtml(html)
print analyse.getContent()
print analyse.getPages()
analyse.getTitles()