import logging
import geoip2.database
import geoip2.errors


class GeoClassifier(object):
    def __init__(self, mmdb_reader):
        self.logger = logging.getLogger('console_log')
        self.mmdb_reader = mmdb_reader

    def lookup_ipaddr(self, ipaddr):
        try:
            self.place = self.mmdb_reader.city(ip_address=ipaddr)
        except geoip2.errors.AddressNotFoundError as ANFerr:
            self.logger.error('IP address db lookup error.')
            self.logger.error(ANFerr)

    def get_country(self):
        if self.place.country.name:
            return self.place.country.name, self.place.country.iso_code
        else:
            self.logger.debug('Place not found in MMdb')
            return 'Unknown', 'Unknown'

    def get_subdiv(self):
        if self.place.subdivisions:
            return self.place.subdivisions.most_specific.names['en']
        else:
            self.logger.debug('Subdivision not found in MMdb')
            return 'Unknown'