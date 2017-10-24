#!/usr/bin/python
import sys, os, shutil
import argparse
import openreview
import ConfigParser

from variables import parse_properties

def select_templates(templates_dir):
    # given some options, returns template file paths with the format /conference-template/<file>
    # e.g. returns ['process/comment.process', 'process/review.process']

    # TODO: Make this function select particular files based on the input configuration

    templates = []

    template_path = '../conference-template'
    subdirectories = [d for d in os.listdir(template_path) if os.path.isdir(os.path.join(template_path, d))]
    for subdir in subdirectories:
        for file in os.listdir(os.path.join(template_path, subdir)):
            if file.endswith((".process", ".webfield", ".py")):
                templates.append(os.path.join(subdir, file))
    return templates

def build_directories(paths, templates_dir, conference_dir):
    # create the subdirectories if they don't exist
    for subpath in paths:
        path = os.path.join(conference_dir, subpath)
        if not os.path.exists(path):
            print "Creating directory {0}".format(os.path.join(conference_dir, path))
            os.makedirs(path)

    # get and copy the files from the conference template
    templates = select_templates(templates_dir)
    for template_file in templates:
        shutil.copyfile(os.path.join(templates_dir, template_file), os.path.join(conference_dir, template_file))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help = "a .properties file containing configuration parameters. This script will automatically look for a file called config.properties in the directory specified by the `--venue` argument.")
    parser.add_argument('--overwrite', action='store_true', help="if true, overwrites the conference directory.")
    parser.add_argument('--baseurl')
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    conference_dir = os.path.dirname(args.config)

    # load config
    config_file = args.config
    config = parse_properties(config_file, 'config')
    options = parse_properties(config_file, 'options')

    subdirectories = [
        'webfield',
        'process',
    ]

    templates_dir = '../conference-template'

    # build the directory structure
    build_directories(subdirectories, templates_dir, conference_dir)

if __name__ == '__main__':
    main()
