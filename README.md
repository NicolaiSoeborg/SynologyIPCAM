Synology IPCAM
==============

[![GitHub issues](https://img.shields.io/github/issues/NicolaiSoeborg/SynologyIPCAM.svg)](https://github.com/NicolaiSoeborg/SynologyIPCAM/issues)
[![Beerpay](https://beerpay.io/NicolaiSoeborg/SynologyIPCAM/badge.svg?style=flat)](https://beerpay.io/NicolaiSoeborg/SynologyIPCAM)
[![license](https://img.shields.io/badge/License-Beerware-blue.svg)](https://github.com/NicolaiSoeborg/SynologyIPCAM/blob/master/LICENSE)

This is a simple python script to activate Synology DS Surveillance Station 7 based on inputs from a RPi PiFace.

# Files
 * `ipcam.py` - monitors events on the PiFace
 * `trigger.py` - sends http request to Syno DS SS7


# Setup
1. Create limited user in Surveillance Station and add the username and password to `trigger.py`
2. Create custom alarms in Surveillance Station for different "External Event"
3. Change `ipcam.py` s.t. `get_event()` returns a tuple containing an external event, if any changes is detected by the PiFace
4. On the Raspberry Pi type: `crontab -e` and add: `@reboot /usr/bin/tmux new-session -d -s IPCAM /home/pi/ipcam.py`
5. Make sure `pifacedigitalio` is installed: `pip install pifacedigitalio`

Reboot the Raspberry Pi and now you can at any time check the status of the script: `tmux a -t IPCAM`.


# Todo
I can't get the `InputEventListener` to work ([and might not be the only one](https://www.element14.com/community/message/166553/l/re-event-listeners-do-not-work-piface-2-with-python3#166553)), however this would make the implementation of `ipcam.py` much simpler.
