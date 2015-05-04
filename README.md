# LightUpPi Alarm

This is a Clock Alarm System, with lights and mains socket switch control for the Raspberry Pi.

It has been modularised into the following packages:

* __LightUpAlarm__: Completely independent Python package to manage alarms (create, edit, and delete Alarms; and executes a callback function on alarm alert).
* __LightUpHardware__: Controls external hardware to complement the alarm alert, in this case controls the room lights, mains socket switch, and snooze functionality from a physical button.
* __LightUpServer__: Creates an HTTP server to interface with the LightUpAlarm system using a web interface or JSON (used in the LightUpDroid Android app).
* __LightUpWeb__: Front-end web interface for the LightUpServer. 

Additionally, an Android application can be used to interface with the LightUpPi Alarm system. For more information about this app please visit its repository: [LightUpDrop Alarm][1]

## Installing LightUpPi Alarm

This application has been been develop to run a Raspberry Pi with Python 2.7. The project currently aims to maintain compatibility with Python 3. 

Install the dependencies described below. Then download this repository, by clicking [here][2] or running the following in the command line:

```
git clone git://github.com/carlosperate/LightUpPi-Alarm.git
```


### Dependencies
You can see the project dependencies on the [requirements.txt][3] file.

More information about specific dependencies can be found in each package README:
* LightUpAlarm [README][4]
* LightUpServer [README][5]
* LightUpHardware [README][6]


## Running LightUpPi Alarm
There are three different ways to run LightUpPi Alarm:

1. Using the command line interface only, by launching the application with the `-c` flag:

    ```
    python main.py -c
    ```
    
    Instructions about how to use the CLI can be found in the LightUpAlarm package [README][4].
    
    <img src="http://carlosperate.github.com/LightUpPi-Alarm/images/screenshot_cli_1.png" alt="CLI screenshot" width="60%">

2. Using the web interface only, designed to run on a headless system, by launching the program with the `-s` flag:

    ```
    python main.py -s
    ```
    
    And then pointing your browser to the following adddress: ` http://raspberrypi.local/LightUpPi ` or using the [LightUpDroid][1] app.

    <img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/clock.png" alt="Clock Screen" width="20%"> 
<img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/alarms.png" alt="Alarms Screen" width="20%"> 
<img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/timepicker.png" alt="Timepicker Screen" width="20%"> 
<img src="http://raw.githubusercontent.com/carlosperate/LightUpDroid-Alarm/master/screenshots/settings.png" alt="Settings Screen" width="20%"> 

3. Or having both the command line and the server interface running simultaneously, by launching the program with the `-s` flag:

    ```
    python main.py -b
    ```


## License
This project is licensed under The MIT License (MIT), a copy of which can be found in the [LICENSE][7] file.

[1]: http://github.com/carlosperate/LightUpDroid-Alarm
[2]: http://github.com/carlosperate/LightUpPi-Alarm/archive/master.zip
[3]: http://github.com/carlosperate/LightUpPi-Alarm/blob/master/requirements.txt
[4]: http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpAlarm/README.md
[5]: http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpServer/README.md
[6]: http://github.com/carlosperate/LightUpPi-Alarm/blob/master/LightUpHardware/README.md
[7]: http://raw.githubusercontent.com/carlosperate/LightUpPi-Alarm/master/LICENSE
