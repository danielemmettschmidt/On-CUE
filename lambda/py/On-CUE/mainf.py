import xml.etree.ElementTree as ET

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

address = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=fairfax&r=green2&s=maifsw'

tree = ET.ElementTree(file=urllib2.urlopen(address))
body = tree.getroot()

for elem in tree.iter(tag='prediction'):
    minutes = elem.get('minutes')
    print(minutes)
    break
    