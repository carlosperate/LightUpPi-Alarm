# LightUpPi Alarm

This is a Clock Alarm System, with lights and mains socket switch control for the Raspberry Pi.

It has been modularised into the following packages:

* __LightUpAlarm__: Completely independent Python package to manage alarms (create, edit, delete, and run alarms).
* __LightUpHardware__: Controls external hardware to complement the alarm ring, in this case controls the room lights, mains socket switch, and snooze functionality from a physical button.
* __LightUpServer__: Creates an HTTP server to interface with the LightUpAlarm system using a web interface or JSON (used in the LightUpDroid Android app).
* __LightUpWeb__: Front-end web interface for the LightUpServer. 

Additionally, an Android application can be used to interface with the LightUpPi Alarm system. For more information about this app please visit its repository: [LightUpDrop Alarm](http://github.com/carlosperate/LightUpDroid-Alarm)

## Installing LightUpPi Alarm

This application has been been develop to run a Raspberry Pi with Python 2.7. The project currently aims to maintain compatibility with Python 3. 

Install the dependencies described below. Then download this repository, by clicking [here](http://github.com/carlosperate/LightUpPi-Alarm/archive/master.zip) or running the following in the command line:

```
git clone git://github.com/carlosperate/LightUpPi-Alarm.git
```


### Dependencies
Each one of the Python packages has its own dependencies, please read their respective READMEs:
* LightUpAlarm [README](http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpAlarm/README.md)
* LightUpServer [README](http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpServer/README.md)
* LightUpHardware [README](http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpHardware/README.md)


## Running LightUpPi Alarm
There are two different ways to run LightUpPi Alarm:

1. Using the command line using, by launching the application with the `-c` flag:

    ```
    python main.py -c
    ```
    
    Instructions about how to use the CLI can be found in the LightUpAlarm package [README](http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpAlarm/README.md).
    
    <img src="http://carlosperate.github.com/LightUpPi-Alarm/images/screenshot_cli_1.png" alt="CLI screenshot" width="60%">

2. Or using the web interface, by launching the program with the `-s` flag:

    ```
    python main.py -s
    ```
    
    And then pointing your browser to the following adddress: ` http://raspberrypi.local/LightUpPi ` or using the [LightUpDroid](http://github.com/carlosperate/LightUpDroid-Alarm) app.

    <img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/clock.png" alt="Clock Screen" width="20%"> 
<img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/alarms.png" alt="Alarms Screen" width="20%"> 
<img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/timepicker.png" alt="Timepicker Screen" width="20%"> 
<img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/settings.png" alt="Settings Screen" width="20%"> 


## License
This project is licensed under The MIT License (MIT), a copy of which can be found in the [LICENSE](http://raw.githubusercontent.com/carlosperate/LightUpPi-Alarm/master/LICENSE) file.
