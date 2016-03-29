from sys import argv

def todo_manager():

	list_tasks = []
	filename = 'task_list.txt'
	# open the file for appending
	txt = open(filename, "rw+")
	#print "File text: %s" % filename

	# store content of the file on a list of tasks
	for line in txt:
		list_tasks.append(line)

	# print the content of the file (alphabetical order)
	#print sorted(list_tasks)

	while True:
		print "\nWelcome!\n\n1. insert new task\n2. remove a task\n3. show all existing tasks (alphabetical order)\n4. close the program\n"
		option = int(raw_input("Your choice: "))
		if option == 1:		# insert a new task
			new_task = raw_input("Insert task name: ")
			list_tasks.append(new_task)
			txt.write("\n" + new_task)
		elif option == 2:	# remove a task
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
		elif option == 3:	# show all tasks
			for task in sorted(list_tasks):
				print task
		elif option == 4:	# close program
			print "Closing application..."
			break

	# close the file
	txt.closed

if __name__ == '__main__':
	todo_manager()
