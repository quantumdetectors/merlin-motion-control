# Merlin Motion Control

This is a beta version of the Merlin Motion Control. Interlock and controller for MerlinEM DMC.

## About

The Merlin Motion Control app is used in conjunction with Quantum Detector's retractable Merlin detectors and the MotionPod interlock unit from MotionLink.

## Requirements

* Anaconda 3
* Kivy 1.11.1
* Gclib for Python 3

## Usage

In the main interface you have access to all the relevant status fields and buttons for safely controlling your retractable Merlin detector using the MotionPod from MotionLink.

<div align="center">
<img src="views/static/images/main_window.png" alt="alt text" width="450" height="100%">
</div>

The main window has control buttons for Standby, Move in, Move out and Stop commands; and fields displaying the current status of the MotionLink system. In the actionbar ther are buttons for Info and Settings.


<div align="center">
<img src="views/static/images/settings_modal.png" alt="alt text" width="450" height="100%">
</div>

Settings window with advanced settings that can be adjusted and saved for the current session. On exit these settings are disregarded, and the default ones are loaded on relaunching the application.

<div align="center">
<img src="views/static/images/info_modal.png" alt="alt text" width="450" height="100%">
</div>

Info window with name of software, version and copyright notice.

### Buttons
* Standby: Moves the detector in to the standby position.
* Move in: Moves the detector in to the requested position.
* Move out: Moves the detector out. When it reaches position 0 a stop command is issued. The detector will temporarily be at a negative position, but adjust itself back to 0 before its current state is changed to retracted.
* Stop: Stops any ongoing movement of the detector and changes the current state to 'Stopped', upon which the detector can't be moved in. Move Out needs to be clicked before Move In can be used again.

### Status fields
* Requested State / Current State:
    *'Stopped' if the Stop button has recently been pressed.
    *'Moving' if a requested move in/move out or standby request has not been completed.
    *'Inserted' if no other command is issued after 'Move in', and Requested Position and Position are equal.
    *'Retracted' if no other command is issued after 'Move out' and Position equals 0.
* Gatan In: Value read from the MotionLink unit based on interlock set up.
    *'Yes': If the Gatan detector is inserted into the detector chamber.
    *'No': If the Gatan detector is out.
* Gatan Veto:
    *'Yes': If the interlock has been activated.
        * If Merlin is retracted and the Gatan detector is in: If the 'Move In' button is pressed the Merlin remains retracted.
        * If Merlin is moving and then the Gatan is inserted: The interlock overrides the insertion of the Gatan detector, moves the Merlin out until its current state is 'Retracted', then moves the Gatan detector in.
        * If Merlin is inserted and then the Gatan is inserted: Interlock override Gatan and keeps it out while retracting the Merlin. When Merlin is 'Retracted' the Gatan moves in.
* Requested Position: 3200 units equals 1 mm. This is the distance to which you want to insert the Merlin relative its retracted position. The default requested positin can be set in the settings.json file. There is a hard limit to the maximum value you can set. If you try and assign a higher value than that of the maximum value the program will automatically override your input.
* Position: The current position relative the retracted position. 3200 units equals 1 mm.

## Contributing

Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the ["fork-and-pull" Git workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962).

* Fork the repo on GitHub
* Clone the project to your own machine
* Commit changes to your own branch
* Push your work back up to your fork
* Submit a Pull request so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## License
[MIT](https://choosealicense.com/licenses/mit/)
