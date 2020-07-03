import feedparser
import calendar
from datetime import datetime
import time
 
def parseRSS( rss_url ):
    return feedparser.parse( rss_url )
 
 
 
def getHeadlines(rss_url):
    headlines = []
 
    feed = parseRSS(rss_url)
    print('yay')
    for newsitem in feed['items']:
        #print(newsitem)
        headlines.append(newsitem['title'])
        #print(time.gmtime(time.mktime(datetime.today().timetuple())))
        #print(newsitem['published'])
        twodays = 86400/2

        current=time.strftime ("%s",time.localtime())
        t = time.strptime(newsitem['published'],"%a, %d %b %Y %H:%M:%S %Z")
        if int(current) - time.mktime(t) > twodays:
            print(newsitem['links'][0]['href'])

    return headlines
 
 
 
allheadlines = []
 
 
newsurls = {
 
    'googlenews': 'https://news.google.com/news/rss/?hl=en&amp;ned=us&amp;gl=US',
 
}
 
 
for key, url in newsurls.items():
    
    allheadlines.extend(getHeadlines(url))
 
 
for hl in allheadlines:
    #print(hl)
    break