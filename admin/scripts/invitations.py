#!/usr/bin/python

import sys, os, shutil
import argparse
import openreview
import ConfigParser
import pprint
import re

from compile import process_params
from variables import Variables
from variables import parse_properties

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', required=True, help = "config.properties file.")
parser.add_argument('-i', '--invitations', nargs='*')
parser.add_argument('--enable', action='store_true', help="if present, enables the given invitation")
parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

# load config
config_file = args.config
conference_dir = os.path.dirname(args.config)
print 'config_file', config_file
config = parse_properties(config_file, 'config')

# initialize variables
variables = Variables()
variables.init(conference_dir)

invitation_configurations = variables.invitations['by_paper']

if args.invitations == ['all']:
    invitations_to_process = invitation_configurations.keys()
else:
    invitations_to_process = args.invitations

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

pp = pprint.PrettyPrinter(indent=4)


papers = client.get_notes(invitation = variables.submission_id)

def get_or_create_invitations(invitationId, overwrite):
    invitation_config = invitation_configurations[invitationId]
    if invitation_config['byPaper']:

        invitations = client.get_invitations(regex = config['CONFERENCE_ID'] + '/-/Paper.*/' + invitationId, tags = invitation_config.get('tags'))
        if invitations and len(invitations) == len(papers) and not overwrite:
            # TODO: why is this here? why not just return invitations?
            return [i for i in invitations if re.match(config['CONFERENCE_ID'] + '/-/Paper[0-9]+/' + invitationId, i.id)]
        else:
            invitations = []
            for n in papers:

                params, webfield_src, process_src = process_params(invitation_config['params'], config)
                new_invitation = openreview.Invitation(config['CONFERENCE_ID'] + '/-/Paper{0}/'.format(n.number) + invitationId, **params)

                if webfield_src:
                    new_invitation.web = webfield_src
                if process_src:
                    new_invitation.process = process_src

                if 'byForum' in invitation_config and invitation_config['byForum']:
                    new_invitation.reply['forum'] = n.forum

                if 'reference' in invitation_config and invitation_config['reference']:
                    new_invitation.reply['referent'] = n.forum

                if 'byReplyTo' in invitation_config and invitation_config['byReplyTo']:
                    new_invitation.reply['replyto'] = n.forum

                if 'signatures' in invitation_config:
                    new_invitation.reply['signatures']['values-regex'] = prepare_regex(new_invitation.id, invitation_config['signatures'])
                    new_invitation.reply['writers']['values-regex'] = prepare_regex(new_invitation.id, invitation_config['signatures'])

                invitations.append(client.post_invitation(new_invitation))
            return invitations
    else:
        try:
            invitation = client.get_invitation(config['CONFERENCE_ID'] + '/-/' + invitationId)
            invitation_exists = True
        except openreview.OpenReviewException as error:
            if error[0][0]['type'].lower() == 'not found':
                invitation_exists = False
            else:
                raise error

        if invitation_exists and not overwrite:
            return [invitation]
        else:
            new_invitation = openreview.Invitation(config['CONFERENCE_ID'] + '/-/' + invitationId, **invitation_config['params'])
            return [client.post_invitation(new_invitation)]

def prepare_invitees(invitationId, invitees):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        return [ invitee.replace('[PAPER_NUMBER]', match.group(1)) for invitee in invitees]
    else:
        return invitees

def prepare_regex(invitationId, members):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        return '|'.join([ member.replace('[PAPER_NUMBER]', match.group(1)) for member in members])
    else:
        return members

for invitationId in invitations_to_process:
    print "processing invitation ", invitationId
    if invitationId in invitation_configurations:
        if args.enable or args.disable:
            enable = args.enable and not args.disable

            invitations = get_or_create_invitations(invitationId, args.overwrite)
            updated = 0

            if invitations:
                for i in invitations:

                    i.invitees = prepare_invitees(i.id, invitation_configurations[invitationId]['invitees']) if enable else []
                    if 'noninvitees' in invitation_configurations[invitationId]:
                        i.noninvitees = prepare_invitees(i.id, invitation_configurations[invitationId]['noninvitees'])
                    result = client.post_invitation(i)

                    pp.pprint({'Invitation ID ..': result.id, 'Invitees .......': i.invitees})
                    print '\n'
                    updated += 1
            else:
                print "Invitation not found: ", invitationId

            print "# Invitations updated: ", updated

        else:
            print "Invalid enable value: ", args.enable

    else:
        print "Invalid invitation: ", invitationId

    print '\n'




