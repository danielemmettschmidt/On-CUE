import xml.etree.ElementTree as ET

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

class Stop_Index:
    def __init__(self):
        self.column_route_title = []
        self.column_route_id = []
        self.column_stop_title = []
        self.column_stop_title_split = []
        self.column_stop_tag = []
        self.column_stop_id = []

        self.route_filter_function_success = 0
        self.street_filter_function_success = 0
        self.cross_reference_function_success = 0

    def wipe(self):
        self.column_route_title = []
        self.column_route_id = []
        self.column_stop_title = []
        self.column_stop_title_split = []
        self.column_stop_tag = []
        self.column_stop_id = []

    def build(self, source):
        self.column_route_title = source.column_route_title.copy()
        self.column_route_id = source.column_route_id.copy()
        self.column_stop_title = source.column_stop_title.copy()
        self.column_stop_title_split = source.column_stop_title_split.copy()
        self.column_stop_tag = source.column_stop_tag.copy()
        self.column_stop_id = source.column_stop_id.copy()

    def append(self, source, iterator):
        self.column_route_title.append(source.column_route_title[iterator])
        self.column_route_id.append(source.column_route_id[iterator])
        self.column_stop_title.append(source.column_stop_title[iterator])
        self.column_stop_tag.append(source.column_stop_tag[iterator])
        self.column_stop_id.append(source.column_stop_id[iterator])

    def pull_stop_index(self):
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

        for route_id in route_list:

            stop_url = (stop_url_base + route_id)    

            tree = ET.ElementTree(file=urllib2.urlopen(stop_url))
            
            for elem in tree.iter(tag='stop'):
                stop_title = elem.get('title')
                if stop_title:
                    stop_id = (index_base[index_iter] + elem.get('stopId'))
                    stop_tag = elem.get('tag')
                    self.column_route_title.append(route_title_list[index_iter])
                    self.column_route_id.append(route_id)
                    self.column_stop_title.append(stop_title)
                    self.column_stop_tag.append(stop_tag)
                    self.column_stop_id.append(stop_id)

                    #print('Added: ' + route_title_list[index_iter] + ', ' + route_id + ', ' + stop_title + ', ' + stop_id)


            index_iter = index_iter + 1

    def split_title(self):
        split_iter = 0

        for each in self.column_stop_title:
            if 'at ' in self.column_stop_title[split_iter]:
                self.column_stop_title_split.append(self.column_stop_title[split_iter].split("at ",1)[1])
            elif 'and ' in self.column_stop_title[split_iter]:
                self.column_stop_title_split.append(self.column_stop_title[split_iter].split("and ",1)[1])
            else:
                self.column_stop_title_split.append(' ')
            
            split_iter = split_iter + 1

    def filter_index_route(self, user_input_route):

        reference_index = Stop_Index()
        reference_index.build(self)
        self.wipe()
       
        route_filter_iter = 0

        for each in reference_index.column_route_title:
            if reference_index.column_route_title[route_filter_iter].upper() == user_input_route:
                self.append(reference_index, route_filter_iter)
                self.route_filter_function_success = 1

            route_filter_iter = route_filter_iter + 1

    def filter_index_street(self, user_input_route, user_input_letter):
        self.filter_index_route(user_input_route)
        
        reference_index = Stop_Index()
        reference_index.build(self)
        
        self.wipe()

        street_filter_iter = 0

        for street in reference_index.column_stop_title:
            street = street.upper()
            letter = street[0]

            if letter == user_input_letter:
                self.append(reference_index,street_filter_iter)
                self.street_filter_function_success = 1
            
            street_filter_iter = street_filter_iter + 1

    def filter_cross_reference(self, user_input_route, user_input_letter):
        self.filter_index_route(user_input_route)

        reference_index = Stop_Index()
        reference_index.build(self)

        reference_index.split_title()

        self.wipe()

        cross_reference_iter = 0

        for cross_reference in reference_index.column_stop_title_split:
            street = cross_reference.upper()
            letter = street[0]
            
            if letter == user_input_letter:
                self.append(reference_index, cross_reference_iter)
                self.cross_reference_function_success = 1

            cross_reference_iter = cross_reference_iter + 1
                 
    def print_index(self):
        print_iter = 0

        if len(self.column_stop_title_split) == 0:
            self.column_stop_title_split = ['  '] * (len(self.column_stop_title))

        for header in self.column_route_title:
            print(header + ', ' + self.column_route_id[print_iter] + ', ' + self.column_stop_title[print_iter] + ', ' \
                + self.column_stop_tag[print_iter]  + ', ' + self.column_stop_id[print_iter] + ';')

            print_iter = print_iter + 1

def get_stop_url_inputs(user_input_code):

    stop_index = Stop_Index()
    stop_index.pull_stop_index()

    stop_url_iter = 0
    stop_url_route = ''
    stop_url_stop = ''
    url_function_success = 0

    for tag in stop_index.column_stop_tag:
        if stop_index.column_stop_id[stop_url_iter] == user_input_code:
            stop_url_route = stop_index.column_route_id[stop_url_iter]
            stop_url_stop = stop_index.column_stop_tag[stop_url_iter]
            url_function_success = 1

        stop_url_iter = stop_url_iter + 1
    
    return stop_url_route, stop_url_stop, url_function_success

def get_prediction(user_input_code):
    stop_url_route, stop_url_stop, url_function_success = get_stop_url_inputs(user_input_code)

    if url_function_success == 1:
        address = ('http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=fairfax&r=' + stop_url_route + '&s=' + stop_url_stop)

        tree = ET.ElementTree(file=urllib2.urlopen(address))

        for elem in tree.iter(tag='predictions'):
            message_route_title = elem.get('routeTitle')
            message_stop_title = elem.get('stopTitle')
            break

        for elem in tree.iter(tag='prediction'):
            minutes = elem.get('minutes')
            message = ('The next ' + message_route_title + ' bus will arrive at ' + message_stop_title + ' in ' + minutes + ' minutes.')
            break
    else:
            message = "Sorry, that code didn't work."
    
    return message

user_input_route = input('Route: ')
user_input_letter = input('Letter: ')

user_input_route = user_input_route.upper()
user_input_letter = user_input_letter.upper()

a_filter_index = Stop_Index()
a_filter_index.pull_stop_index()

a_filter_index.filter_index_street(user_input_route, user_input_letter)

print("-- Stops On Street --")
a_filter_index.print_index()

a_filter_index.wipe()
a_filter_index.pull_stop_index()
a_filter_index.filter_cross_reference(user_input_route, user_input_letter)

print("-- Stops On Cross-Streets --")
a_filter_index.print_index()

user_input_code = input('Code: ')
message = get_prediction(user_input_code)

print(message)