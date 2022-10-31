const url =
  "https://archive-api.open-meteo.com/v1/era5?latitude=52.52&longitude=13.41&start_date=2015-01-01&end_date=2017-07-13&hourly=temperature_2m,precipitation";
const fs = require("fs");
const converter = require("json-2-csv");

let json2csvCallback = function (err, csv) {
  if (err) throw err;
  fs.writeFile("weather.csv", csv, "utf8", function (err) {
    if (err) {
      console.log(
        "Some error occured - file either not saved or corrupted file saved."
      );
    } else {
      console.log("It's saved!");
    }
  });
};

fetch(url)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    const time = data.hourly.time;
    const temp = data.hourly.temperature_2m;
    const precipitation = data.hourly.precipitation;

    const fullArray = [];

    for (i = 0; i < time.length; i++) {
      fullArray.push({
        time: time[i],
        temp: temp[i],
        precipitation: precipitation[i],
      });
    }

    console.log(fullArray);

    converter.json2csv(fullArray, json2csvCallback, {
      prependHeader: false,
    });
  });
