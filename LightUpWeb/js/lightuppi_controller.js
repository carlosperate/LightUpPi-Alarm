/**
 * @license Licensed under the Apache License, Version 2.0 (the "License"):
 *          http://www.apache.org/licenses/LICENSE-2.0
 *
 * @fileoverview LightUpPi app AngularJS controller.
 */
'use strict';

/** Create a namespace for the application and Angular app. */
var LightUpPi = LightUpPi || {};
LightUpPi.app = angular.module('lightUpPi', ['ui.bootstrap']);

/**
 * Main controller for the LightUpPi Angular App.
 */
LightUpPi.app.controller('lightUpCtrl', function($scope) {
  // Nothing yet in the main controller.
});

/**
 * This controls the Modal launched to add a new alarm. It only controls the
 * modal execution, code within the modal is connected in 'AddAlarmCtrl'.
 */
LightUpPi.app.controller('AddAlarmModalCtrl', function ($scope, $modal, $log) {
  $scope.animationsEnabled = true;

  $scope.open = function (size) {
    var modalInstance = $modal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'addalarm.html',
      controller: 'AddAlarmCtrl',
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
        $log.info('Modal dismissed at: ' + new Date());
      }
    );
  };

});

/**
 * Mote that $modalInstance represents a modal window (instance) dependency. It
 * is not the same as the $modal service used in AddAlarmModalCtrl.
 */
LightUpPi.app.controller('AddAlarmCtrl', function ($scope, $modalInstance, $log) {
  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  $scope.mytime = new Date();
  $scope.hstep = 1;
  $scope.mstep = 1;

  $scope.ismeridian = true;
  $scope.toggleMeridianMode = function() {
    $scope.ismeridian = ! $scope.ismeridian;
  };

  $scope.changed = function () {
    $log.log('Time changed to: ' + $scope.mytime);
  };
});

/**
 * Controller for the navigation bar drop down which allows dynamic theme
 * selection.
 */
LightUpPi.app.controller('ThemeDropdownCtrl', function ($scope, $log) {
  $scope.themeCssFiles = [
    { name: "default",  link: "//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.css" },
    { name: "cerulean", link: "//bootswatch.com/cerulean/bootstrap.css" },
    { name: "cosmo",    link: "//bootswatch.com/cosmo/bootstrap.css" },
    { name: "cyborg",   link: "//bootswatch.com/cyborg/bootstrap.css" },
    { name: "flatly",   link: "//bootswatch.com/flatly/bootstrap.css" },
    { name: "journal",  link: "//bootswatch.com/journal/bootstrap.css" },
    { name: "readable", link: "//bootswatch.com/readable/bootstrap.css" },
    { name: "simplex",  link: "//bootswatch.com/simplex/bootstrap.css" },
    { name: "slate",    link: "//bootswatch.com/slate/bootstrap.css" },
    { name: "spacelab", link: "//bootswatch.com/bootswatch/bootstrap.css" },
    { name: "united",   link: "//bootswatch.com/united/bootstrap.css" },
  ];

  $scope.status = {
    isopen: false
  };

  $scope.toggled = function(open) {
    $log.log('Dropdown is now: ', open);
    LightUpPi.editCssTheme(this.css);
  };

  $scope.toggleDropdown = function($event) {
    $event.preventDefault();
    $event.stopPropagation();
    $scope.status.isopen = !$scope.status.isopen;
  };
});


/**
 *
 */
LightUpPi.app.controller('AlarmPanelController', function () {
  this.showTimestamp = true;
  this.alarms = LightUpPi.getAlarmsJson();

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
});

/**
 * Create a custom filter to always display a leading zero for < 10 digits.
 * Useful for time display.
 */
LightUpPi.app.filter('leadingzero', function() {
  return function(input) {
    if (input < 10) { 
      input = '0' + input;
    }
    return input;
  };
});
