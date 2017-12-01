#!/usr/bin/python

import sys, os
import argparse
import openreview
import config

"""

OPTIONAL SCRIPT ARGUMENTS

	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password

"""

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help = "base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl = args.baseurl, username = args.username, password = args.password)

dblp = openreview.Group(id = config.CONF, readers = ['everyone'], signatures = ['OpenReview.net'], signatories = [config.CONF])

reply = {
    'forum': None,
    'replyto': None,
    'readers': {
        'description': 'The users who will be allowed to read the above content.',
        'values': ['everyone']
    },
    'signatures': {
        'description': 'Your authorized identity to be associated with the above content.',
        'values': [dblp.id]
    },
    'writers': {
        'values': [dblp.id]
    },
    'content':{
        'title': {
            'description': 'Title of paper.',
            'order': 1,
            'value-regex': '.{1,250}',
            'required': False
        },
        'abstract': {
            'description': 'Abstract of paper.',
            'order': 2,
            'value-regex': '[\\S\\s]{1,5000}',
            'required': False
        },
        'authors': {
            'description': 'Comma separated list of author names. Please provide real names; identities will be anonymized.',
            'order': 3,
            'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
            'required': False
        },
        'authorids': {
            'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile. Please provide real emails; identities will be anonymized.',
            'order': 4,
            'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
            'required': False
        }
    }
}

invitation = openreview.Invitation(id = config.SUBMISSION, readers = ['everyone'], writers = [dblp.id], signatures = [dblp.id], reply = reply, transform = '../process/dblpTransform.js')

client.post_group(dblp)
client.post_invitation(invitation)
