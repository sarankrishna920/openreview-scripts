import argparse
import openreview
import config

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('id', help = "the note ID of the assignment")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

assignment_note = client.get_note(args.id)

def next_anonreviewer_id(empty_anonreviewer_groups, anonreviewer_groups):
    if len(empty_anonreviewer_groups) > 0:
        anonreviewer_group = empty_anonreviewer_groups[0]
        empty_anonreviewer_groups.remove(anonreviewer_group)
        return anonreviewer_group.id
    else:
        anonreviewer_group_ids = [g.id for g in anonreviewer_groups]

        # reverse=True lets us get the AnonReviewer group with the highest index
        highest_anonreviewer_id = sorted(anonreviewer_group_ids, reverse=True)[0]

        # find the number of the highest anonreviewer group
        highest_anonreviewer_index = highest_anonreviewer_id[-1]
        return 'ICLR.cc/2018/Conference/Paper{0}/AnonReviewer{1}'.format(paper_number, int(highest_anonreviewer_index)+1)


for paper_number, assignment in assignment_note.content['assignments'].iteritems():
    anonreviewer_groups = client.get_groups(id = 'ICLR.cc/2018/Conference/Paper{0}/AnonReviewer.*'.format(paper_number))
    empty_anonreviewer_groups = sorted([ a for a in anonreviewer_groups if a.members == [] ], key=lambda x: x.id)
    anonreviewer_groups = client.get_groups(id = 'ICLR.cc/2018/Conference/Paper{0}/AnonReviewer.*'.format(paper_number))

    paper_reviewer_group = client.get_group('{0}/{1}/Reviewers'.format(config.CONF, paper_number))

    for reviewer in assignment['assigned']:
        anonymous_reviewer_group = next_anonreviewer_id(empty_anonreviewer_groups, anonreviewer_groups)
        print "assigning reviewer {0} to {1}".format(reviewer, anonymous_reviewer_group.id)
        client.remove_members_from_group(anonymous_reviewer_group, anonymous_reviewer_group.members)
        client.add_members_to_group(anonymous_reviewer_group, reviewer)
        client.add_members_to_group(paper_reviewer_group, reviewer)

