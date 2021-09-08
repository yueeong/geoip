import logging
import re


class FilterExtract(object):
    def __init__(self, regex_list, word_list):
        self.logger = logging.getLogger('console_log')

        self.regex_filter_list = regex_list
        self.string_filter_list = word_list

    def check_regex(self, string_to_test):
        for each in self.regex_filter_list:
            if re.search(each, string_to_test):
                self.logger.debug('regex match Found')
                return True

    def check_presence(self, string_to_test):
        if any(i in string_to_test for i in self.string_filter_list):
            self.logger.debug('Found')
            return True
        else:
            return False