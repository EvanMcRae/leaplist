import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load CSV file into variable data
data = pd.read_csv("Leaplist.csv")

# For Daily Task ---------------------------------------------------------------------------------------------------
def daily_view():
    task_list = {}
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == current_date:
            print(row["Task Name"])
            # Calculate how much of the task is completed
            percentage = float(row["Time Input"]) / float(row["Completion Time"])
            task_list.update({row["Task Name"]: percentage})
    
    x = list(task_list.keys())
    y = list(task_list.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(x, y, color='green', width=0.4)
    
	# Set the x and y axis limits to start from 0
    plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Daily Tasks")
    plt.xlabel("Task")
    plt.ylabel("Percentage Completed of Tasks for Today")
    
    #plt.show()
    plt.savefig('daily_fig.png')
    return 'daily_fig.png'

#Py chart to represent information
def daily_view_pychart():
    task_list = {}
    completed = 0
    uncompleted = 0
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == current_date:
            if row['Status'] == 'completed':
                plt.bar(row['Task Name'], 1, color='black')
            else:
                percentage = float(row["Time Input"]) / float(row["Completion Time"])
                plt.bar(row['Task Name'], percentage, color='limegreen')

    fig = plt.figure(figsize=(10, 5))
    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels)        
    plt.savefig('daily_fig.png')
    return 'daily_fig.png'


# For Monthly Tasks -----------------------------------------------------------------------------------------------------
def monthly_view(month):
    completed = 0
    uncompleted = 0
    # Get current month in YYYY-MM format
    current_month = datetime.now().strftime("%Y-%m")

    for index, row in data.iterrows():
        if row['Work Date'][0:7] == current_month:
            if row["Status"] == 'completed':
                completed += 1
            else:
                uncompleted += 1

    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels)
    output_dir = "monthly_output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "monthly_fig.png")
    plt.savefig(output_path)
    return output_path

# For Specific Tag Tasks -------------------------------------------------------------------------------------------
def tag_task(tag_id):
    for index, row in data.iterrows():
        if row['Tags'] == tag_id:
            if row['Status'] == 'completed':
                plt.bar(row['Task Name'], 1, color='black')
            else:
                percentage = float(row["Time Input"]) / float(row["Completion Time"])
                plt.bar(row['Task Name'], percentage, color='limegreen')

    # Label Plot
    plt.title("Tag Specific Tasks")
    plt.xlabel(tag_id)
    plt.ylabel("Amount of Specific Tag Tasks Completed")
    
    plt.savefig('tag_fig.png')
    return 'tag_fig.png'

# For tasks with a specific task and shows how much time was spent on task
def tag_task_time(tags):
    task_list = {}
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == current_date:
            print(row["Task Name"])
            # Calculate how much of the task is completed
            percentage = float(row["Time Input"]) / float(row["Completion Time"])
            task_list.update({row["Task Name"]: percentage})
    
    x = list(task_list.keys())
    y = list(task_list.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(x, y, color='green', width=0.4)
    
	# Set the x and y axis limits to start from 0
    plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Daily Tasks")
    plt.xlabel("Task")
    plt.ylabel("Percentage Completed of Tasks for Today")
    
    #plt.show()
    plt.savefig('daily_fig.png')
    return 'daily_fig.png'

    
#For specific time frame tasks ---------------------------------------------------------------------------------------
def specific_date(start_date, end_date):
    task_list = {}
    completed = 0
    uncompleted = 0

    iter = int(start_date[8:9]+1)
    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date:
            if row['Status'] == 'completed':
                plt.bar(row['Task Name'], 1, color='black')
            else:
                percentage = float(row["Time Input"]) / float(row["Completion Time"])
                plt.bar(row['Task Name'], percentage, color='limegreen')

    # Label Plot
    plt.title("Tag Specific Tasks")
    plt.xlabel(tag_id)
    plt.ylabel("Amount of Specific Tag Tasks Completed")
    
    plt.savefig('tag_fig.png')
    return 'tag_fig.png'

# For specific tasks within a time frame and how long was spent on each task
def date_time(start_date, end_date):
    task_list = {}

    iter = int(start_date[8:9]+1)
    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date:
            # Calculate how much of the task is completed
            percentage = float(row["Time Input"]) / float(row["Completion Time"])
            task_list.update({row["Task Name"]: percentage})
    
    x = list(task_list.keys())
    y = list(task_list.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(x, y, color='blue', width=0.4)
    
	# Set the x and y axis limits to start from 0
    plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Tasks Within Selected Dates")
    plt.xlabel("Task")
    plt.ylabel("Percentage Completed of Tasks for Selected Dates")
    
    plt.savefig('sel_date_fig.png')
    return 'sel_date_fig.png'

# Function to create plot based on productivity parameters
def create_productivity(daily, start_date, end_date, month, tag_id, time_input):
    if time_input is None:
        if daily:
            return daily_view_pychart()
        if tag_id:
            return tag_task(tag_id)
        if start_date and end_date:
            return specific_date(start_date, end_date)
        if month:
            return monthly_view(month)
    else:
        if daily:
            return daily_view()
        if tag_id:
            return tag_task_time(tag_id)
        if start_date and end_date:
            return date_time(start_date, end_date)

    raise ValueError("Invalid parameters: Could not create productivity plot")

#if __name__ == "__main__":
    
    #daily = None
    #start_date = None
    #end_date = None
    #month = "2024-11"
    #tag_id = None
    #time_input = None

    #create_productivity(daily, start_date, end_date, month, tag_id, time_input)
    
