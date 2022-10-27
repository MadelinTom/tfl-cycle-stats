import requests
import json
import csv
from datetime import datetime

urls = []
DATE_FORMAT = '%d/%m/%Y %H:%M'
DATE_FORMAT_MILLIS = '%d/%m/%Y %H:%M:%S'

#  get all urls
with open('journey_links.json') as json_file:
    json_object = json.load(json_file)

    for object in json_object["entries"]:
        urls += [object["url"]]

# print urls
for url in urls:
    print(url)

# open file
f = open('./cleaned_data.csv', 'w')
# create the csv writer
writer = csv.writer(f)

# download csv data from urls and write to master csv file
first_row_count = 0
for url in urls:
    individual_row_count = 0
    with requests.Session() as s:
        print(f'Downloading: {url}')
        download = s.get(url)

        print("Downloaded!")
        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Writing to file")
        for row in my_list:
            # leave in one header row
            if first_row_count == 0:
                writer.writerow(row)

            # ignore all other header rows
            if individual_row_count != 0:

                # ignore any rows with missing data
                if (row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '' or row[6] == '' or row[7] == '' or row[8] == ''):
                    print(f"Empty field! \n {row}")
                    continue

                # if datetime is wrong format force correct format
                # row[3] & row[6]
                end_date = row[3]
                start_date = row[6]

                # HACK: due to the way datetime.strptime works it cannot be used as boolean, we have to catch the exception raised and try to convert
                if not (row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '' or row[6] == '' or row[7] == '' or row[8] == ''):
                    # HACK: see below conidional regarding row[6]
                    if (len(row) == 10):
                        start_date = row[7]
                    try:
                        date = datetime.strptime(end_date, DATE_FORMAT)
                    except ValueError as err:
                        print(err)
                        try:
                            temp = datetime.strptime(end_date, DATE_FORMAT_MILLIS)
                            row[3] = temp.strftime(DATE_FORMAT)
                        except ValueError as err:
                            continue

                    try:
                        date = datetime.strptime(start_date, DATE_FORMAT)
                    except ValueError as err:
                        print(err)
                        try:
                            temp = datetime.strptime(start_date, DATE_FORMAT_MILLIS)
                            # HACK: see below conditional regarding row[6]
                            if (len(row) == 10):
                                row[7] = temp.strftime(DATE_FORMAT)
                            else:
                                row[6] = temp.strftime(DATE_FORMAT)
                        except ValueError as err:
                            continue
                            

                # TODO: ignore rows that have the wrong data type in the corresponding column
                # check for start date being '0' or '1' here (row[6])
                # HACK: The only rows with startdate being '0' or '1' have a length of 10
                if (len(row) == 10):
                    print("Length of row = 10, ignoring row[6]")
                    writer.writerow(
                        [row[0], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[9]])

                # write only the rows that correspond to the header rows (ignore index's above 9)
                # HACK: some rows have random empty fields at the end, but the rest of the data is fine... so we only write the useful data
                elif len(row) > 9:
                    print("Row contains trailing comma's, ignoring")
                    writer.writerow(
                        [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])

                # if we get here the row is formatted correctly
                else:
                    writer.writerow(row)

            individual_row_count += 1
            first_row_count += 1

        print("Done!")

# close the file
f.close()
