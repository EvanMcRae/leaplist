#leaplist CSV set up

import pandas as pd
import os
from datetime import datetime
import uuid

#prob want these later
import numpy as np
import matplotlib as plt


file_path = "LeapList.csv"

# If the CSV doesn't exist yet, create it with the columns below.
# I added more columns than necessary for future items, they can be removed if needed.
# We might want to change up the order of the columns too for readability on the CSV

    # Task ID: generated by the program, uses uuid to generate a unique id
    # Task Name: name of the task that shows up in the list
    # Description: can be left blank, otherwise a description or notes of the task when expanded
    # Work Date: this will be the date a task is listed to be worked on
    # Deadline: this will be the date the task is due, ie you could have a task to work on 10/19 but the deadline is 10/22
    # Priority: high, medium, low, we could use this sort the list
    # Status: auto generates as uncompleted, can be changed to completed when user marks it
    # Creation Time: auto generates the time the task is added to the list
    # Tags: can be left blank, otherwise can be used to sort the list
    # Time to Complete: can be left blank, otherwise it would be the estimated time that was needed to complete the task
    # Completion Time: auto generates the time the task is marked as completed
if not os.path.exists(file_path):
    cols = ["Task ID", "Task Name", "Description", "Work Date", "Deadline", "Priority",
               "Status", "Creation Time", "Tags", "Time to Complete", "Completion Time"]
    pd.DataFrame(columns=cols).to_csv(file_path, index=False)

def new_task(task_name, description, work_date, deadline, priority, tags):
    #after doing this, i realized we will have to have a way to edit each aspect of the task after initally putting it in
    #since optional items might get filled in later


    # required, user input can be anything
    #task_name = input("Enter the name of the task: ")
    # optional, user input can be anything
    #description = input("Enter the description of the task (optional): ")
    # optional, but if no input specifed, should default to current date
    #also need to figure out how to make sure the date is in the correct format
    #in my to do list app there's a mini calendar users select from
    #work_date = input("Enter the date you plan to work on the task (YYYY-MM-DD)(optional): ")
    #optional, my to do list app leaves it blank if not specified
    #also need to figure out how to make sure the date is in the correct format in GUI, maybe use caldendar selection
    #deadline = input("Enter the deadline for the task (YYYY-MM-DD)(optional): ")
    #optional, leave blank if not selected, otherwise ensure user can only select those options
    # maybe use a dropdown menu for these 3 options when selecting in the GUI
    #priority = input("Enter the priority of the task (high, medium, low)(optional): ")
    #optional, leave blank if not selected
    #if other tags exist it would be nice to have a dropdown list of those tags
    #tags = input("Enter any tags for the task (optional): ")


    #generated stuff
    task_ID = str(uuid.uuid4())
    #default status when an item is created, user must mark as complete to change status
    status = "uncompleted"
    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #this only happens if the task is marked as completed
    #leaving them empty for now
    completion_time = ""
    time_to_complete = ""

    #add the new task to the csv
    df = pd.read_csv(file_path)
    new_task = [task_ID, task_name, description, work_date, deadline, priority, status, creation_time, tags, time_to_complete, completion_time]
    new_row = pd.DataFrame([new_task], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False)

    print("Task added!")

def todays_list():
    #this function should load up the csv into the gui and filter to show tasks for todays date
    #we will need other functions to handle more filters and ways of viewing, but I think this is a good default
    df = pd.read_csv(file_path)
    #get the current date
    curr_date = datetime.now().strftime("%Y-%m-%d")
    #look for any tasks that are uncompleted and have the curr date
    todays_tasks = df[(df["Work Date"] == curr_date) & (df["Status"] == "uncompleted")]
    # no tasks found
    if todays_tasks.empty:
        print("Nothing to do")
    #currently just printing out the name of the tasks found
    else:
        for task_name in todays_tasks["Task Name"]:
            print(task_name)

def task_completed():
    #this function should allow the user to mark a task as completed
    #it should also ask for the time it took to complete the task in hrs /mins

    # optional, leave blank if not selected
    # the data vis will have to look at this column and if blank, exclude from the graph
    # will probably want to accept hours and mins
    # this is also asked for after a task is marked complete
    time_to_complete = input("Enter the time it took to complete the task(optional): ")
    #generated when item is marked as complete by the user
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pass

#testing and putting in several tasks
#def menu():
    #show_menu = True
    #while show_menu:
        #print("1. Add a task")
        #print("2. See today's tasks")
        #print("3. Exit")

        #choice = input("Enter your choice: ")
        #if choice == "1":
            #new_task()
        #elif choice == "2":
            #todays_list()
        #elif choice == "3":
            #show_menu = False
        #else:
            #print("Invalid")

#if __name__ == "__main__":
    #menu()