# CMSC 447 Fall 2024 Logic Loopers Group Project

**Authors:** David Bower, Evan McRae, Olivia Patterson, Sophia Xu, William Zheng

**Project Title:** Leaplist

## Description: 
Leaplist is a modern to-do list application to help users leap into productivity! Leaplist is a desktop application designed to enhance the user's productivity by providing advanced task organization tools, and customizable productivity visualizations, and encourage user productivity. 

# Tech Stack: 
- Programming Language: Python
- Libraries: 
    - Tkinter: For implementing the GUI
    - Matplotlib: For creating data visualizations and plots
    - Pandas: For organizing and accessing data stored in a CSV file
    - OS: For handling local file operations and CSV communication
    - Pillow (PIL): For working with and processing images
    - UUID: For generating unique task IDs

## Key Project Components: 
CSV data manipulation, GUI design, data visualization

## Project Technical Problem and Scope: 
This project focuses on developing a to-do list application designed to enhance task organization and improve user productivity. Unlike traditional to-do list apps, this project incorporates features such as tagging tasks, separating tasks into categorized views (e.g., today's tasks, upcoming tasks, and completed tasks), and providing productivity visualizations based on user input. Users can assign a work date for when they want to start working on a task and a deadline for its completion. Tasks not completed on their designated work date are automatically rescheduled for the next day unless otherwise updated by the user.

One of the standout features is prompting users to input the time spent on a task upon marking it as complete. This data enables the generation of insightful visualizations, such as time spent on tasks by tag or over custom time ranges. These visualizations aim to help users better understand their time usage, improve task efficiency, and track progress over time. Additionally, a progress bar encourages daily task completion, promoting consistent productivity.

The primary technical challenges included managing the CSV-based data structure for efficient task storage and retrieval, ensuring smooth integration of GUI elements, and designing meaningful visualizations. A significant obstacle arose when testing the app on macOS, as Tkinter (the chosen library for GUI implementation) proved to be slow and unreliable on macOS compared to Windows. This highlighted the need for platform-aware development and a potential future migration to a more robust library (like PyQt) for better cross-platform support.

The project ultimately serves as an exploration of backend data manipulation and frontend GUI integration in Python. It demonstrates the importance of leveraging user input for both functionality and visual engagement, as well as the challenges of ensuring consistent performance across different operating systems.

## Instructions to run the provided executable (Windows ONLY):
1. Download `leaplistgui-exec.zip` and unzip.
2. Double-click on `leaplistgui.exe` inside the unzipped directory and the application will open on your machine.

## Instructions to run via a Python Interpreter: 
1. Ensure Python is installed on your machine.
2. Ensure the necessary libraries outlined above are installed.
3. Clone or download the repository containing the Leaplist files.
4. Open the files on an IDE or navigate to them in your terminal .
5. Run `leaplistgui.py`.
6. The application should pop up on your machine and allow you to interact with it. Please be aware that if you are running it on a Mac, the application will run much more slowly and might require multiple clicks before registering when interacting with the GUI. 
