#!/usr/bin/env python

#import stdlib
import os
import sys
import logging
import argparse

#import 3rd party lib
import apache_log_parser
from tabulate import tabulate
import geoip2.errors

#import custom libs
from utils import logcollector
from utils import file_utils
from library.filterextract import FilterExtract
from library.stats import StatsCollector
from library.geo_utils import GeoClassifier

if __name__ == "__main__":
    '''
    '''
    cli_argparser = argparse.ArgumentParser(description='Geo IP reporting tool.')
    cli_argparser.add_argument('-f', '--file', type=str, dest='log_file_path', required=True,
                               help='Enter path to apache log file to parse. Mandatory.')
    cli_argparser.add_argument('-db', '--dbfile', type=str, dest='mmdb_file_path', required=False,
                               default='./data/GeoLite2-City.mmdb',
                               help='Enter alternative path MaxMind db file. Default ./data/GeoLite2-City.mmdb')
    cli_argparser.add_argument('-r', '--report_style', type=str, dest='report_style', required=False,
                               default='psql',
                               help='Style of output report. Valid types : plain, psql, html, grid, rst')
    cli_argparser.add_argument('-v', '--quiet', dest='verboselog', action='store_true', required=False,
                               help='Bool. Set to quiet logs in terminal')

    options_given = cli_argparser.parse_args()

    # Set up logging
    CONSOLE_LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + '/logs/' + 'reporter.log'
    logcollector.setup_file_logger('console_log', CONSOLE_LOG_FILE, options_given.verboselog, level='INFO')
    logger = logging.getLogger('console_log')

    #Set up needed data
    try:
        mmdb_reader = geoip2.database.Reader(options_given.mmdb_file_path)
    except FileNotFoundError as fne:
        logger.error(fne)
        sys.exit(1)
    except Exception as ee:
        logger.error('Could not load MaxMind DB file')
        logger.error(ee)
        sys.exit(1)

    list_regex_patterns = ['[a-f0-9]+\/+((css)|(js))',
                            '[a-f0-9]+\/images\/',
                            '.*\.rss',
                            '.*\.atom']
    list_string_to_check = ['/entry-images/',
                            '/images/',
                            '/user-images/',
                            '/static/',
                            '/robots.txt',
                            '/favicon.ico']

    regex_most_visited_url_path_to_filter = '^\/$'

    # Init vars
    list_valid_ips = []
    list_valid_ips_country = []
    list_valid_ips_by_state = []

    list_of_countries = []
    list_of_us_states = []

    # Init objects
    geoclassifier = GeoClassifier(mmdb_reader=mmdb_reader)
    filterextractor = FilterExtract(list_regex_patterns, list_string_to_check)
    inlog_to_parse = file_utils.load_input_data(options_given.log_file_path)
    line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"")

    # Filter and Extract IPaddress and URL paths needed based on above filters
    # list_string_to_check and list_regex_patterns
    for line in inlog_to_parse:
        line_dict = line_parser(line)
        # filter
        url_path_to_test = line_dict['request_url_path']
        if not filterextractor.check_regex(url_path_to_test) and not filterextractor.check_presence(url_path_to_test):
            # pprint(line_dict['remote_host'])
            list_valid_ips.append({'ip': line_dict['remote_host'], 'path': url_path_to_test})

    logger.info('Number of valid IPs: ' + str(len(list_valid_ips)))

    # From list_valid_ips , lookup their Country and if US, lookup State.
    # Creates 2 lists : list_of_countries and list_of_us_states
    for each in list_valid_ips:
        geoclassifier.lookup_ipaddr(each['ip'])
        list_of_countries.append([geoclassifier.get_country()[0], each['path']])
        if geoclassifier.get_country()[1] == 'US':
            try:
                list_of_us_states.append([geoclassifier.get_subdiv(), each['path']])
            except KeyError as ke:
                logger.error(geoclassifier.place)
                logger.error(ke)

    logger.info('Number of countries: ' + str(len(list_of_countries)))
    logger.info('Number of US States: ' + str(len(list_of_us_states)))
    # Init objects that contain stats to be presented
    country_stats = StatsCollector(list_of_countries, 'Country')
    us_state_stats = StatsCollector(list_of_us_states, 'US State')

    # Determine most visited URL path for each Place (ie Country or US state in this case.
    logger.debug(country_stats.get_unique_loc())
    country_stats.set_most_visited_per_place(regex_most_visited_url_path_to_filter)
    logger.debug((us_state_stats.get_unique_loc()))
    us_state_stats.set_most_visited_per_place(regex_most_visited_url_path_to_filter)

    # Present report inline
    logger.info('.. Display Country Visitor Stats')
    print(tabulate(country_stats.df.nlargest(10, 'Visits'),
                   headers='keys',
                   showindex='never',
                   tablefmt=options_given.report_style))
    logger.info('.. Display US State Visitor Stats')
    print(tabulate(us_state_stats.df.nlargest(10, 'Visits'),
                   headers='keys',
                   showindex='never',
                   tablefmt=options_given.report_style))

    #TODO Any Cleanup
    #close out file
    inlog_to_parse.close()



