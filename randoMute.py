
## IMPORTS AND LOGGING #########################################################################

import os, random
from sys import exit
from random import choice
from twython import Twython, TwythonError
import logging

logging.basicConfig(filename='twitterWarn.log',level=logging.INFO)

### TWITTER DATA #########################################################################

#yeah i know this should be a config of some kind. But it ain't right now. 

keys = []
with open('keys.txt','r') as my_file:
	keys = my_file.read().splitlines()

APP_KEY = keys[0]
APP_SECRET = keys[1]
OAUTH_TOKEN = keys[2]
OAUTH_TOKEN_SECRET = keys[3]

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### TASK FUNCTIONS  ########################################################################################

def muteUsers():

	## VARIABLES ##################

	followers = []
	silent_followers = []
	next_cursor = -1
	butts_cursor = -1 #lol

	## FLOW CONTROL ##################

	while True:
		username = raw_input("Input your twitter screen name (eg: beckyGoo) > ")
		to_mute = int(raw_input("Enter number of followers to mute > "))

		print "Username: %s" % username
		print "Number of users to mute: %d " % to_mute

		cont = confirm('Confirm these are correct to continue >', resp=True)

		if cont == True:
			break
		else:
			continue

	print "Creating Follower List"

	### GET FOLLOWERS ##################

	while(next_cursor):
		get_followers = twitter.get_followers_list(screen_name=username, count=200, cursor=next_cursor)

		for follower in get_followers["users"]:
			followers.append(follower["screen_name"].encode("utf-8"))
			next_cursor = get_followers["next_cursor"]

	print "%s followers found" % str(len(followers))
	print " "
	print "get muted users"


	## GET LAREADY MUTED FOLLOWERS ##################

	while(butts_cursor):
		get_muted = twitter.list_mutes(screen_name=username, count=200, cursor=butts_cursor)

		for x in get_muted["users"]:
			silent_followers.append(x["screen_name"].encode("utf-8"))
			butts_cursor = get_muted["next_cursor"]
	
	print " "
	print "%s silent_followers found" % str(len(silent_followers))
	print silent_followers

	scrubbed_users = set(followers) - set(silent_followers)

	print " "
	print "%s of scrubbed_users" % str(len(scrubbed_users))
	print scrubbed_users
	print " "

	## CREATE USERS TO MUTE ################## 
	
	users_to_mute = random.sample(set(scrubbed_users), to_mute) #make a new data set out of your old data set
	print "Have gathered %s users to mute." % str(len(users_to_mute)) #print users_to_mute # array
	print users_to_mute
	
	## OPEN OR CREATE A FILE, MUTE, AND WRITE MUTED OUT ##################

	mute_file = open('muted_users.txt', 'a') # open a file to write to

	try:
		for target in users_to_mute:
			
			print "muting %s" % target #you may want to comment this out this if its a large number.
			twitter.create_mute(screen_name=target)
			mute_file.write("%s\n" % target)

	except TwythonError as e:
		logging.info(e)

	print "users muted"
	mute_file.close()
	print "appended users to text file"
	

### TASK FUNCTIONS - UNMUTE ###############################################

def unMuteThem():
	
	filepath = "muted_users.txt"

	if os.path.isfile(filepath):
		
		muted = []

		print "opening saved muted users"

		with open('muted_users.txt','r') as my_file:
			muted = my_file.read().splitlines()
		print muted
		
		os.remove('muted_users.txt')
		print "file deleted"

		try:
			for beep in muted:
				print "unmuting %s" % beep
				twitter.destroy_mute(screen_name=beep)
		except TwythonError as e:
			logging.info(e)
	else:
		print " %s file not found. Go mute some people first!" % filepath
    	

### FLOW CONTROL ###############################################

def confirm(prompt=None, resp=False):
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s] | %s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s] | %s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False



### PROGRAM LOOP-DE-LOOP ###############################################

while True:

	### MENU #######################
	print " "
	print "-"*20
	print "RANDO TWITTER MUTER"
	print "-"*20
	print "1. mute random users"
	print "2. unmute users"
	print "3. exit"
	print "-"*20
	print " "

	### USER TASK SELECTION ############

	command = int(raw_input("choose a menu item: [1-3] > "))

	if command == 1:
		print "1"
		muteUsers()

	elif command == 2:
		print "2"
		unMuteThem()

	elif command == 3:
		print "Quitting"
		exit(1)
	else:
		print "Not a valid entry"