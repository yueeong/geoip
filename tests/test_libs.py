import unittest
import geoip2.database
from collections import Counter

from library.filterextract import FilterExtract
from library.geo_utils import GeoClassifier
from library.stats import StatsCollector

class TestFE(unittest.TestCase):
    def setUp(self):
        self.list_of_strings = ['static', 'images', '/images/', 'images/', '.txt', 'llll']
        self.list_of_neg_strings = ['hello', 'telecom', 'foo']
        self.list_regex_patterns = ['[a-f0-9]+\/+((css)|(js))',
                               '[a-f0-9]+\/images\/',
                               '.*\.rss',
                               '.*\.atom']
        self.list_string_to_check = ['/entry-images/',
                                '/images/',
                                '/user-images/',
                                '/static/',
                                '/robots.txt',
                                '/favicon.ico']
        self.fe = FilterExtract(self.list_regex_patterns, self.list_string_to_check)

    def test_regex_samples(self):
        pass

    def test_string_samples(self):
        # tests if any in list is present
        self.assertTrue(self.fe.check_presence(self.list_of_strings))

    def test_string_samples_neg(self):
        #checks that if all don't exists
        self.assertFalse(self.fe.check_presence(self.list_of_neg_strings))

    def test_string_sample_partials(self):

        # checks partials are not matched, only exact
        self.assertFalse(self.fe.check_presence(['.txt']))
        self.assertFalse(self.fe.check_presence(['robots.txt']))
        self.assertTrue(self.fe.check_presence(['/robots.txt']))


class TestGeo(unittest.TestCase):
    def setUp(self):
        mmdb_reader = geoip2.database.Reader('../data/GeoLite2-City.mmdb')
        self.known_ip = '8.8.8.8'
        self.geoc = GeoClassifier(mmdb_reader=mmdb_reader)

    def test_known_ip(self):
        self.geoc.lookup_ipaddr(self.known_ip)

        self.assertEqual(self.geoc.place.country.iso_code, 'US')

    def test_country(self):
        self.geoc.lookup_ipaddr(self.known_ip)
        self.assertEqual(self.geoc.get_country()[0], 'United States')

    def test_subdivision_of_country(self):
        self.geoc.lookup_ipaddr('208.67.220.220')
        self.assertEqual(self.geoc.get_subdiv(), 'California')

class TestStats(unittest.TestCase):
    def setUp(self):
        self.test_data_list = [['Canada', '/region/459'],
                               ['United States', '/entry/9680'],
                               ['Philippines', '/region/2'],
                               ['United States', '/entry/13395/reviews'],
                               ['United States', '/entry/2785'],
                               ['Netherlands', '/entry/near/19.2017%2C-155.523/filter'],
                               ['United States', '/region/2']]
        self.sc = StatsCollector(self.test_data_list, 'Country')

        # print(self.sc.df)

    def test_unique_loc(self):
        self.assertEqual(self.sc.get_unique_loc(), ['Canada', 'United States', 'Philippines', 'Netherlands'])

    def test_counting_urlpages(self):
        self.assertEqual(self.sc.get_counter_urlpages('United States'),
                         Counter({'/entry/9680': 1, '/entry/13395/reviews': 1, '/entry/2785': 1, '/region/2': 1}) )

    def test_counting_urlpages_neg(self):
        self.assertEqual(self.sc.get_counter_urlpages('Foo'), Counter())








if __name__ == '__main__':
    unittest.main()