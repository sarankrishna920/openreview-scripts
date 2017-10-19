#!/usr/bin/python
import sys, os, shutil
import argparse
import openreview
import ConfigParser
import imp

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--venue', required=True, help = "the full path of the conference group to create.")
parser.add_argument('-d', '--config', help = "a .properties file containing configuration parameters. This script will automatically look for a file called config.properties in the directory specified by the `--venue` argument.")
parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory.")
parser.add_argument('--baseurl')
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
conference_group_id = args.venue
conference_dir = os.path.join(os.path.dirname(__file__), '../../venues/{0}'.format(conference_group_id))

def compile_template(template_path):
    '''
    Generates source code from a template file
    '''
    print "compiling template path: ", template_path
    with open(os.path.join(os.path.dirname(__file__), template_path)) as template:
        template_string = template.read()

    for replacement in config:
        template_string = template_string.replace('<<{0}>>'.format(replacement), config[replacement])

    return template_string

def process_params(params):
    webfield_src = None
    process_src = None

    if 'web_template' in params:
        webfield_src = compile_template(params.pop('web_template'))

    if 'process_template' in params:
        process_src = compile_template(params.pop('process_template'))

    return params, webfield_src, process_src

def parse_properties(file, section):
    config = ConfigParser.RawConfigParser()
    config.read(file)
    return {key.upper(): value for key, value in config.items(section)}


# load config
config_file = args.config if args.config else os.path.join(conference_dir, 'config.properties')
config = parse_properties(config_file, 'config')

# import variables from the conference directory
variables = imp.load_source('variables', os.path.join(conference_dir, 'python', 'variables.py'))

# replace templates with javascript code, then post the groups/invitations
for obj_name, openreview_objects in variables.objects.iteritems():

    if obj_name == 'groups':
        class_type = openreview.Group
        post = client.post_group
    if obj_name == 'invitations':
        class_type = openreview.Invitation
        post = client.post_invitation

    for id, params in openreview_objects.iteritems():

        params, webfield_src, process_src = process_params(params)
        obj = class_type(id, **params)

        if webfield_src:
            obj.web = webfield_src

        if process_src:
            obj.process = process_src

        post(obj)
        print "posted ", obj.id



