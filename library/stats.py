import logging
import re
from collections import Counter
import pandas as pd

class StatsCollector(object):
    def __init__(self, data_list, title):
        self.logger = logging.getLogger('console_log')
        self.title = title
        self.list_of_place_urlpath = data_list
        self.list_of_places = [each[0] for each in data_list]

        self.counter = Counter(self.list_of_places)

        self.df = pd.DataFrame().from_dict(self.counter, orient='index').reset_index()
        self.df = self.df.rename(columns={'index': str(title), 0: 'Visits'})
        self.df['Most Visited Page'] = ''


    def get_unique_loc(self):
        self.list_of_unique_loc = []

        for eachc in self.counter:
            self.list_of_unique_loc.append(eachc)
        return self.list_of_unique_loc

    def get_counter_urlpages(self, to_match):
        '''

        :param to_match:
        :return: collections.Counter object containing list of tuples(urlpages, num visits)
        '''
        urlpage_list = []
        for eachpath in self.list_of_place_urlpath:
            self.logger.debug(to_match)
            self.logger.debug(eachpath[0])
            self.logger.debug(eachpath[1])
            if to_match == eachpath[0]:
                urlpage_list.append(eachpath[1])
        self.logger.debug(to_match)
        self.logger.debug(Counter(urlpage_list))

        return Counter(urlpage_list)

    def set_most_visited_per_place(self, url_to_filter):
        for eachunique in self.list_of_unique_loc:
            top_two_urlpath = self.get_counter_urlpages(eachunique).most_common(2)
            if re.match(url_to_filter, top_two_urlpath[0][0]) and not len(top_two_urlpath ) ==1:
                del top_two_urlpath[0]
            self.df['Most Visited Page'][self.df[self.title] == eachunique] = top_two_urlpath[0][0]