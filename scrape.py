# Script for scraping the comments data off of the public comment site
# v1.1

from bs4 import BeautifulSoup as bs
import urllib2
import time
import datetime
import pandas as pd

#number of pages of comments
pages = 221

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
raw = '\n'.join(data)

print 'Saving the raw html...'
with open('raw.html', 'w') as fi:
    fi.write(raw)
    
print 'Parsing the comments...'
soup = bs(raw, 'html.parser')

#select the comments out of the html
comments = soup.findAll("li", { "class" : "comment" })

#dictionary for our parsed data
parsed = {}

for c in comments:
    tmp = {}
    #select the comment ID
    cid = c.find('article').get('id')
    
    #try to get the author name. Use empty string if they have no name.
    try:
        tmp['author'] = c.find('p', {'class': 'comment-author-name'}).string
    except(AttributeError):
        tmp['author'] = ''
        
    #try to get their occupation. Use empty string if it's missing.
    try:
        tmp['occupation'] = c.find('strong').string
    except(AttributeError):
        tmp['occupation'] = ''
    
    #grab the timestamp on the comment
    time = c.find('time').get('datetime')
    #convert the timestamp to an actual python datetime object
    tmp['time'] = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+00:00')
    
    #grab the body text of the comment
    tmp['text'] = c.find('section', {'itemprop': 'commentText'}).get_text()
    
    #add this user's comment information to our dictionary of all comments
    parsed[cid] = tmp
    
#convert the parsed dictionary into a clean dataframe :)
df = pd.DataFrame.from_dict(parsed, orient='index')
#reorder the columns
df = df[['time', 'author', 'occupation', 'text']]
#sort comments by the date, starting with the first comments
df = df.sort_values(by='time')

print 'Cleaning up text...'
def strip_occ(row):
    '''Remove the occupation from the text of the comment. Also remove newlines.'''
    occ = unicode(row['occupation'])
    txt = row['text'].replace('\n', ' ').replace(occ+'. ', '', 1)
    return txt

def clean(s):
    '''Clean up text for ease of processing'''
    return unicode(s).lower().strip().replace('\n', ' ')

df['text'] = df.apply(strip_occ, axis=1)
df['author'] = df['author'].apply(clean)
df['occupation'] = df['occupation'].apply(clean)

print 'Saving parsed comment data...'
df.to_csv('parsed.tsv', sep='\t', encoding='utf-8')

print 'Done!'