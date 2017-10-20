#!/usr/bin/python
import sys, os
import ConfigParser

class Variables:

    def init(self, conference_dir):

        def parse_properties(file, section):
            config = ConfigParser.RawConfigParser()
            config.read(file)
            return {key.upper(): value for key, value in config.items(section)}

        # load config
        config_file = os.path.join(conference_dir, 'config.properties')
        config = parse_properties(config_file, 'config')
        options = parse_properties(config_file, 'options')

        CONFERENCE_ID = config['CONFERENCE_ID']
        SUBMISSION_TIMESTAMP = config['SUBMISSION_TIMESTAMP']
        REVIEW_TIMESTAMP = config['REVIEW_TIMESTAMP']

        ADMIN = CONFERENCE_ID + '/Admin'
        PROGRAM_CHAIRS = CONFERENCE_ID + '/Program_Chairs'
        AREA_CHAIRS = CONFERENCE_ID + '/Area_Chairs'
        REVIEWERS = CONFERENCE_ID + '/Reviewers'

        self.SUBMISSION_ID = CONFERENCE_ID + '/-/' + config['SUBMISSION_NAME']
        self.COMMENT_ID = CONFERENCE_ID + '/-/Public_Comment'

        self.initial_objects = {}

        """
        GROUPS

        """
        self.initial_objects['groups'] = {
            CONFERENCE_ID: {
                'readers': ['everyone'],
                'writers': [CONFERENCE_ID],
                'signatories': [CONFERENCE_ID],
                'web_template': os.path.join(conference_dir, 'webfield/conference.webfield'),
            },
            PROGRAM_CHAIRS: {
                'readers': [CONFERENCE_ID, PROGRAM_CHAIRS],
                'writers': [CONFERENCE_ID],
                'signatories': [CONFERENCE_ID, PROGRAM_CHAIRS],
                'signatures': [CONFERENCE_ID],
                'web_template': os.path.join(conference_dir, 'webfield/programchair.webfield'),
            },
            REVIEWERS: {
                'readers': [CONFERENCE_ID],
                'writers': [CONFERENCE_ID],
                'signatories': [CONFERENCE_ID],
                'signatures': [CONFERENCE_ID]
            },
        }
        if options['AC_ENABLED'].lower() == 'true':
            self.initial_objects['groups'][AREA_CHAIRS] = {
                'readers': [CONFERENCE_ID, PROGRAM_CHAIRS, AREA_CHAIRS],
                'writers': [CONFERENCE_ID],
                'signatories': [CONFERENCE_ID, AREA_CHAIRS],
                'signatures': [CONFERENCE_ID],
                'web_template': os.path.join(conference_dir, 'webfield/areachair.webfield'),
            }

        """
        INVITATIONS

        """

        self.initial_objects['invitations'] = {
            self.SUBMISSION_ID: {
                'readers': ['everyone'],
                'writers': [CONFERENCE_ID],
                'invitees': ['~'],
                'signatures': [CONFERENCE_ID],
                'process_template': os.path.join(conference_dir, 'process/submission.process'),
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
            self.COMMENT_ID: {
                'readers': ['everyone'],
                'writers': [CONFERENCE_ID],
                'invitees': ['~'],
                'signatures': [CONFERENCE_ID],
                'process_template': os.path.join(conference_dir, 'process/comment.process'),
                'reply': {
                    'forum': None,
                    'replyto': None,
                    'invitation': self.SUBMISSION_ID,
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
            'process_template': os.path.join(conference_dir, 'process/officialReview.process'),
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

        """
        Per-paper invitation parameters
        """

        self.maskAuthorsGroup = CONFERENCE_ID + "/Paper[PAPER_NUMBER]/Authors"
        self.maskReviewerGroup = CONFERENCE_ID + "/Paper[PAPER_NUMBER]/Reviewers"
        self.maskAreaChairGroup = CONFERENCE_ID + "/Paper[PAPER_NUMBER]/Area_Chair"
        self.maskAnonReviewerGroup = CONFERENCE_ID + "/Paper[PAPER_NUMBER]/AnonReviewer[0-9]+"

        self.invitation_configurations = {
            self.COMMENT_ID: {
                'byPaper': True,
                'byForum': True,
                'invitees': ['~'],
                'noninvitees': [self.maskAuthorsGroup, self.maskReviewerGroup, self.maskAreaChairGroup],
                'params': self.initial_objects['invitations'][self.COMMENT_ID],
            },
            'Add_Revision': {
                'byPaper': True,
                'invitees': [self.maskAuthorsGroup],
                'byForum': True,
                'reference': True,
                'params': {
                    'readers': ['everyone'],
                    'writers': [CONFERENCE_ID],
                    'invitees': [], # set during submission process function; replaced in invitations.py
                    'signatures': [CONFERENCE_ID],
                    'reply': {
                        'forum': None,
                        'referent': None,
                        'signatures': self.initial_objects['invitations'][self.SUBMISSION_ID]['reply']['signatures'],
                        'writers': self.initial_objects['invitations'][self.SUBMISSION_ID]['reply']['writers'],
                        'readers': self.initial_objects['invitations'][self.SUBMISSION_ID]['reply']['readers'],
                        'content': self.initial_objects['invitations'][self.SUBMISSION_ID]['reply']['content']
                    }
                },
            },
            'Official_Comment': {
                'byPaper': True,
                'byForum': True,
                #'invitees': [self.maskReviewerGroup, self.maskAuthorsGroup, self.maskAreaChairGroup, config.PROGRAM_CHAIRS],
                #'signatures': [self.maskAnonReviewerGroup, self.maskAuthorsGroup, self.maskAreaChairGroup, config.PROGRAM_CHAIRS],
                #'params': config.official_comment_params
            },
            'Official_Review': {
                'byPaper': True,
                'invitees': [self.maskReviewerGroup],
                'signatures': [self.maskAnonReviewerGroup],
                'byForum': True,
                'byReplyTo': True,
                #'params': config.official_review_params
            },
            'Meta_Review': {
                'byPaper': True,
                'byForum': True,
                'byReplyTo': True,
                'invitees': [self.maskAreaChairGroup],
                'signatures': [self.maskAreaChairGroup],
                #'params': config.meta_review_params
            },
            'Add_Bid': {
                'tags': True,
                'byPaper': False,
                #'invitees': [config.REVIEWERS],
                #'params': config.add_bid_params
            },
            'Withdraw_Paper': {
                'byPaper': True,
                'invitees': [self.maskAuthorsGroup],
                'byForum': True,
                'reference': True,
                #'params': config.withdraw_paper_params
            }
        }
