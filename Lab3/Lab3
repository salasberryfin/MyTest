import twitter
import os

list_tasks = []
filename = 'task_list.txt'
# open the file for appending
txt = open(filename, "rw+")
#print "File text: %s" % filename
# store content of the file on a list of tasks
for line in txt:
	list_tasks.append(line)

# insert a new task
def insert_new(list_tasks):
	new_task = raw_input("Insert task name: ")
	list_tasks.append(new_task)
	txt.write("\n" + new_task)


# remove task
def remove_task(list_tasks):
	str_rm = raw_input("Write the contained string of the task you want to delete: ")
	for task in list_tasks:
		if str_rm in task:
			list_tasks.remove(task)
			# clean file
			txt.seek(0)	# cursor on position 0
			txt.truncate()
			for n in list_tasks:
				# rewrite the updated task list
				txt.write(n)
			print "Task/s was/were removed\n"
	print "The string you entered is not part of any task!\n"


# read tasks
def voice_tasks(list_tasks):
	# read tasks alphabetically ordered
	#for task in sorted(list_tasks):
	os.system('wget -q -U Mozilla -O test.mp3 "http://api.voicerss.org/?key=372c6bee13824fad884ed65442e123bd&hl=en-us&src=hello"')
	# play it (system dependent)
    # parameters for mplayer (used to remove unwanted messages):
    #  -quiet
    #    Make console output less verbose; in particular, prevents the status line (i.e. A: 0.7 V: 0.6 A-V: 0.068 ...) from being displayed
    #  -nolirc
    #    Turns off LIRC support.
    #  -msglevel <all=<livello>:<modulo>=<livello>:...>
    #    Control verbosity directly for each module
	os.system("mplayer -quiet -nolirc -msglevel all=-1 test.mp3")


# twitter mentions
def twitter_mentions(list_tasks):
	# from my created app 'CsToDoList'
	api = twitter.Api(consumer_key = '2FfCs3COs4GwaccX6kqrBuHa0',
		consumer_secret = 'aq7pl3085OXY2twDO5mSaYzQZk3CDXgn45mt1dhfSYpwITXjCS',
		access_token_key = '364827409-XiHcNJNElSqeQLUCzQnHt0qHhUCe80d7bNMWZUQL',
		access_token_secret = 'VWfcQFESQrO3MA4MpbBFVOIBvAJT3p1Bu5eceqL6zEsD3')

	# verify if credentials are successful
	#print(api.VerifyCredentials())
	# print tweets from specified user
	#statuses = api.GetUserTimeline(screen_name='salasberryfin')
	#print([s.text for s in statuses])

	# checking for mentions containing the str_task string
	str_task = "#Manada"
	mentions = api.GetMentions()
	for mention in mentions:
		if str_task in mention.text:
			print mention.text



# manager method
def todo_manager():
	#print the content of the file (alphabetical order)
	#print sorted(list_tasks)

	while True:
		print "\nWelcome!\n\n1. insert new task\n2. remove a task\n3. show all existing tasks (alphabetical order)\n4. read the first two tasks\n5. add Twitter mentions\n6. close the program\n"
		option = int(raw_input("Your choice: "))
		if option == 1:		# insert a new task
			insert_new(list_tasks)

		elif option == 2:	# remove a task
			remove_task(list_tasks)

		elif option == 3:	# show all tasks
			for task in sorted(list_tasks):
				print task

		elif option == 4:	# read the list of tasks
			voice_tasks(list_tasks)

		elif option == 5:	# add twitter mentions to the to do list
			twitter_mentions(list_tasks)

		elif option == 6:	# close program
			print "Closing application..."
			break

	# close the file
	txt.closed

if __name__ == '__main__':
	todo_manager()
