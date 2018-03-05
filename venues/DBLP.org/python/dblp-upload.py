import argparse
import sys
import htmlentitydefs
import xml.etree.ElementTree as ET
from xml.etree  import ElementTree
from openreview import *
import config
from multiprocessing import Pool


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

def post_with_retries(note):
	response = None
	count = 0
	while response is None and count < 5:
		try:
			response = client.post_note(note)
		except requests.exceptions.ConnectionError:
			count += 1

	if not response:
		print 'Could not post the note', note.content.dblp

	return response

def post_note(elem):
	note = openreview.Note(content = { 'dblp': ElementTree.tostring(elem, encoding='utf8', method='xml') }, invitation = config.SUBMISSION, readers = ['everyone'], writers = [config.CONF], signatures = [config.CONF])
	saved_note = post_with_retries(note)
	if saved_note.invitation != config.SUBMISSION:
		print 'Existent submission', saved_note.id
	else
		print elem.get('key') + ',' + saved_note.id

p = Pool(4)
elem_buffer = []
for event, elem in context:

	if elem.tag in ['article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'person', 'data']:

		elem_buffer.append(elem)

		if len(elem_buffer) > 1000:
			p.map(post_note, elem_buffer[:])
			elem_buffer = []
