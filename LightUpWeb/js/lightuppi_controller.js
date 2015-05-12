/**
 * @license Licensed under the Apache License, Version 2.0 (the "License"):
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * @fileoverview LightUpPi app AngularJS controller.
 */
"use strict";

/** Create/reuse the namespace for the application and Angular app. */
var LightUpPi = LightUpPi || {};
LightUpPi.app = angular.module("lightUpPi", ["ui.bootstrap"]);

/**
 * Main controller for the LightUpPi Angular App.
 */
LightUpPi.app.controller("lightUpCtrl", ["$scope", function($scope) {
  // Nothing yet in the main controller.
}]);

/**
 * This controls the Modal launched to add a new alarm. It only controls the
 * modal execution, code within the modal is connected in 'AddAlarmCtrl'.
 */
LightUpPi.app.controller("AddAlarmModalCtrl", ["$scope", "$modal", "$log",
    function ($scope, $modal, $log) {
  $scope.animationsEnabled = true;

  $scope.open = function (size) {
    var modalInstance = $modal.open({
      animation: $scope.animationsEnabled,
      templateUrl: "addalarm.html",
      controller: "AddAlarmCtrl",
      size: size,
      resolve: {
        items: function () {
          return $scope.items;
        }
      }
    });

    modalInstance.result.then(
      function (selectedItem) {
        $scope.selected = selectedItem;
      },
      function () {
        $log.info("Modal dismissed at: " + new Date());
      }
    );
  };

}]);

/**
 * Mote that $modalInstance represents a modal window (instance) dependency. It
 * is not the same as the $modal service used in AddAlarmModalCtrl.
 */
LightUpPi.app.controller("AddAlarmCtrl", ["$scope", "$modalInstance", "$log",
    function ($scope, $modalInstance, $log) {
  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss("cancel");
  };

  $scope.mytime = new Date();
  $scope.hstep = 1;
  $scope.mstep = 1;

  $scope.ismeridian = true;
  $scope.toggleMeridianMode = function() {
    $scope.ismeridian = ! $scope.ismeridian;
  };

  $scope.changed = function () {
    $log.log("Time changed to: " + $scope.mytime);
  };
}]);

/**
 * Controller for the navigation bar drop down which allows dynamic theme
 * selection.
 */
LightUpPi.app.controller("ThemeDropdownCtrl", ["$scope", "$log", "$window", "$location",
    function ($scope, $log, $window, $location) {
  this.themeCssFiles = LightUpPi.themeList;

  this.editCssTheme = function(themeName, cssFile) {
    LightUpPi.editCssTheme(cssFile);
    // Edit the address bar location without reloading the page
    $location.url("/?theme=" + themeName).replace();
  };

  $scope.status = {
    isopen: false
  };

  $scope.toggled = function(open) {
    $log.log("Dropdown is now: ", open);
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };
}]);

/**
 * Controller for the Alarm Panels. It collects the JSON data from the server
 * and creates a panel per Alarm with all its information.
 */
LightUpPi.app.controller("AlarmPanelController", ["$http", function ($http) {
  var context = this; 
  this.showTimestamp = true;
  this.alarms = [];
  $http.get("http://localhost/LightUpPi/getAlarm?id=all")
       .success(function(data) {
         context.alarms = data.alarms;
       });

  // Returns a string to indicate if the alarm is enabled or disabled
  this.enabledButtonText = function(enabled) {
    if (enabled) {
      return "Enabled";
    } else {
      return "Disabled";
    }
  };

  // Formats a string to list the repeat days
  this.formatedRepeat = function(alarm) {
    var d = "---"
    var strArray = [];
    if (alarm.monday)    { strArray.push("Mon"); } else { strArray.push(d); }
    if (alarm.tuesday)   { strArray.push("Tue"); } else { strArray.push(d); }
    if (alarm.wednesday) { strArray.push("Wed"); } else { strArray.push(d); }
    if (alarm.thursday)  { strArray.push("Thu"); } else { strArray.push(d); }
    if (alarm.friday)    { strArray.push("Fri"); } else { strArray.push(d); }
    if (alarm.saturday)  { strArray.push("Sat"); } else { strArray.push(d); }
    if (alarm.sunday)    { strArray.push("Sun"); } else { strArray.push(d); }
    return strArray.join(" ");
  };
}]);

/**
 * Create a custom filter to always display a leading zero for < 10 digits.
 * Useful for time display.
 */
LightUpPi.app.filter("leadingzero", function() {
  return function(input) {
    if (input < 10) { 
      input = "0" + input;
    }
    return input;
  };
});
