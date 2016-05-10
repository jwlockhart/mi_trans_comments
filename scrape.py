# Script for scraping the comments data off of the public comment site
# v0.2

from bs4 import BeautifulSoup as bs
import urllib2
import time

#number of pages of comments
pages = 214

#the base url for all pages of comments
url = 'http://everyvoicecountsmi.org/136/public-comment-on-the-state-board-of-education-draft-statement-and-guidance-on-safe-and-supportive-learning-environments-for-lesbian-gay-bisexual-transgender-and-questioning-lgbtq-students/comment-page-'

#a list for holding pages of comments
data = []

print 'Downloading comment pages...'
for i in range(1, pages+1):
    #figure out the address to read next
    addr = url + str(i)
    
    #print progress report
    if i % 10 == 0:
        print 'Completed {:03.1f}%'.format((100.0 * i) / pages)
        
    #chill for a bit so as not to overwhelm server
    time.sleep(1)
    
    #download the page
    req = urllib2.Request(addr, headers={'User-Agent': 'Magic-Browser'})
    con = urllib2.urlopen(req)
    data.append(con.read())
    
print 'Completed 100%'

#merge all the webpages into one single giant string
together = '\n'.join(data)

print 'Saving the raw html...'
with open('raw.html', 'w') as fi:
    fi.write(together)
    
print 'Done saving!'

#TODO: parse the html