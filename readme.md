# CutWire

## Introduction
CutWire is a plugin created for [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python).  As such, it requires [Source.Python](https://github.com/Source-Python-Dev-Team/Source.Python) to be installed on your CS:S or CS:GO game server.  The plugin gives players the option of cutting one of four wires instead of attempting to defuse the bomb on CS:S and CS:GO.

## Installation
To install, simply download the current release from its [release thread](https://forums.sourcepython.com/viewtopic.php?t=779) and install it into the main directory on your server.  Once you have installed CutWire on your server, simply add the following to your autoexec.cfg file:
```
sp plugin load cut_wire
```

## Configuration
After having loaded the plugin once, a configuration file will have been created on your server at **../cfg/source-python/cut_wire.cfg**  Edit that file to your liking.  The current default configuration file looks like:
```
// Options
//   * 1 = Always send the defuser a menu.
//   * 2 = Only send menu when not enough time.
//   * 3 = Send menu when not enough time or not using a kit.
// Default Value: 1
// Send the defuser a menu on specified occasions.
   cw_send_menu 1


// Options
//   * 0 = Do not have bot cut wire.
//   * 1 = Have bot cut wire only if not enough time to defuse.
//   * 2 = Always have bot cut wire.
// Default Value: 0
// Automatically have bots cut wire on defuse.
   cw_bot_choose_wire 0
```

## Screenshots
The following are screenshots of the menu and messages that accompany this plugin:

**CS:GO Menu:**

![CSGO Menu](https://raw.githubusercontent.com/satoon101/CutWire/screenshots/csgo_menu.png "CS:GO Menu")

**CS:GO cut correct wire:**

![CSGO Correct](https://raw.githubusercontent.com/satoon101/CutWire/screenshots/csgo_correct_wire.png "CS:GO Correct")

**CS:GO cut wrong wire:**

![CSGO Wrong](https://raw.githubusercontent.com/satoon101/CutWire/screenshots/csgo_wrong_wire.png "CS:GO Wrong")

**CS:S Menu:**

![CSS Menu](https://raw.githubusercontent.com/satoon101/CutWire/screenshots/css_menu.png "CS:S Menu")

**CS:S cut correct wire:**

![CSS Correct](https://raw.githubusercontent.com/satoon101/CutWire/screenshots/css_correct_wire.png "CS:S Correct")

**CS:S cut wrong wire:**

![CSS Wrong](https://raw.githubusercontent.com/satoon101/CutWire/screenshots/css_wrong_wire.png "CS:S Wrong")
