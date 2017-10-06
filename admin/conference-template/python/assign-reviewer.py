import argparse
import openreview
import config

def make_anonreviewer_group(anonreviewer_id):

	# copy the reviewer group params. add this group to its own readers list.
	anonreviewer_group_params = {k: v for k,v in config.reviewer_group_params}
	anonreviewer_group_params['readers'].append(anonreviewer_id)

	return openreview.Group(anonreviewer_id, **anonreviewer_group_params)


def get_next_empty_reviewer(client, paper_number):
	lowest_group = None

	# loop through AnonReviewers 1 through 5 and see if they exist.
	# if the AnonReviewer group does exist, and it's empty, that's the lowest
	# reviewer number.
	for reviewer_number in range(1,5):
		try:
			lowest_group = client.get_group('{0}/Paper{1}/AnonReviewer{2}'.format(config.CONFERENCE_ID, paper_number, reviewer_number))
		except openreview.OpenReviewException as e
			if e[0][0]['type'].lower() == 'not found':
				pass
			else:
				raise(e)

		if lowest_group and lowest_group.members == []:
			break

	return lowest_group


# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-u','--user', help = "the id or email of the user", required = True)
parser.add_argument('-p','--paper', help = "the paper number", required = True)
parser.add_argument('-r','--reviewer', help = "the reviewer number", required = False)
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

if args.reviewer_number:
	anonreviewer_id = '{0}/Paper{1}/AnonReviewer{2}'.format(config.CONFERENCE_ID, args.paper, args.reviewer)
else:
	anonreviewer_id = get_next_empty_reviewer(client, args.paper)

anonreviewer_group = make_anonreviewer_group(anonreviewer_id)

anonreviewer_group.members = [args.user]

post_group = raw_input("Assigning {0} to {1}. Post group to <{2}> ? y/[n]: ".format(anonreviewer_group.members, anonreviewer_group.id, client.baseurl))
if post_group.lower() == 'y':
	client.post_group(anonreviewer_group)


