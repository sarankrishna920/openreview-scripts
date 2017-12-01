import argparse
import sys
import htmlentitydefs
import xml.etree.ElementTree as ET
from xml.etree  import ElementTree
from openreview import *
import config


parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--file', help="filter containing the DBLP papers");

args = parser.parse_args()

client = openreview.Client(baseurl = args.baseurl, username = args.username, password = args.password)

# http://stackoverflow.com/a/10792473/190597 (lambacck)
parser = ET.XMLParser()
parser.entity.update((x, unichr(i)) for x, i in htmlentitydefs.name2codepoint.iteritems())
context = ET.iterparse(args.file, events = ('end', ), parser=parser)

count = 0

for event, elem in context:
    if elem.tag in ['article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www', 'person', 'data']:

    	note = openreview.Note(content = { 'dblp': ElementTree.tostring(elem, encoding='utf8', method='xml') }, invitation = config.SUBMISSION, readers = ['everyone'], writers = [config.CONF], signatures = [config.CONF])

        saved_note = client.post_note(note)

        print saved_note.id

        count = count + 1

        if count > 10:
        	break
