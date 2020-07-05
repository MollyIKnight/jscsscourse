import urllib.request, urllib.parse, urllib.error
import re

#can only retrieve unlock toot.

inurl = 'https://pawoo.net/@witw/103468338496997606'
udf = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
url = urllib.request.Request(inurl, headers=udf)
urlrsp = urllib.request.urlopen(url)
charset=urlrsp.info().get_content_charset()
html = urlrsp.read().decode(charset)
print(html)
href=re.findall('(href=.*/[0-9]+)', html)
print(href)