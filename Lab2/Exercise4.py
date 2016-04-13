from sys import argv

def task_priority():

	dict = [{'todo':'call John for AmI project organization', 'urgent': True}, 
	{'todo':'by a new mouse', 'urgent': True}, 
	{'todo':"find a present for Angela's birthday", 'urgent': False},
	{'todo':'organize mega party (last week of April)', 'urgent': False},
	{'todo':'book summer holidays', 'urgent': False}, 
	{'todo':'whatsapp Mary for a coffee', 'urgent': True}]

	for task in dict:
		if task["urgent"]:
			print "Urgent tasks: \new%s" % task
		else:
			print "Non urgent tasks: \n%s" % task

	
	
	
	
	

	# return only the urgent tasks


	

if __name__ == '__main__':
	task_priority()
