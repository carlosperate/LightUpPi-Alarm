/**
 * @license Licensed under the Apache License, Version 2.0 (the "License"):
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * @fileoverview Main LightUpPi app javascript
 */
'use strict';

/** Create a namespace for the application. */
var LightUpPi = LightUpPi || {};


LightUpPi.editCssTheme = function(cssFile) {
  cssFile = "//bootswatch.com/cerulean/bootstrap.css";
  $("#theme-css").attr("href", cssFile);
  console.log("New CSS:" + cssFile);
};


LightUpPi.getAlarmsJson = function(cssFile) {
  return JSON.parse(
      jQuery.ajax({
        url: "http://localhost/LightUpPi/getAlarm?id=all",
        async: false
      }).responseText).alarms;
};
