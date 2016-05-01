from flask import Flask, url_for, redirect, render_template, request, flash
import sqlite3, os
from sys import argv

app = Flask(__name__)


@app.route('/')
def todo_list_manager():
	tasks_list = []
   	sql = "SELECT * FROM task"
	conn = sqlite3.connect("task_list.db")
	cursor = conn.cursor()
	cursor.execute(sql)

	results = cursor.fetchall()

	for element in results:
		tasks_list.append(element)

	cursor.close()
	conn.close()

	return render_template('index.html', tasks = tasks_list)

@app.route('/delete_task/<task>', methods=['POST'])
def delete_task(task):
	sql_delete = "DELETE FROM task WHERE id_task = %s" % task
	conn = sqlite3.connect("task_list.db")
	cursor = conn.cursor()
	cursor.execute(sql_delete)

	conn.commit()
	cursor.close()
	conn.close()

	return redirect(url_for('todo_list_manager'))

@app.route('/add_task', methods = ['POST'])
def add_task():
	# only accepts POST request but this is a step that has to be done
	# when accepting also GET
	if request.method == 'POST':
		# read task name & urgent
		new_task = request.form['taskname']
		new_urgent = 'urg' in request.form
		# insert into sqlite3 db
		sql_add = "INSERT INTO task (todo, urgent) values ('%s', '%s')" % (new_task, new_urgent)
		#print sql_add
		conn = sqlite3.connect("task_list.db")
		cursor = conn.cursor()
		cursor.execute(sql_add)

		conn.commit()
		cursor.close()
		conn.close()
		#flash("You added the task: '%s' with Urgent '%s'" % (new_task, new_urgent))

	return redirect(url_for('todo_list_manager'))



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
