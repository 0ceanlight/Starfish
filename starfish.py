# Created by Oceanlight

import argparse

# subprocess -> cpy, bash exec, webbrowser -> open links
import subprocess, webbrowser

from SQLupdate import *
from SQLquery import *

# argparse
# {} required, [] optional, <> not added
# $ this {subjectName ...} [--zoom, -z] [--openurls, -o] <--seturl / --removeurl <url: str>> <--remove (subject)>

# Create the parser (this need a better name btw)
my_parser = argparse.ArgumentParser(
    prog='sch', 
    usage='%(prog)s subject [options]',
    description='Open urls and open zoom meetings associated with a subject')

my_parser.add_argument(
    '-s',
    '--subject',
    action='store', 
    type=str, 
    required=True
)

my_parser.add_argument(
    '-z',
    '--zoom',
    action='store_true',
    help='open zoom meeting associated with specified subject')

my_parser.add_argument(
    '-o', 
    '--openurls', 
    action='store_true', 
    help='open urls associated with specified subject'
)

args = my_parser.parse_args()


if (id := getSubjectID(args.subject)) != None:
    print(id)
else:
    # raise NameError('subject does not exist')
    print("Error: subject does not exist - enter an existing subject")
    exit()



# this thingy[0] stuff is ridiculous
# but I don't wanna create an array in subjectUrls() either D:
if args.openurls:
    for url in getSubjectURLs(id):
        webbrowser.open(url, new=1)

if args.zoom:
    if (zoomURL := getSubjectZoomURL(id)) != None and (zoomPass := getSubjectZoomPasscode(id)) != None:
        # open link in zoom
        bashCommand = "open -a zoom.us " + zoomURL
        subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)

        # TODO: automate password entry
        # yank zoom password to clipboard (yeah I use vim haha)
        subprocess.run("pbcopy", universal_newlines=True, input=zoomPass)


# print(args.subject)
# print(args.zoom)
# print(args.openurls)
