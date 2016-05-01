
def todo_manager():
	while True:
		print "1. insert new task\n2. remove a task\n3. show all existing tasks\n4. close the program\n"
		option = int(raw_input("Your choice: "))
		if option == 1:		# insert a new task
			print "Good"
		elif option == 2:	# remove a task
			print "Do something"
		elif option == 3:	# show all tasks
			print "Do other something"
		elif option == 4:	# close program
			print "Closing application..."
			break

if __name__ == '__main__':
	todo_manager()