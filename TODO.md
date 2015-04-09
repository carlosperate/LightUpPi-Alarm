# LightUpPi Alarm to-do list
- [ ] Create working full package

## LightUpAlarm
- [ ] Convert static methods into calls to an instantiated AlarmDb. This will save constructor call and might increase performance.
- [ ] Improve performance of AlarmDb calls.
- [ ] Add Pre-alert time functionality to AlarmManager.
- [ ] Add Pre-alert time functionality to AlarmCli.
- [ ] Add Snooze Time functionality to AlarmManager.
- [ ] Add Snooze Time functionality to AlarmCli.
- [ ] Change AlarmDb init to check for specifc snooze and pre-alert columns instdead of just checking if the db is empty.

## LightUpHardware
- [ ] Test switch functionality.
- [ ] Finish HardwareThread unit test.
- [ ] We only use a small subset of the Phue library, which can be easily replicated using HTTP requests, so could write a small class to control the hue light bulb brightness and ON/OFF state. 

## LightUpServer
- [ ] Add Pre-alert time functionality.
- [ ] Add Snooze time functionality.

## LightUpWeb
- [ ] Create Web interface using Angular Angular bootstrap

## OS specific
- [ ] Nothing yet
