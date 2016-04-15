# LightUpAlarm package

This is an Alarm Clock Python package.

This README file is still under development.

## Running LightUpAlarm

### Dependencies
Currently tested on Python 2.7 and 3.4.

Install version 0.5.4 of [Dataset](http://dataset.readthedocs.org/en/latest/index.html): 
```
pip install -I dataset=0.5.4
```
Or:
```
git clone git://github.com/pudo/dataset.git
cd dataset/
git checkout 9a91f3d1139a022b8c29f7c4215f6500b9e39b75
python setup.py install
```

## Run
The LightUpAlarm can run independently with its own command line interface:
```
python LightUpAlarm
```


## Using LightUpAlarm
LightUpAlarm can be used through its Command Line Interface.

Using the UP and DOWN arrow keys will go through your command history.

If the optional module `pyreadline` is installed it will enable tab auto-completion.

![CLI screenshot](http://carlosperate.github.com/LightUpPi-Alarm/screenshots/screenshot_cli_1.png)

The following commands are available:

### active
Displays the active alarms currently running.

### add
Add an alarm using the format (days follow the 3 letter format):

```hh mm <enabled/disabled> <days to repeat>```

E.g.:
```
add 9 00 enabled Mon Fri
add 10 30 disabled sat sun
add 7 10 enabled all
add 22 55 disabled
```

### alarms
Displays all the alarms.

Use the keyword 'full' to display additional info.

### delete
Delete an alarm identified by its id, or all the alarms. E.g.:
```
delete 3
delete all
```

### edit
Edit an alarm using the following format:

```edit <alarm ID> <attribute> <new value>```

E.g.
```
edit 3 hour 9
edit 4 minute 30
edit 7 enabled no
edit 1 repeat mon fri
```

### next
Displays the next scheduled alarm to alert.

### offsetalert
Displays the currently set offset alert time, (time before the alarm alert
is triggered and used to launch any kind of process), or if accompanied
by an integer it will change the offset alert time and display the new
value. E.g.:
```
offsetalert
offsetalert 5
offsetalert -15
```

### snooze
Displays the currently set snooze time, or if accompanied by an integer it will change the snooze time and display the new value. E.g.:

```
snooze
snooze 5
```

### help
List all available commands, or display detailed help with:

```help <cmd>```

### exit
Exists the LightUp Alarm program.


## License
This project is licensed under The MIT License (MIT), a copy of which can be 
found in the `LICENSE` file.
