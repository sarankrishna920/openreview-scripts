#!/usr/bin/python
import sys, os
import ConfigParser

def parse_properties(file, section):
    config = ConfigParser.RawConfigParser()
    config.read(file)
    return {key.upper(): value for key, value in config.items(section)}

class Variables:


    def build_groups(self, config, options):
        groups = {}

        initial = {}
        by_paper = {}

        initial[self.conference_id] = {
            'readers': ['everyone'],
            'writers': [self.conference_id],
            'signatories': [self.conference_id],
            'web_template': os.path.join(self.conference_dir, 'webfield/conference.webfield'),
        }

        initial[self.programchairs_id] = {
            'readers': [self.conference_id, self.programchairs_id],
            'writers': [self.conference_id],
            'signatories': [self.conference_id, self.programchairs_id],
            'signatures': [self.conference_id],
            'web_template': os.path.join(self.conference_dir, 'webfield/programchair.webfield'),
        }

        initial[self.reviewers_id] = {
            'readers': [self.conference_id],
            'writers': [self.conference_id],
            'signatories': [self.conference_id],
            'signatures': [self.conference_id]
        }

        if eval(options['AC_ENABLED']):
            initial[config['AREA_CHAIRS']] = {
                'readers': [self.conference_id, self.programchairs_id, self.areachairs_id],
                'writers': [self.conference_id],
                'signatories': [self.conference_id, self.areachairs_id],
                'signatures': [self.conference_id],
                'web_template': os.path.join(conference_dir, 'webfield/areachair.webfield'),
            }

            by_paper[self.maskAreaChairGroup] = {
                'byPaper': True,
                'params': {
                    'readers': [self.conference_id, self.programchairs_id, self.maskAreaChairGroup],
                    'writers': [self.conference_id],
                    'signatories': [self.maskAreaChairGroup, self.conference_id],
                    'signatures': [self.conference_id],
                }
            }

        if eval(options['BLINDNESS']) == 2:
            by_paper[self.maskAuthorsGroup] = {
                'byPaper': True,
                'params': {
                    'readers': [self.conference_id, self.programchairs_id],
                    'writers': [self.conference_id],
                    'signatories': [self.maskAuthorsGroup, self.conference_id],
                    'signatures': [self.conference_id],
                }
            }

        by_paper[self.maskReviewersGroup] = {
            'byPaper': True,
            'params': {
                'readers': [self.conference_id, self.programchairs_id, self.areachairs_id],
                'writers': [self.conference_id],
                'signatories': [self.conference_id],
                'signatures': [self.conference_id],
            }
        }

        by_paper[self.maskAnonReviewerGroup] = {
            'byPaper': True,
            'params': {
                'readers': [self.conference_id, self.programchairs_id, self.areachairs_id, self.maskAnonReviewerGroup],
                'nonreaders': [self.maskReviewersNonreadersGroup],
                'writers': [self.conference_id],
                'signatories': [self.maskAnonReviewerGroup, self.conference_id],
                'signatures': [self.conference_id],
            }
        }

        groups = {'initial': initial, 'by_paper': by_paper}

        return groups

    def build_invitations(self, config, options):
        initial = {}
        by_paper = {}

        '''
        Invitations that can be created before papers are submitted;
        they aren't unique by paper.
        '''

        submission_reply = {
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

        submission_params = {
            'readers': ['everyone'],
            'writers': [self.conference_id],
            'invitees': ['~'],
            'signatures': [self.conference_id],
            'process_template': os.path.join(self.conference_dir, 'process/submission.process'),
            'duedate': self.submission_timestamp,
            'reply': submission_reply
        }

        blindsubmission_params = {
            'readers': ['everyone'],
            'writers': [self.conference_id],
            'invitees': [self.conference_id],
            'signatures': [self.conference_id],
            'duedate': self.submission_timestamp,
            'reply': submission_reply
        }

        initial[self.submission_id] = submission_params

        publiccomment_params = {
            'readers': ['everyone'],
            'writers': [self.conference_id],
            'invitees': ['~'],
            'signatures': [self.conference_id],
            'process_template': os.path.join(self.conference_dir, 'process/comment.process'),
            'reply': {
                'forum': None,
                'replyto': None,
                'invitation': self.submission_id,
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
        }

        initial[self.publiccomment_id] = publiccomment_params
        by_paper[self.publiccomment_name] = {
            'byPaper': False,
            'byForum': False,
            'invitees': ['~'],
            'noninvitees': [self.maskAuthorsGroup, self.maskReviewersGroup, self.maskAreaChairGroup],
            'params': initial.pop(self.publiccomment_id),
        }

        review_params = {
            'readers': ['everyone'],
            'writers': [self.conference_id],
            'signatures': [self.conference_id],
            'process_template': os.path.join(self.conference_dir, 'process/officialReview.process'),
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

        initial[self.review_id] = review_params


        '''
        Invitations that must be created on a per-paper basis.
        '''

        revision_params = {
            'readers': submission_params['readers'],
            'writers': submission_params['writers'],
            'invitees': [], # set during submission process function; replaced in invitations.py
            'signatures': submission_params['signatures'],
            'reply': {
                'forum': None,
                'referent': None,
                'signatures': submission_params['reply']['signatures'],
                'writers': submission_params['reply']['writers'],
                'readers': submission_params['reply']['readers'],
                'content': submission_params['reply']['content']
            }
        }

        by_paper['Add_Revision']= {
            'byPaper': True,
            'invitees': [self.maskAuthorsGroup],
            'byForum': True,
            'reference': True,
            'params': revision_params,
        }


        '''
        Modifications based on "blindness"
        '''

        if eval(options['BLINDNESS']) == 1 or eval(options['BLINDNESS']) == 2:

            by_paper[self.publiccomment_name] = {
                'byPaper': True,
                'byForum': True,
                'invitees': ['~'],
                'noninvitees': [self.maskAuthorsGroup, self.maskReviewersGroup, self.maskAreaChairGroup],
                'params': initial.pop(self.publiccomment_id),
            }

            official_comment_params = {
                'readers': ['everyone'],
                'writers': [self.conference_id],
                'invitees': [],
                'signatures': [self.conference_id],
                'process_template': os.path.join(self.conference_dir, 'process/comment.process'),
                'reply': {
                    'forum': None,
                    'replyto': None,
                    'readers': {
                        'description': 'The users who will be allowed to read the above content.',
                        'values': ['everyone']
                    },
                    'signatures': {
                        'description': 'How your identity will be displayed with the above content.',
                        'values-regex': ''
                    },
                    'writers': {
                        'values-regex': ''
                    },
                    'content':{
                        'title': {
                            'order': 0,
                            'value-regex': '.{1,500}',
                            'description': 'Brief summary of your comment.',
                            'required': True
                        },
                        'comment': {
                            'order': 1,
                            'value-regex': '[\\S\\s]{1,5000}',
                            'description': 'Your comment or reply.',
                            'required': True
                        }
                    }
                }
            }

            by_paper[self.officialcomment_name] = {
                'byPaper': True,
                'byForum': True,
                'invitees': [self.maskReviewersGroup, self.maskAreaChairGroup, self.programchairs_id],
                'signatures': [self.maskAnonReviewerGroup, self.maskAreaChairGroup, self.programchairs_id],
                'params': official_comment_params
            }

            by_paper[self.review_name] = {
                'byPaper': True,
                'invitees': [self.maskReviewersGroup],
                'signatures': [self.maskAnonReviewerGroup],
                'byForum': True,
                'byReplyTo': True,
                'params': initial.pop(self.review_id)
            }

        if eval(options['BLINDNESS']) == 2:
            initial[self.submission_id]['process_template'] = os.path.join(self.conference_dir, 'process/submission-blind.process')
            initial[self.conference_id]['web_template'] = os.path.join(self.conference_dir, 'webfield/conference-blind-tabs.webfield')
            by_paper[self.officialcomment_name]['invitees'].append(self.maskAuthorsGroup)
            by_paper[self.officialcomment_name]['signatures'].append(self.maskAuthorsGroup)

        '''
        Modifications based on AC_ENABLED
        '''
        if eval(options['AC_ENABLED']):
            meta_review_params = {
                'readers': ['everyone'],
                'writers': [self.conference_id],
                'invitees': [],
                'signatures': [self.conference_id],
                'process': os.path.join(os.path.dirname(__file__), '../process/metaReview.process'),
                'duedate': 1517270399000, # 23:59:59 EST on January 1, 2018
                'reply': {
                    'forum': None,
                    'replyto': None,
                    'writers': {
                        'values-regex': self.conference_id + '.*'
                    },
                    'signatures': {
                        'values-regex': self.conference_id + '.*'
                    },
                    'readers': {
                        'values': [self.areachairs_id, self.programchairs_id],
                        'description': 'The users who will be allowed to read the above content.'
                    },
                    'content': {
                        'title': {
                            'order': 1,
                            'value-regex': '.{1,500}',
                            'description': 'Brief summary of your review.',
                            'required': True
                        },
                        'metareview': {
                            'order': 2,
                            'value-regex': '[\\S\\s]{1,5000}',
                            'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
                            'required': True
                        },
                        'recommendation': {
                            'order': 3,
                            'value-dropdown': [
                                'Accept (Oral)',
                                'Accept (Poster)',
                                'Reject',
                                'Invite to Workshop Track'
                            ],
                            'required': True
                        },
                        'confidence': {
                            'order': 4,
                            'value-radio': [
                                '5: The area chair is absolutely certain',
                                '4: The area chair is confident but not absolutely certain',
                                '3: The area chair is somewhat confident',
                                '2: The area chair is not sure',
                                '1: The area chair\'s evaluation is an educated guess'
                            ],
                            'required': True
                        }
                    }
                }
            }

            by_paper['Meta_Review'] =  {
                    'byPaper': True,
                    'byForum': True,
                    'byReplyTo': True,
                    'invitees': [self.maskAreaChairGroup],
                    'signatures': [self.maskAreaChairGroup],
                    'params': meta_review_params
            }

        '''
        Add Bids
        '''
        if eval(options['BIDS_ENABLED']):
            by_paper['Add_Bid'] = {
                'tags': True,
                'byPaper': False,
                'invitees': [self.reviewers_id],
                #'params': config.add_bid_params
            }


        invitations = {
            'initial': initial,
            'by_paper': by_paper,
        }

        return invitations



    def init(self, conference_dir):

        # load config
        config_file = os.path.join(conference_dir, 'config.properties')
        config = parse_properties(config_file, 'config')
        options = parse_properties(config_file, 'options')

        self.conference_dir = conference_dir
        self.conference_id = config['CONFERENCE_ID']

        #self.audience = eval(config['AUDIENCE'])

        self.programchairs_name = 'Program_Chairs'
        self.programchairs_id = os.path.join(self.conference_id, self.programchairs_name)

        self.areachairs_name = 'Area_Chairs'
        self.areachairs_id = os.path.join(self.conference_id, self.areachairs_name)

        self.reviewers_name = 'Reviewers'
        self.reviewers_id = os.path.join(self.conference_id, self.reviewers_name)

        self.submission_timestamp = config['SUBMISSION_TIMESTAMP']
        self.review_timestamp = config['REVIEW_TIMESTAMP']

        self.submission_name = config['SUBMISSION_NAME']
        self.submission_id = os.path.join(self.conference_id, '-', self.submission_name)

        self.blindsubmission_name = config['BLIND_SUBMISSION_NAME']
        self.blindsubmission_id = os.path.join(self.conference_id, '-', self.blindsubmission_name)

        self.publiccomment_name = config['PUBLIC_COMMENT_NAME']
        self.publiccomment_id = os.path.join(self.conference_id, '-', self.publiccomment_name)

        self.officialcomment_name = config['OFFICIAL_COMMENT_NAME']
        self.officialcomment_id = os.path.join(self.conference_id, '-', self.officialcomment_name)

        self.review_name = 'Review'
        self.review_id = os.path.join(self.conference_id, '-', self.review_name)

        # todo: change these to snake case to match style everywhere else
        self.maskAuthorsGroup = os.path.join(self.conference_id, "Paper[PAPER_NUMBER]/Authors")
        self.maskReviewersGroup = os.path.join(self.conference_id, "Paper[PAPER_NUMBER]/Reviewers")
        self.maskAreaChairGroup = os.path.join(self.conference_id, "Paper[PAPER_NUMBER]/Area_Chair")
        self.maskAnonReviewerGroup = os.path.join(self.conference_id, "Paper[PAPER_NUMBER]/AnonReviewer[0-9]+")
        self.maskReviewersNonreadersGroup = os.path.join(self.conference_id, "Paper[PAPER_NUMBER]/Reviewers/Nonreaders")

        self.groups = self.build_groups(config, options)
        self.invitations = self.build_invitations(config, options)


