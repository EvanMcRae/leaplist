#leaplist CSV set up

import pandas as pd
import os
from datetime import datetime
import uuid

file_path = "LeapList.csv"

# If the CSV doesn't exist yet, create it with the columns below.

    # Task ID: generated by the program, uses uuid to generate a unique id
    # Task Name: name of the task that shows up in the list
    # Description: can be left blank, otherwise a description or notes of the task when expanded
    # Work Date: this will be the date a task is listed to be worked on
    # Deadline: this will be the date the task is due, ie you could have a task to work on 10/19 but the deadline is 10/22
    # Priority: high, medium, low, we could use this sort the list
    # Status: auto generates as uncompleted, changed to completed when user marks it
    # Creation Time: auto generates the time the task is added to the list
    # Tags: can be left blank, otherwise can be used to sort the list
    # Time to Complete: user must fill this in when checking off a task, although they can set it as 0 hr 0 min.
    #   use this to calculate productivity
    # Completion Time: auto generates the time the task is marked as completed
if not os.path.exists(file_path):
    cols = ["Task ID", "Task Name", "Description", "Work Date", "Deadline", "Priority",
               "Status", "Creation Time", "Tags", "Time to Complete", "Completion Time"]
    pd.DataFrame(columns=cols).to_csv(file_path, index=False)

def new_task(task_name, description, work_date, deadline, priority, tags):

    #generated stuff
    task_ID = str(uuid.uuid4())
    #default status when an item is created, user must mark as complete to change status
    status = "uncompleted"
    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #this only happens if the task is marked as completed
    #leaving them empty for now
    completion_time = ""
    time_to_complete = ""
    timeInput = ""

    #add the new task to the csv
    df = pd.read_csv(file_path)

    new_task = [task_ID, task_name, description, work_date, deadline, priority, status, creation_time, tags, time_to_complete, completion_time]

    if len(df.columns) != len(new_task):
        new_task = [task_ID, task_name, description, work_date, deadline, priority, status, creation_time, tags, time_to_complete, completion_time, timeInput]


    new_row = pd.DataFrame([new_task], columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False)

    print("Task added!")
    return task_ID

def todays_list():
    #this function should load up the csv into the gui and filter to show tasks for todays date
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

def task_completed(task_ID, hours, minutes):
    #the request for hours/minutes has been made mandatory as that is the main point of the productivity to do list
    #the user can obviously leave it as 0 0, so that data vis will need to handle those cases

    df = pd.read_csv(file_path)
    index = df[df["Task ID"] == task_ID].index

    if not index.empty:
        df.loc[index, "Status"] = "completed"
        time_to_complete = f"{int(hours):02}:{int(minutes):02}"
        df.loc[index, 'Time to complete'] = time_to_complete

        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.loc[index, 'Completion Time'] = completion_time

        df.to_csv(file_path, index=False)
        print(f"Task {task_ID} marked as completed with time to complete: {time_to_complete}")
    else:
        print(f"Task ID {task_ID} not found.")


def getProgessPerc():
    df = pd.read_csv(file_path)
    #print(df)
    totalTask = 0
    completeTask = 0
    progressPerc = 0
    for index, row in df.iterrows():
        totalTask += 1
        if row['Status'] == 'completed':
            completeTask += 1
        #print(row['Status'], row['Task ID'])


    if totalTask != 0:
        progressPerc = (completeTask/totalTask)
    return progressPerc


def remove_task(task_ID):
    pass
