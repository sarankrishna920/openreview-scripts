#!/usr/bin/python

'''
Assigns group membership (and creates groups when they don't exist).
'''
import sys, os
import argparse
import openreview
from variables import Variables
from variables import parse_properties

def validate_args(args):
    if (args.paper and args.file):
        print "--file and --paper parameters are mutually exclusive. Please choose one or the other."
        sys.exit()

    if not (args.areachairs or args.reviewers):
        print "you must pass in at least one value for either --areachairs or --reviewers (you may also pass in values for both)."
        sys.exit()

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, help = "config.properties file.")
    parser.add_argument('-f', '--file')
    parser.add_argument('-p', '--paper')
    parser.add_argument('-a', '--areachairs', nargs='*')
    parser.add_argument('-r', '--reviewers', nargs='*')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--baseurl')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    args_valid = validate_args(args)

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    # load config
    config_file = args.config
    conference_dir = os.path.dirname(args.config)
    print 'config_file', config_file
    config = parse_properties(config_file, 'config')

    # initialize variables
    variables = Variables()
    variables.init(conference_dir)




papers = client.get_notes(invitation = variables.submission_id)

def prepare_parameters(params_mask, number):
    new_params = {k:v for k,v in params_mask.iteritems()}
    for p in ['readers', 'nonreaders', 'writers', 'signatures', 'signatories', 'members']:
        if p in new_params:
            new_params[p] = [r.replace('[PAPER_NUMBER]', str(number)).replace('[0-9]+', str(n.number)) for r in new_params[p]]
    return new_params

def get_or_create_group(group_mask, params_mask, number):
    new_group_id = group_mask.replace('[PAPER_NUMBER]', str(n.number)).replace('[0-9]+', str(n.number))
    new_params = prepare_parameters(params_mask, number)
    new_group = openreview.Group(new_group_id, **new_params)

    if not args.overwrite:
        try:
            new_group = client.get_group(new_group_id)
        except openreview.OpenReviewException:
            pass

    return new_group

for group_mask, group_settings in variables.groups['by_paper'].iteritems():
    params_mask = group_settings['params']
    for n in papers:
        new_group = get_or_create_group(group_mask, params_mask, n.number)
        print "processing", new_group.id
        client.post_group(new_group)

