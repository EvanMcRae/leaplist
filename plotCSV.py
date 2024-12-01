import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load CSV file into variable data
data = pd.read_csv("Leaplist.csv")


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
    output_dir = "daily_fig"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_fig.png")
    plt.savefig(output_path)      
    return output_path


#For specific time frame tasks ---------------------------------------------------------------------------------------
def specific_date(start_date, end_date):
    task_list = {}
    completed = 0
    uncompleted = 0
    
    iter = int(start_date[8:9]+1)
    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date:
            if row["Status"] == 'completed':
                completed += 1
            else:
                uncompleted += 1

    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels)
    output_dir = "tag_fig_py"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "tag_fig_py.png")
    plt.savefig(output_path)      
    return output_path


# For Monthly Tasks -----------------------------------------------------------------------------------------------------
def monthly_view(month):
    completed = 0
    uncompleted = 0

    for index, row in data.iterrows():
        if row['Work Date'][0:7] == month:
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


# For Daily Task ---------------------------------------------------------------------------------------------------
def daily_view():
    task_list = {}
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == current_date:
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
    
    output_dir = "daily_fig"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_fig.png")
    plt.savefig(output_path)      
    return output_path

# Monthly Time bar graph
def month_time(month):
    task_list = {}

    for index, row in data.iterrows():
        if row['Work Date'][0:7] == month:
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
    plt.title("Monthly Tasks")
    plt.xlabel("Task")
    plt.ylabel("Percentage Completed of Task")

    output_dir = "monthly_output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "monthly_fig.png")
    plt.savefig(output_path)
    return output_path


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
    
    output_dir = "sel_date_fig"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sel_date_fig.png")
    plt.savefig(output_path)      
    return output_path

#Functions for if no time input but with tag specific
#Py chart to represent information
def daily_view_py_tag(tag_id):
    completed = 0
    uncompleted = 0
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == current_date:
            if row['Tags'] == tag_id:
                if row['Status'] == 'completed':
                    completed += 1
                else:
                    uncompleted += 1

    fig = plt.figure(figsize=(10, 5))
    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels) 
    output_dir = "daily_tag_fig"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_tag_fig.png")
    plt.savefig(output_path)      
    return output_path


# For Monthly Tasks -----------------------------------------------------------------------------------------------------
def month_py_tag(month, tag_id):
    completed = 0
    uncompleted = 0

    for index, row in data.iterrows():
        if row['Work Date'][0:7] == month:
            if row['Tags'] == tag_id:
                if row['Status'] == 'completed':
                    completed += 1
                else:
                    uncompleted += 1

    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels)
    output_dir = "month_tag_fig"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "month_tag_fig.png")
    plt.savefig(output_path)
    return output_path

#For specific time frame tasks ---------------------------------------------------------------------------------------
def date_py_tag(start_date, end_date, tag_id):
    completed = 0
    uncompleted = 0
    
    iter = int(start_date[8:9]+1)
    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date:
            if row['Tags'] == tag_id:
                if row["Status"] == 'completed':
                    completed += 1
                else:
                    uncompleted += 1

    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels)
    output_dir = "date_tag_fig"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "date_tag_fig.png")
    plt.savefig(output_path)      
    return output_path


#For tag specific items and time input
# For Daily Task ---------------------------------------------------------------------------------------------------
def daily_tag_bar(tag_id):
    task_list = {}
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == current_date:
            if row['Tags'] == tag_id:
                if row['Status'] == 'completed':
                    plt.bar(row['Task Name'], 1, color='black')
                else:
                    percentage = float(row["Time Input"]) / float(row["Completion Time"])
                    plt.bar(row['Task Name'], percentage, color='limegreen')

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
    
    output_dir = "daily_tag_bar"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_tag_bar.png")
    plt.savefig(output_path)      
    return output_path

# For specific tasks within a time frame and how long was spent on each task
def date_tag_bar(start_date, end_date, tag_id):
    task_list = {}

    iter = int(start_date[8:9]+1)
    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date:
            if row['Tags'] == tag_id:
                if row['Status'] == 'completed':
                    plt.bar(row['Task Name'], 1, color='black')
                else:
                    percentage = float(row["Time Input"]) / float(row["Completion Time"])
                    plt.bar(row['Task Name'], percentage, color='limegreen')
    
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
    
    output_dir = "date_time_bar"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "date_time_bar.png")
    plt.savefig(output_path)      
    return output_path


def month_tag_bar(month, tag_id):
    task_list = {}

    for index, row in data.iterrows():
        if row['Work Date'][0:7] == month:
            if row['Tags'] == tag_id:
                if row['Status'] == 'completed':
                    plt.bar(row['Task Name'], 1, color='black')
                else:
                    percentage = float(row["Time Input"]) / float(row["Completion Time"])
                    plt.bar(row['Task Name'], percentage, color='limegreen')
    
    x = list(task_list.keys())
    y = list(task_list.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(x, y, color='green', width=0.4)
    
	# Set the x and y axis limits to start from 0
    plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Monthly Tasks")
    plt.xlabel("Task")
    plt.ylabel("Percentage Completed of Task")

    output_dir = "month_tag_bar"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "month_tag_bar.png")
    plt.savefig(output_path)
    return output_path


# Function to create plot based on productivity parameters
def create_productivity(daily, start_date, end_date, month, tag_id, time_input):
    if time_input is None:
        if tag_id is None:
            if daily:
                return daily_view_pychart()
            if start_date and end_date:
                return specific_date(start_date, end_date)
            if month:
                return monthly_view(month)
        else:
            if daily:
                return daily_view_py_tag(tag_id)
            if start_date and end_date:
                return date_py_tag(start_date, end_date, tag_id)
            if month:
                return month_py_tag(month, tag_id)
    else:
        if tag_id is None:
            if daily:
                return daily_view()
            if month:
                return month_time(tag_id)
            if start_date and end_date:
                return date_time(start_date, end_date)
        else:
            if daily:
                return daily_tag_bar(tag_id)
            if start_date and end_date:
                return date_tag_bar(start_date, end_date, tag_id)
            if month:
                return month_tag_bar(month, tag_id)
        

    raise ValueError("Invalid parameters: Could not create productivity plot")
    
