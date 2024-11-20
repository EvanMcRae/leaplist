# Command to download matplot library
# pip install pandas matplotlib

import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
data = pd.read_csv("Leaplist.csv")

# Load which view: 1 = daily, 2 = monthly, 3 = tag
# ??????????????
view = 1

#Determine if Daily, Monthly, Tag Specific View is wanted
# For Daily Task ---------------------------------------------------------------------------------------------------
if int(view) == 1:

	task = 0
	# Determine if task is on current day for daily tasks
	for e in data:
		if e.iloc[7][0:10] == current_date.strftime("%Y-%m-%d"):
			# Calculate how much of the task is completed
			percentage = e[10] / e[9]
			# Plot Data in Bar Graph form
			plt.bar(task, percentage, color='limegreen')
		 	# Label the Bar
		    plt.text(task, percentage + 0.05, e[1], ha='center', va='bottom')
	
			task += 1
		
		
	# Label Plot
	plt.title("Daily Tasks")
	plt.xlabel("Task")
	plt.ylabel("Percentage Completed")
	
	# Show the plot
	plt.show()
	
	task = 0

	
# For Monthly Tasks -------------------------------------------------------------------------------------------
if int(view) == 2:
	task = 0
	done = 0
	# Determine if task is on current data for monthly tasks
	# variable used to keep track of tasks done in each day
	curr = current_date.strftime("%Y-%m-%d")
	for e in data:
		if e[7][0:8] == current_date.strftime("%Y-%m"):
			if e['Status'] == 'completed':
				done += 1
			task += 1

	# create a split of completed tasks in the month
	y = [done, task-done]
	mylabels = ["Completed", "Uncompleted"]

	plt.pie(y, labels = mylabels)		
	plt.show() 
	


# For Specific Tag Tasks -------------------------------------------------------------------------------------------
if view == 3:
	task = 0
	completed = 0
	# Determine which tag to create a graph for	
	tag_choice = "Homework"

	for e in data:
		# Determine if task is on current data for monthly tasks
		if e[8] in tag_choice:
			task += 1
		 	if e['Status'] == 'completed':
		  		completed += 1
		  	
			# Plot Data in Bar Graph form
			plt.bar(task, percentage, color='limegreen')
			# Label the Bar
			plt.text(task, completed + 0.05, e.iloc[1], ha='center', va='bottom')


	# Label Plot
	plt.title("Tag Specific Tasks")
	plt.xlabel(tag_choice)
	plt.ylabel("Amount of Specific Tag Tasks Completed")
	
	# Show the plot
	plt.show()
