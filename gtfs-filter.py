#!/usr/bin/env python

import csv
from io import TextIOWrapper
from zipfile import ZipFile

ROUTE_SHORT_NAME = 2
TRIP_ROUTE_ID = 0

def filter_for(archive, file_name, field_no, values):
    """

    :param ZipFile archive:
    :param str file_name:
    :param int field_no: field number
    :param List[str] values:
    :return:
    """
    output_file = open(file_name, 'w')
    with archive.open(file_name, 'r') as table:
        datareader = csv.reader(TextIOWrapper(table, 'utf-8'))
        for row in datareader:
            # print(row[field_no])
            if row[field_no] in values:
                output_file.write(','.join(row) + '\n')



def main():
    with ZipFile('hsl.zip') as zipped_gtfs:
        filter_for(zipped_gtfs,'routes.txt', ROUTE_SHORT_NAME,['94', '95'])
        filter_for(zipped_gtfs, 'trips.txt', TRIP_ROUTE_ID, ['1094', '1095'])
        # with zipped_gtfs.open('trips.txt', 'r') as routes:
        #       datareader = csv.reader(TextIOWrapper(routes, 'utf-8'))
        #       print('%s' % next(datareader))
        #       print('%s' % next(datareader))


if __name__ == '__main__':
    main()
