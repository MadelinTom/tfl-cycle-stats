import csv
from operator import itemgetter
from datetime import datetime
from symbol import comparison

DATE_FORMAT = '%d/%m/%Y %H:%M'
DATE_FORMAT_MILLIS = '%d/%m/%Y %H:%M:%S'
file_name = 'all_trips.csv'

# get statistics from the csv file
with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    longest_journey = 0
    shortest_journey = 100000 # arbitary value

    # individual bike stats
    bike_id = "1171"
    bike_id_trips = 0
    bike_id_trip_list = []
    individual_trips = []

    for row in csv_reader:
        # ignore column names 
        if (row[0] == "Rental Id"):
            print(f'line: {line_count} is a header')

        if (row[0] != "Rental Id"):
            line_count += 1

            # individual bike trip
            if(row[2] == bike_id):
                bike_id_trips += 1
                bike_id_trip_list += [row]

                if (row[6] != "0"):
                    individual_trips += [[row[6], row[8], ">", row[5]]]

            # longest and shortest journeys
            # if (int(row[1]) > longest_journey):
            #     longest_journey = int(row[1])

            # if(int(row[1]) < shortest_journey):
            #     shortest_journey = int(row[1])

    # trips for individual bike in chronological order
    # bike_id_trips_chronological = sorted(bike_id_trip_list, key=itemgetter(6))
    # for s in bike_id_trips_chronological:
    #     print(*s)
    
    # print("-----------------------------------")

    def comparison_with_or_without_milli_seconds(x):
        return_object = datetime.now()
        # print(x)

        if (x[0] != '0' and x[0] != ''): # need this due to faulty data in set
            try:
                return_object = datetime.strptime(x[0], DATE_FORMAT)
            except:
                print("EXCEPT-----", x[0])
                return_object = datetime.strptime(x[0], DATE_FORMAT_MILLIS)
        return return_object

    # start and end journeys in chronological order
    individual_trips_chronological = sorted(individual_trips, key=lambda x: comparison_with_or_without_milli_seconds(x))
    # key=itemgetter(0)
    # key=lambda x: datetime.strptime(x[1],'%d/%m/%Y')
    for i in individual_trips_chronological:
        print(*i)

    # open file
    f = open('./1171_trips.csv', 'w')
    # create the csv writer
    writer = csv.writer(f)
    for row in individual_trips_chronological:
        writer.writerow(row)
    # close the file
    f.close()
    

    print(f'Processed {line_count} trips.')
    print(f'Bike trips {bike_id_trips}.')
    # print(f'Bike trips list {bike_id_trip_list}.')
    # print(f'Longest journey: {longest_journey}.')
    # print(f'Shortest journey: {shortest_journey}.')
