#!/usr/bin/python

"""

This is the initialization script for dblp.org

"""

## Import statements
import argparse
import openreview
import config

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


DBLP = client.post_group(openreview.Group(config.BASE,
             readers=['OpenReview.net'],
             writers=['OpenReview.net', config.BASE],
             signatures=['OpenReview.net'],
             signatories=[config.BASE],
             members=[]))

import_arguments = {
    'readers': ['everyone'],
    'writers': [config.GROUP],
    'invitees': [config.GROUP],
    'signatures': [config.BASE],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': [config.GROUP]
        },
        'writers': {
            'values':  [config.GROUP]
        },
        'content': {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '[\\S\\s]{0,750}',
                'required': False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 2,
                'value-regex': '[\\S\\s]{0,5000}',
                'required': False
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':False
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':False
            },
            'DBLP_url': {
                'description': 'DBLP.org url associated with this paper',
                'order': 3,
                'value-regex': '[^\\n]{0,250}',
                'required': False
            },
            'isbn': {
                'description': 'isbn number of this paper',
                'order': 5,
                'value-regex': '[^\\n]{0,20}',
                'required': False

            },
            'ee': {
                'description': 'electronic edition of the paper',
                'order': 6,
                'value-regex': '[^\\n]{0,500}',
                'required': False

            },
            'series': {
                'description': 'The name of the series the volume is a part of',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'mag_number': {
                'description': 'The number of a journal, magazine, technical '
                               'report, or of a work in a series',
                'order': 5,
                'value-regex': '[^\\n]{0,20}',
                'required': False

            },
            'month': {
                'description': 'the month in which the paper or work was published.',
                'order': 5,
                'value-regex': '.{0,200}',
                'required': False

            },
            'year': {
                'description': 'year in which paper/journal was Published',
                'order': 5,
                'value-regex': '[^\\n]{0,20}',
                'required': False

            },
            'booktitle': {
                'description': 'Title of a book, part of which is being cited',
                'order': 5,
                'value-regex': '.{0,500}',
                'required': False

            },
            'editors': {
                'description': 'Comma separated list of editor names',
                'order': 7,
                'value-regex': '[^,\\n]*(,[^,\\n]+)*',
                'required': False
            },
            'sub_type': {
                'description': 'subtype of a technical report',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'type': {
                'description': 'The type of a technical report',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'journal': {
                'description': 'A journal name.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'volume': {
                'description': 'The volume of a journal or multivolume book.',
                'order': 5,
                'value-regex': '[^\\n]{0,100}',
                'required': False

            },
            'pages': {
                'description': 'One or more page numbers or range of numbers',
                'order': 5,
                'value-regex': '[^\\n]{0,100}',
                'required': False

            },
            'crossref': {
                'description': 'The database key of the entry being cross referenced.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'chapter': {
                'description': 'A chapter (or section or whatever) number',
                'order': 5,
                'value-regex': '[^\\n]{0,8}',
                'required': False

            },
            'publisher': {
                'description': 'The publisher\'s name.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'school': {
                'description': 'The name of the school where a thesis was written.',
                'order': 5,
                'value-regex': '[^\\n]{0,250}',
                'required': False

            },
            'pub_key': {
                'description': 'a key that uniquely identifies this record. formatted as follows: <first author lastname>|<parsed title>, where <parsed title> is the title, lowercased and with spaces replaced with _ (underscore)',
                'order': 5,
                'value-regex': '[^ ]+\|[^ ]+.',
                'required': False
            }

        }
    }
}

import_invitation = client.post_invitation(openreview.Invitation('DBLP.org/-/Import', **import_arguments))


raw_arguments = {
    'readers': ['everyone'],
    'writers': [config.GROUP],
    'invitees': [config.GROUP],
    'signatures': [config.GROUP],
    'reply': {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': [config.GROUP]
        },
        'writers': {
            'values':  [config.GROUP]
        },
        'content': {
            '_dblp': {
                'description': 'raw dblp data',
                'order': 1,
                'value-regex': '.*',
                'required': True
            }
        }
    }
}


xml_invitation = client.post_invitation(openreview.Invitation('DBLP.org/-/Raw', **raw_arguments))
