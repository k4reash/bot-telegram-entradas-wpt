import urllib2, sys
from bs4 import BeautifulSoup

site= "https://www.worldpadeltour.com/entradas"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(site,headers=hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page, 'html.parser')
soup2 = soup.find("h3", class_="c-tournaments__title").text

print (soup2)

f=open("kk.txt","w")
f.write(soup2)
f.close()