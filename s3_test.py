import requests, json, csv

urls = []

#  get all urls
with open('journey_links.json') as json_file:
    json_object = json.load(json_file)

    for object in json_object["entries"]:
        urls += [object["url"]]

# print urls
for url in urls:
    print(url)

# open file
f = open('./all_trips_2.csv', 'w')
# create the csv writer
writer = csv.writer(f)

# download csv data from urls and write to master csv file
for url in urls:
    with requests.Session() as s:
        print(f'Downloading: {url}')
        download = s.get(url)

        print("Downloaded!")
        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        print("Writing to file")
        for row in my_list:
            writer.writerow(row)

        print("Done!")

# close the file
f.close()
