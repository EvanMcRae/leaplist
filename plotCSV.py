import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load CSV file into variable data
data = pd.read_csv("Leaplist.csv")

def convert_time(time):
    try:
        hours, minutes = map(int, time.split(':'))
        #return hr / min converted to hr
        return hours + minutes / 60
    except ValueError:
        raise ValueError("Couldn't convert time to minutes")

#Py chart to represent information
def daily_view_pychart(day):
    completed = 0
    uncompleted = 0
    # Get current date
    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == day:
            if row['Status'] == 'completed':
                completed += 1
            else:
                uncompleted += 1

    fig = plt.figure(figsize=(10, 5))
    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    plt.pie(y, labels=mylabels)
    
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_fig.png")
    plt.savefig(output_path)      
    return output_path

#For specific time frame tasks ---------------------------------------------------------------------------------------
def specific_date(start_date, end_date):
    completed = 0
    uncompleted = 0
    
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

    #plt.pie(y, labels=mylabels)
    plt.bar(mylabels, y, color=['blue','green'])
    plt.title("Completed vs Uncompleted Tasks from " + start_date + " to " + end_date)
    plt.ylabel("Number of Tasks")
    output_dir = "vis_plots"
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

    #plt.pie(y, labels=mylabels)
    plt.bar(mylabels, y, color=['blue', 'green'])
    plt.title("Completed vs Uncompleted Tasks from " + month)
    plt.ylabel("Number of Tasks")

    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "monthly_fig.png")
    plt.savefig(output_path)
    return output_path

# For Daily Task ---------------------------------------------------------------------------------------------------
def daily_view(day):
    task_list = {}
    total_time = 0

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == day and row["Status"] == 'completed':
            # Calculate how much of the task is completed
            time_input = convert_time(row["Time Input"])
            total_time += time_input
            #percentage = float(row["Time Input"]) / float(row["Completion Time"])
            task_list[row["Task Name"]] = time_input
    
    x = list(task_list.keys()) + ["Total Time"]
    y = list(task_list.values()) + [total_time]

    #fig = plt.figure(figsize=(10, 5))
    #plt.bar(x, y, color='green', width=0.4)

    plt.figure(figsize=(10, 5))
    bars = plt.bar(x, y, color=['green'] * len(task_list) + ['blue'], width=0.4)
    for bar, time in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center', va='bottom')

	# Set the x and y axis limits to start from 0
    #plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    #plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Time Spent on Today's Tasks")
    plt.xlabel("Task")
    plt.ylabel("Time Spent in Hours")
    
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_fig_bar.png")
    plt.savefig(output_path)      
    return output_path

# Monthly Time bar graph
def month_time(month):
    task_list = {}

    for index, row in data.iterrows():
        if row["Work Date"][0:7] == str(month):
            print("Task found: %f", row["Task Name"])
            percentage = float(row["Time Input"]) / float(row["Completion Time"])
            task_list.update({row["Task Name"]: percentage})
    
    x = list(task_list.keys())
    y = list(task_list.values())

    fig = plt.figure(figsize=(10, 5))

    plt.bar(x, y, color='darkgreen', width=0.4)
    
	# Set the x and y axis limits to start from 0
    plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Monthly Tasks")
    plt.xlabel("Task")
    plt.ylabel("Percentage Completed of Task")

    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "monthly_output_fig.png")
    plt.savefig(output_path)
    return output_path

# For specific tasks within a time frame and how long was spent on each task
def date_time(start_date, end_date):
    task_list = {}

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
    
    output_dir = "vis_plots"
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

    #fig = plt.figure(figsize=(10, 5))
    # create a split of completed tasks in the month
    y = [completed, uncompleted]
    mylabels = ["Completed", "Uncompleted"]

    #plt.pie(y, labels=mylabels)
    plt.bar(mylabels, y, color=['blue', 'green'])
    plt.title("Completed vs Uncompleted Tasks from Today with Tag: " + tag_id )
    plt.ylabel("Number of Tasks")
    output_dir = "vis_plots"
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

    #plt.pie(y, labels=mylabels)
    plt.bar(mylabels, y, color=['blue', 'green'])
    plt.title("Completed vs Uncompleted Tasks from This Month with Tag: " + tag_id)
    plt.ylabel("Number of Tasks")
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "month_tag_fig.png")
    plt.savefig(output_path)
    return output_path

#For specific time frame tasks ---------------------------------------------------------------------------------------
def date_py_tag(start_date, end_date, tag_id):
    completed = 0
    uncompleted = 0
    
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

    #plt.pie(y, labels=mylabels)
    plt.bar(mylabels, y, color=['blue', 'green'])
    plt.title("Completed vs Uncompleted Tasks from " + start_date +" to " + end_date + " with Tag: " + tag_id, fontsize=10)
    plt.ylabel("Number of Tasks")
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "date_tag_fig.png")
    plt.savefig(output_path)      
    return output_path

#For tag specific items and time input
# For Daily Task ---------------------------------------------------------------------------------------------------
def daily_tag_bar(day, tag_id):
    task_list = {}

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == day:
            if row['Tags'] == tag_id:
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
    
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_tag_bar.png")
    plt.savefig(output_path)      
    return output_path

# For specific tasks within a time frame and how long was spent on each task
def date_tag_bar(start_date, end_date, tag_id):
    task_list = {}

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date:
            if row['Tags'] == tag_id:
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
    
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "date_time_bar.png")
    plt.savefig(output_path)      
    return output_path

def month_tag_bar(month, tag_id):
    task_list = {}

    for index, row in data.iterrows():
        if row['Work Date'][0:7] == month:
            if row['Tags'] == tag_id:
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

    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "month_tag_bar.png")
    plt.savefig(output_path)
    return output_path


# I want to add a function for:
# daily / all tags
# monthly / all tags
# specific date / all tags
# daily / all tags / time input
# monthly / all tags / time input
# specific date / all tags / time input
# Function to create plot based on productivity parameters
def create_productivity(daily, start_date, end_date, month, tag_id, time_input):
    if time_input is False:
        if tag_id is None:
            if daily:
                return daily_view_pychart(daily)
            if start_date and end_date:
                return specific_date(start_date, end_date)
            if month:
                return monthly_view(month)
        else:
            if tag_id == "All Tags":
                pass
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
                return daily_view(daily)
            if month:
                return month_time(month)
            if start_date and end_date:
                return date_time(start_date, end_date)
        else:
            if tag_id == "All Tags":
                pass
            else:
                if daily:
                    return daily_tag_bar(daily, tag_id)
                if start_date and end_date:
                    return date_tag_bar(start_date, end_date, tag_id)
                if month:
                    return month_tag_bar(month, tag_id)
        

    raise ValueError("Invalid parameters: Could not create productivity plot")
    
#if __name__ == "__main__":
    #daily = None
    #start_date = "2024-10-31"
    #end_date = "2024-11-15"
    #month = None
    #tag_id = "household"
    #time_input = None
    #create_productivity(daily, start_date, end_date, month, tag_id, time_input)
