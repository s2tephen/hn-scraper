import os, csv, urllib2
from BeautifulSoup import BeautifulSoup

# initialize variables
link_list = []
ids = []
FILE_NAME = 'hacker_news.csv'

# get current keys
if os.path.isfile(FILE_NAME):
  input_file = csv.DictReader(open(FILE_NAME))
  for r in input_file:
    ids.append(r['id'])
    link_list.append(r)

# set basic parameters
target_url = 'http://news.ycombinator.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US))'}

# send request and soupify
request = urllib2.Request(target_url, None, headers)
response = urllib2.urlopen(request)
soup = BeautifulSoup(response)

# structure dat data
print 'scraping...'
links = soup.findAll('td', 'title')[1::2]
for l in links:
  id_ = l.parent.nextSibling.findAll('a')[1].get('href').split('=')[1]
  if id_ not in ids:
    data = {}
    data['id'] = l.parent.nextSibling.findAll('a')[1].get('href').split('=')[1]
    data['url'] = l.a.get('href')
    data['title'] = l.a.text
    data['user'] = l.parent.nextSibling.findAll('a')[0].text
    data['comments'] = l.parent.nextSibling.findAll('a')[1].text.split(' ')[0]
    link_list.append(data)
  else: # only update comment count if already in db
    data = link_list[ids.index(id_)]
    data['id'] = data['id'].decode('utf8')
    data['url'] = data['url'].decode('utf8')
    data['title'] = data['title'].decode('utf8')
    data['user'] = data['user'].decode('utf8')
    data['comments'] = l.parent.nextSibling.findAll('a')[1].text.split(' ')[0]
  print '  ' + l.a.get('href')
print '...done!'

# output to csv
field_names = link_list[0].keys()
writer = csv.DictWriter(open('hacker_news.csv', 'wb'), fieldnames=field_names)
headers = dict((n, n) for n in field_names)
writer.writerow(headers)
for data in link_list:
  writer.writerow(dict((k, v.encode('utf8')) for k, v in data.iteritems()))