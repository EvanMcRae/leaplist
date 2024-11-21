# Command to download matplot library
# pip install pandas matplotlib

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load CSV file into variable data
data = pd.read_csv("Leaplist.csv")

#Determine if Daily, Monthly, Tag Specific View is wanted
# For Daily Task ---------------------------------------------------------------------------------------------------
def daily_view():
	# Determine if task is on current day for daily tasks
    for index, row in df.iterrows():
		totalTask = 0
		if row['Work Date'] == datetime.now().strftime("%Y-%m-%d"):
			# Calculate how much of the task is completed
			percentage = row["Time Input"] / row["Completion Time"]

			# Plot Data in Bar Graph form
			plt.bar(totalTask, percentage, color='limegreen')
		 	# Label the Bar
		    plt.text(totalTask, percentage + 0.05, row["Task Name"], ha='center', va='bottom')
	
			totalTask += 1
		
	# Label Plot
	plt.title("Daily Tasks")
	plt.xlabel("Task")
	plt.ylabel("Percentage Completed")
	
	# Show the plot
	plt.savefig("output/daily_view.png")
	return plt

	
# For Monthly Tasks -------------------------------------------------------------------------------------------
def monthly_view(month):
	totalTask = 0
	completed_task = 0
	for index, row in df.iterrows():
		
		if row['Work Date'] == datetime.now().strftime("%Y-%m-%d"):
			# Calculate how much of the task is completed
			percentage = row["Time Input"] / row["Completion Time"]

			# Plot Data in Bar Graph form
			plt.bar(totalTask, percentage, color='limegreen')
		 	# Label the Bar
		    plt.text(totalTask, percentage + 0.05, row["Task Name"], ha='center', va='bottom')
	
			totalTask += 1

	# create a split of completed tasks in the month
	y = [completed_task, totalTask]
	mylabels = ["Completed", "Uncompleted"]

	plt.pie(y, labels = mylabels)		
	plt.show() 
	


# For Specific Tag Tasks -------------------------------------------------------------------------------------------
def tag_task(tag_id):
	task = 0
	completed = 0

	for e in data:
		# Determine if task is on current data for monthly tasks
		if e[8] in tag_id:
			task += 1
		 	if e['Status'] == 'completed':
		  		completed += 1
		  	
			# Plot Data in Bar Graph form
			plt.bar(task, percentage, color='limegreen')
			# Label the Bar
			plt.text(task, completed + 0.05, e.iloc[1], ha='center', va='bottom')


	# Label Plot
	plt.title("Tag Specific Tasks")
	plt.xlabel(tag_id)
	plt.ylabel("Amount of Specific Tag Tasks Completed")
	
	# Show the plot
	plt.show()

#main function that filters through inputs to determine what type of graph is wanted and calls the function to generate it
def create_productivity(daily, start_date, end_date, month, tags, time_input):
	if not time_input:
		#creates a plot of all tasks for the day and how completed they are
		if not daily:
			return daily_view()

		#creates a plot filled with only one tag and shows how completed they are
		if not tags:
			return tag_task(tags)

		#plots amount of tasks from a starting date till the end date
		if not (start_date or end_date):
			return specific_date(start_date, end_date)

		#plots the amount of tasks in a month; pi chart of completed vs not completed
		#maybe pi chart of the different tasks for the month
		if not month:
			return monthly_view(month)

	elif:
		#plots tags and the amount of time spent on each tag
		if not tags:
			return tag_task_time(tags)

		#plots days from start to end date and shows how many hours were spent working on tasks each day
		if not (start_date or end_date):
			return date_time(start_date, end_date)


			
