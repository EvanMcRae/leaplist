import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load CSV file into variable data
#TODO this does not work at runtime
data = pd.read_csv("LeapList.csv")

def convert_time(time):
    try:
        hours, minutes = map(int, time.split(':'))
        #return hr / min converted to hr
        return hours + minutes / 60
    except ValueError:
        raise ValueError("Couldn't convert time to minutes")

#Py chart to represent information
def daily_view_pychart(day):
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
    task_list = {}
    total_time = 0

    for index, row in data.iterrows():
        #if row["Work Date"][0:7] == str(month):
        if row["Work Date"].startswith(month) and row["Status"] == 'completed':
            print("Task found: %f", row["Task Name"])
            #percentage = float(row["Time Input"]) / float(row["Completion Time"])
            #task_list.update({row["Task Name"]: percentage})
            time_input = convert_time(row["Time Input"])
            total_time += time_input
            task_list[row["Task Name"]] = time_input

    x = list(task_list.keys()) + ["Total Time"]
    y = list(task_list.values()) + [total_time]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=['green'] * len(task_list) + ['blue'], width=0.4)
    for bar, time in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center', va='bottom')

    #plt.bar(x, y, color='darkgreen', width=0.4)
    
	# Set the x and y axis limits to start from 0
    #plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    #plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Time Spend on Tasks This Month")
    plt.xlabel("Task")
    plt.ylabel("Time Spent in Hours")

    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "monthly_output_fig.png")
    plt.savefig(output_path)
    return output_path

# For specific tasks within a time frame and how long was spent on each task
def date_time(start_date, end_date):
    data = pd.read_csv("LeapList.csv")
    task_list = {}
    total_time = 0

    for index, row in data.iterrows():
        # if row["Work Date"][0:7] == str(month):
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date and row["Status"] == 'completed':
            print("Task found: %f", row["Task Name"])
            # percentage = float(row["Time Input"]) / float(row["Completion Time"])
            # task_list.update({row["Task Name"]: percentage})
            time_input = convert_time(row["Time Input"])
            total_time += time_input
            task_list[row["Task Name"]] = time_input

    x = list(task_list.keys()) + ["Total Time"]
    y = list(task_list.values()) + [total_time]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=['green'] * len(task_list) + ['blue'], width=0.4)
    for bar, time in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center', va='bottom')

    # plt.bar(x, y, color='darkgreen', width=0.4)

    # Set the x and y axis limits to start from 0
    # plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    # plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)

    # Label Plot
    plt.title("Time Spend on Tasks From " + start_date + " to " + end_date)
    plt.xlabel("Task")
    plt.ylabel("Time Spent in Hours")

    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "specific_output_fig.png")
    plt.savefig(output_path)
    return output_path

#Functions for if no time input but with tag specific
#Py chart to represent information
def daily_view_py_tag(tag_id):
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
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
    data = pd.read_csv("LeapList.csv")
    task_list = {}
    total_time = 0

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] == day:
            if row['Tags'] == tag_id and row["Status"] == 'completed':
                # Calculate how much of the task is completed
                #percentage = float(row["Time Input"]) / float(row["Completion Time"])
                #task_list.update({row["Task Name"]: percentage})
                time_input = convert_time(row["Time Input"])
                total_time += time_input
                # percentage = float(row["Time Input"]) / float(row["Completion Time"])
                task_list[row["Task Name"]] = time_input
    
    x = list(task_list.keys()) + ["Total on Tag " + tag_id]
    y = list(task_list.values()) + [total_time]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=['green'] * len(task_list) + ['blue'], width=0.4)
    for bar, time in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center', va='bottom')

    # Set the x and y axis limits to start from 0
    # plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    # plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)

    # Label Plot
    plt.title("Time Spent on Today's Tasks with Tag: " + tag_id)
    plt.xlabel("Task")
    plt.ylabel("Time Spent in Hours")
    
	# Set the x and y axis limits to start from 0
    #plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    #plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "daily_tag_bar.png")
    plt.savefig(output_path)      
    return output_path

# For specific tasks within a time frame and how long was spent on each task
def date_tag_bar(start_date, end_date, tag_id):
    data = pd.read_csv("LeapList.csv")
    task_list = {}
    total_time = 0

    # Determine if task is on current day for daily tasks
    for index, row in data.iterrows():
        if row["Work Date"] <= end_date and row["Work Date"] >= start_date and row["Status"] == 'completed':
            if row['Tags'] == tag_id:
                time_input = convert_time(row["Time Input"])
                total_time += time_input
                task_list[row["Task Name"]] = time_input

    x = list(task_list.keys()) + ["Total on Tag " + tag_id]
    y = list(task_list.values()) + [total_time]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=['green'] * len(task_list) + ['blue'], width=0.4)
    for bar, time in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center', va='bottom')

    # Label Plot
    plt.title("Time Spent on Tasks with Tag: " + tag_id + " From " + start_date + " to " + end_date)
    plt.xlabel("Task")
    plt.ylabel("Time Spent in Hours")
    
    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "date_time_bar.png")
    plt.savefig(output_path)      
    return output_path

def month_tag_bar(month, tag_id):
    data = pd.read_csv("LeapList.csv")
    task_list = {}
    total_time = 0

    for index, row in data.iterrows():
        if row["Work Date"].startswith(month) and row["Status"] == 'completed':
            if row['Tags'] == tag_id:
                #percentage = float(row["Time Input"]) / float(row["Completion Time"])
                #task_list.update({row["Task Name"]: percentage})
                time_input = convert_time(row["Time Input"])
                total_time += time_input
                task_list[row["Task Name"]] = time_input
    
    x = list(task_list.keys()) + ["Total on Tag " + tag_id]
    y = list(task_list.values()) + [total_time]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(x, y, color=['green'] * len(task_list) + ['blue'], width=0.4)
    for bar, time in zip(bars, y):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center', va='bottom')

    #fig = plt.figure(figsize=(10, 5))
    #plt.bar(x, y, color='green', width=0.4)
    
	# Set the x and y axis limits to start from 0
    #plt.xlim(-0.5, len(x))  # Ensure the bars have space and are centered on the x-axis
    #plt.ylim(0, 1)  # y-axis starts from 0 and goes up to 100% (since it's a percentage)
    
    # Label Plot
    plt.title("Monthly Time Spent on Tasks with Tag: " + tag_id)
    plt.xlabel("Task")
    plt.ylabel("Time Spent in Hours")

    output_dir = "vis_plots"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "month_tag_bar.png")
    plt.savefig(output_path)
    return output_path

def all_tags_no_time_input(daily, start_date, end_date, month):
    data = pd.read_csv("LeapList.csv")
    if daily is not None:
        tag_list = {}

        for index, row in data.iterrows():
            if pd.notna(row["Tags"]) and row["Work Date"] == daily:
                tag = row["Tags"]
                status = row["Status"]

                if tag not in tag_list:
                    tag_list[tag] = {"completed": 0, "uncompleted": 0}
                if status == "completed":
                    tag_list[tag]["completed"] += 1
                else:
                    tag_list[tag]["uncompleted"] += 1

        tags = list(tag_list.keys())
        num_comp = [tag_list[tag]["completed"] for tag in tags]
        num_uncomp = [tag_list[tag]["uncompleted"] for tag in tags]

        x_ind = range(len(tags))
        width = 0.4
        plt.figure(figsize=(12, 6))
        plt.bar([x - width / 2 for x in x_ind], num_comp, width=width, color='green',
                label='Completed')
        plt.bar([x + width / 2 for x in x_ind], num_uncomp, width=width, color='blue',
                label='Uncompleted')
        plt.xticks(ticks=x_ind, labels=tags, rotation=45, ha='center')
        plt.legend()

        plt.title("Completed vs Uncompleted Tasks Across All Tags Today")
        plt.xlabel("Tag")
        plt.ylabel("Number of Tasks")

        output_dir = "vis_plots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "daily_tag_bar.png")
        plt.savefig(output_path)
        return output_path

    if month is not None:
        tag_list = {}

        for index, row in data.iterrows():
            if pd.notna(row["Tags"]) and row["Work Date"].startswith(month):
                tag = row["Tags"]
                status = row["Status"]

                if tag not in tag_list:
                    tag_list[tag] = {"completed": 0, "uncompleted": 0}
                if status == "completed":
                    tag_list[tag]["completed"] += 1
                else:
                    tag_list[tag]["uncompleted"] += 1

        tags = list(tag_list.keys())
        num_comp = [tag_list[tag]["completed"] for tag in tags]
        num_uncomp = [tag_list[tag]["uncompleted"] for tag in tags]

        x_ind = range(len(tags))
        width = 0.4
        plt.figure(figsize=(12, 6))
        plt.bar([x - width / 2 for x in x_ind], num_comp, width=width, color='green',
                label='Completed')
        plt.bar([x + width / 2 for x in x_ind], num_uncomp, width=width, color='blue',
                label='Uncompleted')
        plt.xticks(ticks=x_ind, labels=tags, rotation=45, ha='center')
        plt.legend()

        plt.title("Completed vs Uncompleted Tasks Across All Tags This Month")
        plt.xlabel("Tag")
        plt.ylabel("Number of Tasks")

        output_dir = "vis_plots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "daily_tag_bar.png")
        plt.savefig(output_path)
        return output_path

    if start_date and end_date is not None:
        tag_list = {}

        for index, row in data.iterrows():
            if pd.notna(row["Tags"]) and row["Work Date"] <= end_date and row["Work Date"] >= start_date:
                tag = row["Tags"]
                status = row["Status"]

                if tag not in tag_list:
                    tag_list[tag] = {"completed": 0, "uncompleted": 0}
                if status == "completed":
                    tag_list[tag]["completed"] += 1
                else:
                    tag_list[tag]["uncompleted"] += 1

        tags = list(tag_list.keys())
        num_comp = [tag_list[tag]["completed"] for tag in tags]
        num_uncomp = [tag_list[tag]["uncompleted"] for tag in tags]

        x_ind = range(len(tags))
        width = 0.4
        plt.figure(figsize=(12, 6))
        plt.bar([x - width / 2 for x in x_ind], num_comp, width=width, color='green',
                label='Completed')
        plt.bar([x + width / 2 for x in x_ind], num_uncomp, width=width, color='blue',
                label='Uncompleted')
        plt.xticks(ticks=x_ind, labels=tags, rotation=45, ha='center')
        plt.legend()

        plt.title("Completed vs Uncompleted Tasks Across All Tags From " + start_date + " to " + end_date)
        plt.xlabel("Tag")
        plt.ylabel("Number of Tasks")

        output_dir = "vis_plots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "daily_tag_bar.png")
        plt.savefig(output_path)
        return output_path

def all_tags_time_input(daily, start_date, end_date, month):
    data = pd.read_csv("LeapList.csv")
    if daily is not None:
        tag_list = {}
        total_time = 0

        for index, row in data.iterrows():
            if pd.notna(row["Tags"]) and row["Work Date"] == daily and row["Status"] == 'completed':
                time_input = convert_time(row["Time Input"])
                total_time += time_input
                tag_list[row["Tags"]] = tag_list.get(row["Tags"], 0) + time_input

        x = list(tag_list.keys()) + ["Total Time on All Tags"]
        y = list(tag_list.values()) + [total_time]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(x, y, color=['green'] * len(tag_list) + ['blue'], width=0.4)
        for bar, time in zip(bars, y):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center',
                     va='bottom')

        plt.title("Time Spent Across All Tags Today")
        plt.xlabel("Tag")
        plt.ylabel("Time Spent in Hours")

        output_dir = "vis_plots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "daily_tag_bar.png")
        plt.savefig(output_path)
        return output_path

    if month is not None:
        tag_list = {}
        total_time = 0

        for index, row in data.iterrows():
            if pd.notna(row["Tags"]) and row["Work Date"].startswith(month) and row["Status"] == 'completed':
                time_input = convert_time(row["Time Input"])
                total_time += time_input
                tag_list[row["Tags"]] = tag_list.get(row["Tags"], 0) + time_input

        #x = list(tag_list.keys()) + ["Total Time on All Tags"]
        #y = list(tag_list.values()) + [total_time]
        x = [str(tag) for tag in tag_list.keys()] + ["Total Time on All Tags"]
        y = list(tag_list.values()) + [total_time]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(x, y, color=['green'] * len(tag_list) + ['blue'], width=0.4)
        for bar, time in zip(bars, y):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center',
                     va='bottom')

        plt.title("Time Spent Across All Tags This Month")
        plt.xlabel("Tag")
        plt.ylabel("Time Spent in Hours")

        output_dir = "vis_plots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "daily_tag_bar.png")
        plt.savefig(output_path)
        return output_path

    if start_date and end_date is not None:
        tag_list = {}
        total_time = 0

        for index, row in data.iterrows():
            if pd.notna(row["Tags"]) and row["Work Date"] <= end_date and row["Work Date"] >= start_date and row["Status"] == 'completed':
                time_input = convert_time(row["Time Input"])
                total_time += time_input
                tag_list[row["Tags"]] = tag_list.get(row["Tags"], 0) + time_input

        x = list(tag_list.keys()) + ["Total Time on All Tags"]
        y = list(tag_list.values()) + [total_time]

        plt.figure(figsize=(12, 6))
        bars = plt.bar(x, y, color=['green'] * len(tag_list) + ['blue'], width=0.4)
        for bar, time in zip(bars, y):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{time:.2f} hrs", ha='center',
                     va='bottom')

        plt.title("Time Spent Across All Tags From " + start_date + " to " + end_date)
        plt.xlabel("Tag")
        plt.ylabel("Time Spent in Hours")

        output_dir = "vis_plots"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "daily_tag_bar.png")
        plt.savefig(output_path)
        return output_path

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
                return all_tags_no_time_input(daily, start_date, end_date, month)
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
                return all_tags_time_input(daily, start_date, end_date, month)
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
