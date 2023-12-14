#!/usr/bin/env python

import csv
from io import TextIOWrapper
from zipfile import ZipFile, ZIP_DEFLATED

ROUTE_SHORT_NAME = 2
TRIP_ROUTE_ID = 0
TRIP_SERVICE_ID = 1
STOP_TIMES_TRIP_ID = 0
STOP_TIMES_STOP_ID = 3
STOP_STOP_ID = 0

def filter_for(archive, file_name, field_no, values):
    """

    :param ZipFile archive:
    :param str file_name:
    :param int field_no: field number
    :param Set[str] values:
    :return:
    """
    count = 0
    output_file = open(file_name, 'w')
    with archive.open(file_name, 'r') as table:
        datareader = csv.reader(TextIOWrapper(table, 'utf-8'))
        for row in datareader:
            # print(row[field_no])
            if row[field_no] in values:
                output_file.write(','.join(row) + '\n')
                count += 1

    print('%d records for file %s' % (count, file_name))

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


def main():
    """
    routes: ['route_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type', 'route_url']
    trips: ['route_id', 'service_id', 'trip_id', 'trip_headsign', 'direction_id', 'shape_id', 'wheelchair_accessible', 'bikes_allowed', 'max_delay']
    stop_times: ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence', 'stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled', 'timepoint']
    stop: ['stop_id', 'stop_code', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon', 'zone_id', 'stop_url', 'location_type', 'parent_station', 'wheelchair_boarding', 'platform_code', 'vehicle_type']

    :return:
    """
    with ZipFile('hsl.zip') as zipped_gtfs:
        filter_for(zipped_gtfs,'routes.txt', ROUTE_SHORT_NAME, {'94', '95'})
        filter_for(zipped_gtfs, 'trips.txt', TRIP_ROUTE_ID, {'1094', '1095'})
        trip_ids = get_column('trips.txt', 2)
        service_ids = get_column('trips.txt', TRIP_SERVICE_ID)
        print('Service ID count: %d' % len(service_ids))
        # print('Service IDs: %r' % service_ids)
        filter_for(zipped_gtfs, 'stop_times.txt', STOP_TIMES_TRIP_ID, trip_ids)
        stop_ids = get_column('stop_times.txt', STOP_TIMES_STOP_ID)
        filter_for(zipped_gtfs, 'stops.txt', STOP_STOP_ID, stop_ids)
        # print('Stop ID count: %d' % len(stop_ids))

        all_files = ['routes.txt', 'trips.txt', 'stop_times.txt', 'stops.txt']
        with ZipFile('hsl_new.zip', 'w', compression=ZIP_DEFLATED) as output_zipped:
            for table in all_files:
                output_zipped.write(table, table)

        with zipped_gtfs.open('stops.txt', 'r') as routes:
              datareader = csv.reader(TextIOWrapper(routes, 'utf-8'))
              print('%s' % next(datareader))
              print('%s' % next(datareader))
        # with open('trips.txt', 'r') as routes:
        #       datareader = csv.reader(routes)
        #       print('%s' % next(datareader))
        #       print('%s' % next(datareader))
        # print(get_column('trips.txt', 2))


if __name__ == '__main__':
    main()
