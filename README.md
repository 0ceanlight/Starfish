# Starfish
> Created by Oceanlight


## About
- A program created by a virtual student who saw a need for streamlining the routine tasks of opening websites, joining meetings, etc. This program makes it possible to open zoom meetings and all the urls needed for a subject at the click of a button or with only a few keystrokes. This was designed for a virtual school setting, but can be used for much more.
- [Project Trailer](https://www.youtube.com/watch?v=zphy5IjFjyM)

<br />

## Requirements

- [Python3](https://www.python.org/downloads/)

- [SQLite3](https://www.sqlite.org/download.html)

- [PyQt5](https://pypi.org/project/PyQt5/)

<br />

## Usage

### GUI version

`python3 qtGui.py`

Add a subject, and enter a subject name to make the subject more identifiable. Under 'URLs', press the '+' button to add URLs to be opened. You can optionally add a zoom URL (which needs to be valid in order to function at all), and the corresponding passcode to the meeting. This passcode will be copied to the clipboard once 'Open meeting' is clicked.

<br />

### Shell version

`python3 starfish.py [-s, --subject <subject name or alias>] [-o, --openurls] [--zoom, -z]`

`-s, --subject <subject name or alias>` - required, specify subject, or subject's alias, to perform an action

`-o, --openurls` - optional, this flag opens all subject URLs

`-z, --zoom` - optional, this opens the specified zoom URL in zoom and copies the passode to the clipboard.

Note: Subjects and their info (urls, aliases, etc.) need to be added manually using `sqlite3` (I promise this has a pleasant schema ha ha), or by using the GUI version. Note that aliases cannot be edited via the GUI.

Suggestion: Add something like `abbr starfish "python3 starfish.py -s"` to your shell config to streamline the process just a bit more.

<br />

### Planned Features
- Deploy the PyQt GUI as an application.
- Add keyboard shortcuts and menubar functions.
- Run application in the background to automatically open scheduled meetings.
- Create function to add currently open URLs to a specified subject.
- Save changes to a subject's edit menu automatically.

<br />

### Possible Issues
This has only been tested on macOS Catalina. Copying passcodes may cause issues outside of MacOS. This will successfully open meetings in `zoom.us`. Note that meetings can also be launched using a browser with the URL feature.

Be sure to let me know if you run into any other issues!
