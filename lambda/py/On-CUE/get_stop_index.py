import xml.etree.ElementTree as ET

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def get_stop_index():
    route_url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=fairfax'

    tree = ET.ElementTree(file=urllib2.urlopen(route_url))

    route_list = []
    route_title_list = []

    for elem in tree.iter(tag='route'):
        grab = elem.get('tag')
        route_list.append(grab)
        grab = elem.get('title')
        route_title_list.append(grab)

    print(route_list)

    stop_url_base = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=fairfax&r='

    index_base = ['A','B','C','D']
    index_iter = 0

    column_route_title = []
    column_route_id = []
    column_stop_title = []
    column_stop_tag = []
    column_stop_id = []

    for route_id in route_list:

        stop_url = (stop_url_base + route_id)    

        tree = ET.ElementTree(file=urllib2.urlopen(stop_url))
        
        for elem in tree.iter(tag='stop'):
            stop_title = elem.get('title')
            if stop_title:
                stop_id = (index_base[index_iter] + elem.get('stopId'))
                stop_tag = elem.get('tag')
                column_route_title.append(route_title_list[index_iter])
                column_route_id.append(route_id)
                column_stop_title.append(stop_title)
                column_stop_tag.append(stop_tag)
                column_stop_id.append(stop_id)
                # print('Added: ' + route_title_list[index_iter] + ', ' + route_id + ', ' + stop_title + ', ' + stop_id)


        index_iter = index_iter + 1

    return column_route_title, column_route_id, column_stop_title, column_stop_tag, column_stop_id

col1, col2, col3, col4, col5 = get_stop_index()

print_iter = 0

for each in col1:
    print('Column: ' + col1[print_iter] + ', ' + col2[print_iter] + ', ' + col3[print_iter] + ', ' + col4[print_iter] + ', ' + col5[print_iter])
    print_iter = print_iter + 1

