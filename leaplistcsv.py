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
               "Status", "Creation Time", "Tags", "Completion Time"]
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

    #add the new task to the csv
    df = pd.read_csv(file_path)

    new_task = [task_ID, task_name, description, work_date, deadline, priority, status, creation_time, tags, completion_time]

    #commenting out for now, I think I had a spelling error causing and extra column to be added
    #why can add it back in if the error persists

    print("DataFrame columns:", df.columns)
    print("New task data:", new_task)

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
        df.loc[index, "Time Input"] = time_to_complete

        completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.loc[index, 'Completion Time'] = completion_time

        df.to_csv(file_path, index=False)
        print(f"Task {task_ID} marked as completed with time to complete: {time_to_complete}")
    else:
        print(f"Task ID {task_ID} not found.")

def uncomplete_task(task_ID):
    #marks task as currently uncomplete and then outputs default values
    df = pd.read_csv(file_path)
    index = df[df["Task ID"] == task_ID].index
    
    if not index.empty:
        df.loc[index, "Status"] = "uncompleted"
        df.loc[index, "Time Input"] = ""
        df.loc[index, "Completion Time"] = ""

        df.to_csv(file_path, index=False)
        print(f"Task {task_ID} marked as uncompleted")
    else:
        print(f"Task ID {task_ID} not found.")

def getProgessPerc():
    #displays information about status for all tasks
    df = pd.read_csv(file_path)
    #print(df)
    totalTask = 0
    completeTask = 0
    progressPerc = 0
    curr_date = datetime.now().strftime("%Y-%m-%d")
    for index, row in df.iterrows():
        if row['Work Date'] == curr_date:
            totalTask += 1
        if row['Status'] == 'completed' and row['Work Date'] == curr_date:
            completeTask += 1
        #print(row['Status'], row['Task ID'])

    #returns the tasks completed compared to amount of tasks
    if totalTask != 0:
        progressPerc = (completeTask/totalTask)
    return progressPerc

#I think no need to pass status / completion time / time input since those are edited only by checking the box
#No need to pass creation time since that shouldn't change anyways 
def edit_task(task_ID, task_name, description, work_date, deadline, priority, tags):
    df = pd.read_csv(file_path)
    index = df[df["Task ID"] == task_ID].index
    
    if not index.empty:
        df.loc[index, "Task Name"] = task_name
        df.loc[index, "Description"] = description
        df.loc[index, "Work Date"] = work_date
        df.loc[index, "Deadline"] = deadline
        df.loc[index, "Priority"] = priority
        df.loc[index, "Tags"] = tags

        df.to_csv(file_path, index=False)
        print(f"Task {task_ID} has been updated")
    else:
        print(f"Task ID {task_ID} not found.")


def getCompletedTask():
    df = pd.read_csv(file_path)
    completedTask = []
    for index, row in df.iterrows():
        if row['Status'] == 'completed':
            completedTask.append(row['Task Name'])

    return completedTask


def remove_task(task_ID):
    pass
