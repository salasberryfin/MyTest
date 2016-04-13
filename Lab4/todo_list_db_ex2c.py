'''
Created on Apr 04, 2016
Copyright (c) 2015-2016 Teodoro Montanaro

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
@author: tmontanaro
'''


# this script is an extension of the script todo_list_db_ex2b.py


from sys import argv
import os
import db_interaction


def new_task():
    '''
    Add a new element to the list of tasks in db
    '''

    # ask the user to insert the task she wants to add
    string = raw_input("Type the new task:\n>")

    urgent = -1
    # ask user to specify if the just inserted task is urgent or not
    # we continue to ask it until she inserts Y or N
    while (urgent == -1):
        urgent_string = raw_input("Is this task urgent (Y/N)?\n>")
        if len(urgent_string) == 1:
            if urgent_string.upper() == "Y" :
                urgent = 1
            elif urgent_string.upper() == "N":
                urgent = 0

    #insert the task in the db
    db_interaction.db_insert_task(string, urgent)

    print "The new task was successfully added to the list"

def remove_multiple_tasks():
    '''
    Remove all the elements that contain a provided string
    '''

    # ask for the substring
    substring = raw_input("Type the substring you want to use to remove all tasks that contain it:\n>")

    #remove from db
    db_interaction.db_remove_task(substring)


def print_sorted_list():
    '''
    Print the elements of the list, sorted in alphabetic order
    '''

    #get the list of tasks from the database
    tasks_list = db_interaction.get_sorted_tasks_list()

    print tasks_list


if __name__ == '__main__':
    # main program

    # set a variable to False: it will be used to re-execute the program multiple times
    ended = False

    # keep asking strings until the user types 4 (to exit)
    while not ended:

        # print the menu every time we finish to perform an operation
        print "Insert the number corresponding to the action you want to perform"
        print "1: insert a new task"
        print "2: show all existing tasks sorted in alphabetic order"
        print "3: remove all the existing tasks that contain a provided string;"
        print "4: close the program"

        # get the action as input
        string = raw_input("Your choice:\n>")

        # check if the inserted string is actually a number
        # we will ask the user a new input until it will insert a number
        while string.isdigit() != True:
            # if the string is not a number we will ask a new input
            string = raw_input("Wrong input! Your choice:\n>")

        # convert the string to int (integer number)
        choice = int(string)

        # depending on the chosen input we perform the right action
        if (choice == 1):  # insert a new task
            tasks_list = new_task()
        elif (choice == 2):  # show the list of tasks
            print_sorted_list()
        elif (choice == 3):  # remove a task
            tasks_list = remove_multiple_tasks()
        elif (choice == 4):  # exit
            ended = True
