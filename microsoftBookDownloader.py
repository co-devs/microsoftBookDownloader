#!/usr/bin/env python
# Author: Michael Devens
#         Derek Ditch <github:@dcode>
# Github: https://github.com/co-devs
# Simple, poorly written script to download all of the files being shared
# by microsoft instead of downloading by hand. Downloads consecutively,
# will therefore take a while. Could be optimized, but meh.
# Also, download path is hardcoded. If you want to use it you will need
# to change the baseDir variable at a minimum


import os
import requests
import bs4
import urllib2


def downloadFile2(url):
    result = urllib2.urlopen(url)
    filename = os.path.basename(urllib2.urlparse.urlparse(result.url).path)
    # print filename
    # print result.geturl()
    return result.geturl()


def downloadFile(url, path):
    local_filename = os.path.join(path, url.split('/')[-1].title())
    # print url
    # print path
    # print local_filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

errors = []

res = requests.get('https://blogs.msdn.microsoft.com/mssmallbiz/2017/07/11/largest-free-microsoft-ebook-giveaway-im-giving-away-millions-of-free-microsoft-ebooks-again-including-windows-10-office-365-office-2016-power-bi-azure-windows-8-1-office-2013-sharepo/?ranMID=24542&ranEAID=lw9MynSeamY&ranSiteID=lw9MynSeamY-ljYIUif9JQSw6mGEPRE6hg&tduid=(35cd2ef014e03b4e91ddad36b13d5d02)(256380)(2459594)(lw9MynSeamY-ljYIUif9JQSw6mGEPRE6hg)(')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

# line = line.translate(None, '<>:\"/\|?*')
badChars = '<>:\"/\|?*'
baseDir = "./"

# file = open('file.html')
# soup = bs4.BeautifulSoup(file, "lxml")

elems = soup.select('tbody')
books = elems[0].select('tr')

booksLen = len(books)

for i in xrange(1, booksLen):
# for i in xrange(1, 5):
    bookData = books[i].select('td')
    category = bookData[0].getText().encode('ascii', 'ignore').translate(None, badChars)
    catDir = os.path.join(baseDir, category)
    # Check to see if the folder for the category exists
    # if not, then make it
    try:
        os.stat(catDir)
        # print catDir, ' Exists'
    except:
        # print 'Mkdir: ', catDir
        os.mkdir(catDir)
    # TODO: Debug print, remove or change to a progress meter
    # print 'Category: ', category
    title = bookData[1].getText().encode('ascii', 'ignore').translate(None, badChars)
    titleDir = os.path.join(catDir, title)
    try:
        os.stat(titleDir)
        # print titleDir, 'Exists'
    except:
        # print 'Mkdir: ', titleDir
        os.mkdir(titleDir)
    # TODO: Debug print, remove or change to a progress meter
    # print 'Title: ', title
    links = bookData[2].select('a')
    linkNum = 1
    for j in links:
        # TODO: Debug prints (x2), remove or change to a progress meter
        # print j['href']
        print 'Downloading book ' + str(i) + '/' + str(booksLen) + ', file ' + str(linkNum) + '/' + str(len(links)) + ' to', titleDir
        # TODO: Implement file download here. Download j['href']
        # Will first need to check if file is present or if we are being
        # redirected. We are likely being redirected and will need to download
        # from a different url
        link = j['href']
        try:
            downloadFile(downloadFile2(link), titleDir)
        except:
            print "ERROR"
            errors.append((category, title))
        linkNum += 1

print '\n\nERROR REPORT:'
for i in errors:
    print i
