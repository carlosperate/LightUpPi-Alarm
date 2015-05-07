/**
 * @license Licensed under the Apache License, Version 2.0 (the "License"):
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * @fileoverview Javascript for the Weather and solar altitude graph.
 *
 * Requires jQuery to be already loaded on the page.
 *
 * TODO: For now only the updateWeatherData() function uses jQuery, done because
 *       the needed timezone library alredy requires it, so no need to reinvent
 *       the wheel, but both instances only use it for the Ajax calls, so this
 *       dependency could be removed.
 */
'use strict';

/** Create a namespace for the application. */
var WeatherGraph = WeatherGraph || {};

/** Add Skyicons instance to application. */
WeatherGraph.skycons = null;

/** Initialize the WeatherGraph on page load. */
window.addEventListener('load', function() {
  WeatherGraph.skycons = new Skycons({"color": "DimGray"});
  WeatherGraph.addSkycons();
  WeatherGraph.updateWeatherData();
});

/**
 * Adds the Skycons canvas into the DOM. Something should be loaded on the page
 * in case the weather data takes to long to load, or there is an error.
 */
WeatherGraph.addSkycons = function() {
  for (var i = 0; i < 8; i++) {
    WeatherGraph.skycons.add("weather"+i, Skycons.PARTLY_CLOUDY_DAY);
  }
  WeatherGraph.skycons.play();
};

/**
 * Request the weather forecast with 3 hour updates from OpenWeatherMap for
 * Wolverhampton.
 */
WeatherGraph.updateWeatherData = function() {
  var city = 2633691;  // Wolverhampton
  var weatherJsonUrl = "http://api.openweathermap.org/data/2.5/forecast" + 
                       "?id=" + city + "&units=metric";

  $.get(weatherJsonUrl, WeatherGraph.processWeather).error(function() {
    alert("Something went wrong fetching the weather data.");
  });
};

/**
 * Process the JSON data received from OpenWeatherMap to update the DOM weather
 * icons and temperatures.
 * @param {!string|object} jsonReturned JSON data from OpenWeatherMap.
 */
WeatherGraph.processWeather = function(jsonReturned) {
  var weatherJsonObject = WeatherGraph.parseWeatherJson(jsonReturned);
  var dayData = weatherJsonObject.list;

  // The list included in the JSON object contains 16 days of data in 3h
  // intervals that might start in the past, so iterate until closest time
  var nowEpochSecs = new Date().getTime() / 1000;
  var nowEpochRemainder = nowEpochSecs % (3 * 60 * 60);
  var nowEpochRounded = nowEpochSecs - nowEpochRemainder + (3 * 60 * 60);
  if (nowEpochRemainder > (1.5 * 60 * 60)) {
    nowEpochRounded += (3 * 60 * 60);
  }

  var nowIndex = 0;
  while (dayData[nowIndex].dt != nowEpochRounded) {
    nowIndex++;
  }
  for (var i = 0; i < 8; i++) {
    WeatherGraph.skycons.set(
        "weather"+i,
        WeatherGraph.weatherToIcon(dayData[nowIndex+i].weather[0].icon));
    var tempSpan = document.getElementById("temp"+i);
    tempSpan.innerHTML = dayData[nowIndex+i].main.temp + " °C";
    //console.log(JSON.stringify(dayData[i], null, 2));
  }
};

/**
 * Converts the weather icon to load from the OpenWeatherMap JSON data to the 
 * equivalent Skycons icon.
 * @param {!string} iconStr String from the OpenWeatherMap JSON data, represents
 *                          its icon to load.
 * @return {function} Skycons function required for skycons.add()
 */
WeatherGraph.weatherToIcon = function(iconStr) {
  if (iconStr === "01d") {
    return Skycons.CLEAR_DAY;
  } else if (iconStr === "01n") {
    return Skycons.CLEAR_NIGHT;
  } else if (iconStr === "02d") {
    return Skycons.PARTLY_CLOUDY_DAY;
  } else if (iconStr === "02n") {
    return Skycons.PARTLY_CLOUDY_NIGHT;
  } else if ((iconStr === "03d") || (iconStr === "03n") ||
             (iconStr === "04d") || (iconStr === "04n")) {
    return Skycons.CLOUDY;
  } else if ((iconStr === "09d") || (iconStr === "09n") ||
             (iconStr === "10d") || (iconStr === "10n") ||
             (iconStr === "11d") || (iconStr === "11n")) {
    return Skycons.RAIN;
  } else if ((iconStr === "13d") || (iconStr === "13n")) {
    return Skycons.SNOW;
  } else if ((iconStr === "50d") || (iconStr === "50n")) {
    return Skycons.FOG;
  } else {
    console.log('icon ' + iconStr + ' not recognised');
    return null;
  }
};

/**
 * Ensures the data received from the server is converted to a JSON object.
 * @param {!string|object} jsonReturned JSON data from OpenWeatherMap.
 * @return {JSON object} Parsed JSON object.
 */
WeatherGraph.parseWeatherJson = function (jsonReturned) {
  var jsonObject = null
  if (typeof jsonReturned =='object') {
    jsonObject = jsonReturned;
  } else {
    try {
      jsonObject = JSON.parse(jsonReturned); 
    } catch(e) {
      alert('Error parsing the JSON string from server.');
      return;
    }
  }
  if (jsonObject.cod != '200') {
    alert('Error '+ jsonObject.cod + ' ('+ jsonObject.message +')');
    return;
  }
  return jsonObject;
};
