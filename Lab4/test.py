import sqlite3

if __name__ == '__main__':
	sql = "SELECT * FROM task"

	conn = sqlite3.connect("task_list.db")
	cursor = conn.cursor()
	cursor.execute(sql)
	
	results = cursor.fetchall()

	for element in results:
		print element[1]

	cursor.close()
	conn.close() 

	
