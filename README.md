# TFL Cycle Data
A repo to gather statistics from historical Santander cycle data in London

## Contents
`s3_test.py` is used to iterating over the `journey_links.json` and download each csv, formating the file row by row, and writing to a master csv file.

`santander_test.py` is used to iterate over the master csv file and log all journeys for a particular bike, and write these to a new csv file in chronological order.