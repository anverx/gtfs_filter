#!/usr/bin/env python

import os
import csv
from io import TextIOWrapper
from zipfile import ZipFile, ZIP_DEFLATED
from typing import Set

class GTFS_Filter:
    """
    routes: ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type', 'route_url']
    trips: ['route_id', 'service_id', 'trip_id', 'trip_headsign', 'direction_id', 'shape_id', 'wheelchair_accessible', 'bikes_allowed', 'max_delay']
    stop_times: ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence', 'stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled', 'timepoint']
    stop: ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station', 'wheelchair_boarding', 'platform_code', 'vehicle_type']
    """
    ROUTE_ROUTE_ID = 0
    ROUTE_SHORT_NAME = 2

    TRIP_ROUTE_ID = 0
    TRIP_SERVICE_ID = 1
    TRIP_TRIP_ID = 2

    STOP_TIMES_TRIP_ID = 0
    STOP_TIMES_STOP_ID = 3
    STOP_STOP_ID = 0

    CALENDAR_SERVICE_ID = 0

    ALL_FILES = ['routes.txt', 'trips.txt', 'stop_times.txt', 'stops.txt', 'calendar.txt']

    def __init__(self, filename):
        """
        :param str filename:
        """
        self.filename = filename
        if not os.path.exists(self.filename):
            print('Archive not found!')

    def filter_for(self, file_name, field_no, values):
        """

        :param str file_name:
        :param int field_no: field number
        :param Set[str] values: Empty set is a special value that means everything
        :return:
        """
        count = 0
        output_file = open(file_name, 'w')
        # print(f'Filtering for: archive: {self.filename}, file: {file_name}, field no: {field_no}')
        with ZipFile(self.filename) as archive:
            with archive.open(file_name, 'r') as table:
                try:
                    datareader = csv.reader(TextIOWrapper(table, 'utf-8'))
                    for row in datareader:
                        # print(row[field_no])
                        try:
                            if not values or row[field_no] in values:
                                output_file.write(','.join(row) + '\n')
                                count += 1
                        except Exception as exc:
                            print('Error in parsing/storing row: %s' % exc)
                except Exception as exc:
                    print('Error in parsing row: %s' %  exc)

        print('%d records for file %s' % (count, file_name))

    @staticmethod
    def get_column(file_name, field_no):
        """
        :param str file_name:
        :param int field_no:
        :rtype: Set[str]
        """
        result = set()
        with open(file_name, 'r') as table:
            datareader = csv.reader(table)
            for row in datareader:
                result.add(row[field_no])
        return result

    @staticmethod
    def create_zip(filename):
        """
        :param str filename:
        """
        with ZipFile(filename.removesuffix('.zip') + '_filtered.zip', 'w', compression=ZIP_DEFLATED) as output_zipped:
            for table in GTFS_Filter.ALL_FILES:
                output_zipped.write(table, table)

    def filter(self, routes):
        """
        :param Set(str) routes:
        """

        self.filter_for('routes.txt', self.ROUTE_SHORT_NAME, routes)
        # self.print_head('routes.txt')

        route_ids = self.get_column('routes.txt', self.ROUTE_ROUTE_ID)

        self.filter_for('trips.txt', self.TRIP_ROUTE_ID, route_ids)
        trip_ids = self.get_column('trips.txt', self.TRIP_TRIP_ID)

        service_ids = self.get_column('trips.txt', self.TRIP_SERVICE_ID)
        self.filter_for('calendar.txt', self.CALENDAR_SERVICE_ID, service_ids)
        print('Service ID count: %d' % len(service_ids))
        # print('Service IDs: %r' % service_ids)

        self.filter_for('stop_times.txt', self.STOP_TIMES_TRIP_ID, trip_ids)
        stop_ids = self.get_column('stop_times.txt', self.STOP_TIMES_STOP_ID)
        self.filter_for('stops.txt', self.STOP_STOP_ID, stop_ids)
        # print('Stop ID count: %d' % len(stop_ids))

        self.create_zip(self.filename)

    def print_head(self, file_name):
        with ZipFile(self.filename) as archive:
            with archive.open(file_name, 'r') as routes:
                datareader = csv.reader(TextIOWrapper(routes, 'utf-8'))
                print('%s' % next(datareader))
                print('%s' % next(datareader))

    def get_all_route_names(self):
        """

        :rtype: Set[str]
        """
        self.filter_for('routes.txt',0, set())
        return self.get_column('routes.txt', self.ROUTE_SHORT_NAME)


def main():
    """

    :return:
    """
    f = GTFS_Filter('hsl.zip')
    print('All route names: %r' % f.get_all_route_names())
    f.filter({'94', '95', '75', '92'})


if __name__ == '__main__':
    main()
