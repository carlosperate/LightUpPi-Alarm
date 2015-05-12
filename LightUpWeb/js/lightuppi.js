/**
 * @license Licensed under the Apache License, Version 2.0 (the "License"):
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * @fileoverview Main LightUpPi app javascript.
 */
"use strict";

/** Create/reuse the namespace for the application. */
var LightUpPi = LightUpPi || {};

/** List of bootstrap CSS themes and URLs */
LightUpPi.themeList = [
  { "name": "default",   "link": "css/bootstrap.default.min.css" },
  { "name": "cerulean",  "link": "css/bootstrap.cerulean.min.css" },
  { "name": "cosmo",     "link": "css/bootstrap.cosmo.min.css" },
  { "name": "custom",    "link": "css/bootstrap.custom.min.css" },
  { "name": "cyborg",    "link": "css/bootstrap.cyborg.min.css" },
  { "name": "darkly",    "link": "css/bootstrap.darkly.min.css" },
  { "name": "flatly",    "link": "css/bootstrap.flatly.min.css" },
  { "name": "journal",   "link": "css/bootstrap.journal.min.css" },
  { "name": "lumen",     "link": "css/bootstrap.lumen.min.css" },
  { "name": "paper",     "link": "css/bootstrap.paper.min.css" },
  { "name": "readable",  "link": "css/bootstrap.readable.min.css" },
  { "name": "sandstone", "link": "css/bootstrap.sandstone.min.css" },
  { "name": "simplex",   "link": "css/bootstrap.simplex.min.css" },
  { "name": "slate",     "link": "css/bootstrap.slate.min.css" },
  { "name": "spacelab",  "link": "css/bootstrap.spacelab.min.css" },
  { "name": "superhero", "link": "css/bootstrap.superhero.min.css" },
  { "name": "united",    "link": "css/bootstrap.united.min.css" },
  { "name": "yeti",      "link": "css/bootstrap.yeti.min.css" }
];

/** Initialize the LightUpPi js on page load. */
window.addEventListener("load", function load(event) {
  window.removeEventListener("load", load, false);
  LightUpPi.loadUrlTheme();
}, false);

/**
 * Edits the bootstrap CSS theme file to that indicated in the input.
 * @param {string} cssFile String with the address of the CSS file to load.
 */
LightUpPi.editCssTheme = function(cssFile) {
  document.getElementById("theme-css").setAttribute("href", cssFile);
  console.log("New CSS: " + cssFile);
};

/**
 * Checks if a specif theme has been requested using URL parameter "theme=x".
 * Where "x" is the theme name. It then loads the theme css file.
 */
LightUpPi.loadUrlTheme = function() {
  var found = false;
  var theme = LightUpPi.getUrlParam("theme");
  if (theme) {
    for (var i=0; i < LightUpPi.themeList.length; i++) {
      if (LightUpPi.themeList[i].name == theme) {
        // Array defined in this file, so can count the link is not undefined
        LightUpPi.editCssTheme(LightUpPi.themeList[i].link);
        found = true;
      }
    }
    if (found === false) {
      alert("URL theme '" + theme + "' not found !");
    }
  }
};

/**
 * Gets the URL query string, divides it into parameters and returns the value
 * of the parameter defined in the argument
 * @param {string} variable Name of the parameter which value is to be returned
 * @return {string} Value of the parameter indicated in the argument.
 *                  Null if parameter not found. 
 */
LightUpPi.getUrlParam = function(param) {
  var queryString = window.location.search.substring(1);
  var parameters = queryString.split("&");
  for (var i = 0; i < parameters.length; i++) {
    var paramValue = parameters[i].split("=");
    if (paramValue[0] == param) {
      return paramValue[1];
    }
  }
  return(null);
};
