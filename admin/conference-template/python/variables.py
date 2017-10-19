#!/usr/bin/python
import sys, os
import ConfigParser

config_file = os.path.join(os.path.dirname(__file__), '../config.properties')
config_parser = ConfigParser.RawConfigParser()
config_parser.read(config_file)
config = {key.upper(): value for key, value in config_parser.items('config')}

CONFERENCE_ID = config['CONFERENCE_ID']
SUBMISSION_TIMESTAMP = config['SUBMISSION_TIMESTAMP']
REVIEW_TIMESTAMP = config['REVIEW_TIMESTAMP']

ADMIN = CONFERENCE_ID + '/Admin'
PROGRAM_CHAIRS = CONFERENCE_ID + '/Program_Chairs'
AREA_CHAIRS = CONFERENCE_ID + '/Area_Chairs'
REVIEWERS = CONFERENCE_ID + '/Reviewers'

SUBMISSION_ID = CONFERENCE_ID + '/-/' + config['SUBMISSION_NAME']
COMMENT_ID = CONFERENCE_ID + '/-/Comment'

objects = {}

"""
GROUPS

"""
objects['groups'] = {
    CONFERENCE_ID: {
        'readers': ['everyone'],
        'writers': [CONFERENCE_ID],
        'signatories': [CONFERENCE_ID],
        'web_template': os.path.join(os.path.dirname(__file__), '../webfield/conference.webfield'),
    },
    PROGRAM_CHAIRS: {
        'readers': [CONFERENCE_ID, PROGRAM_CHAIRS],
        'writers': [CONFERENCE_ID],
        'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS],
        'signatures': [CONFERENCE_ID],
        'web_template': os.path.join(os.path.dirname(__file__), '../webfield/programchair.webfield'),
    },
    AREA_CHAIRS: {
        'readers': [CONFERENCE_ID, PROGRAM_CHAIRS, AREA_CHAIRS],
        'writers': [CONFERENCE_ID],
        'signatories': [CONFERENCE_ID, AREA_CHAIRS],
        'signatures': [CONFERENCE_ID],
        'web_template': os.path.join(os.path.dirname(__file__), '../webfield/areachair.webfield'),
    },
    REVIEWERS: {
        'readers': [CONFERENCE_ID],
        'writers': [CONFERENCE_ID],
        'signatories': [CONFERENCE_ID],
        'signatures': [CONFERENCE_ID]
    },
}


"""
INVITATIONS

"""

objects['invitations'] = {
    SUBMISSION_ID: {
        'readers': ['everyone'],
        'writers': [CONFERENCE_ID],
        'invitees': ['~'],
        'signatures': [CONFERENCE_ID],
        'process_template': os.path.join(os.path.dirname(__file__), '../process/submission.process'),
        'duedate': SUBMISSION_TIMESTAMP,
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': None,
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '~.*'
            },
            'writers': {
                'values': []
            },
            'content':{
                'title': {
                    'description': 'Title of paper (up to 250 chars).',
                    'order': 1,
                    'value-regex': '.{1,250}',
                    'required':True
                },
                'authors': {
                    'description': 'Comma separated list of author names.',
                    'order': 2,
                    'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                    'required':True
                },
                'authorids': {
                    'description': 'Comma separated list of author email addresses, lowercase, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
                    'order': 3,
                    'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                    'required':True
                },
                'keywords': {
                    'description': 'Comma separated list of keywords.',
                    'order': 6,
                    'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
                },
                'TL;DR': {
                    'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper (up to 250 chars)',
                    'order': 7,
                    'value-regex': '[^\\n]{0,250}',
                    'required':False
                },
                'abstract': {
                    'description': 'Abstract of paper (up to 5000 chars).',
                    'order': 8,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'required':True
                },
                'pdf': {
                    'description': 'Upload a PDF file that ends with .pdf',
                    'order': 9,
                    'value-regex': 'upload',
                    'required':True
                }
            }
        }
    },
    COMMENT_ID: {
        'readers': ['everyone'],
        'writers': [CONFERENCE_ID],
        'invitees': ['~'],
        'signatures': [CONFERENCE_ID],
        'process_template': os.path.join(os.path.dirname(__file__), '../process/comment.process'),
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': SUBMISSION_ID,
            'readers': {
                'description': 'The users who will be allowed to read the above content.',
                'values': ['everyone']
            },
            'signatures': {
                'description': 'How your identity will be displayed with the above content.',
                'values-regex': '~.*'
            },
            'writers': {
                'values-regex': '~.*'
            },
            'content':{
                'title': {
                    'order': 0,
                    'value-regex': '.{1,500}',
                    'description': 'Brief summary of your comment (up to 500 chars).',
                    'required': True
                },
                'comment': {
                    'order': 1,
                    'value-regex': '[\\S\\s]{1,5000}',
                    'description': 'Your comment or reply (up to 5000 chars).',
                    'required': True
                }
            }
        }
    },
}

review_params = {
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'process_template': os.path.join(os.path.dirname(__file__), '../process/officialReview.process'),
    'reply': {
        'title': {
            'order': 1,
            'value-regex': '.{0,500}',
            'description': 'Brief summary of your review (up to 500 chars).',
            'required': True
        },
        'review': {
            'order': 2,
            'value-regex': '[\\S\\s]{1,5000}',
            'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons (up to 5000 chars).',
            'required': True
        },
        'rating': {
            'order': 3,
            'value-dropdown': [
                '5: Top 15% of accepted papers, strong accept',
                '4: Top 50% of accepted papers, clear accept',
                '3: Marginally above acceptance threshold',
                '2: Marginally below acceptance threshold',
                '1: Strong rejection'
            ],
            'required': True
        },
        'confidence': {
            'order': 4,
            'value-radio': [
                '3: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
                '2: The reviewer is fairly confident that the evaluation is correct',
                '1: The reviewer\'s evaluation is an educated guess'
            ],
            'required': True
        }
    }
}

