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


        index_iter = index_iter + 1

    return column_route_title, column_route_id, column_stop_title, column_stop_tag, column_stop_id


#### delete up from here

def get_stop_url_inputs(user_input):
    column_route_title, column_route_id, column_stop_title, column_stop_tag, column_stop_id = get_stop_index()

    stop_url_iter = 0
    stop_url_route = ''
    stop_url_stop = ''
    function_success = 0

    for tag in column_stop_tag:
        if column_stop_id[stop_url_iter] == user_input:
            stop_url_route = column_route_id[stop_url_iter]
            stop_url_stop = column_stop_tag[stop_url_iter]
            function_success = 1

        stop_url_iter = stop_url_iter + 1
    
    return stop_url_route, stop_url_stop, function_success

stop_url_route, stop_url_stop, function_success = get_stop_url_inputs(input('Code: '))

address = ('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=fairfax&r=' + stop_url_route + '&s=' + stop_url_stop + ' - ', function_success)

print(address)