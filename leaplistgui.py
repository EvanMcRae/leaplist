import tkinter
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sys
import leaplistcsv as llcsv
import plotCSV as pCSV
import datetime
from tkcalendar import Calendar
#from playsound import playsound

# fixes some ugly blurring on windows
# if sys.platform == "win32":
#     from ctypes import windll
#     windll.shcore.SetProcessDpiAwareness(1)

# TODO: add more task functions to this
class Task():
    def __init__(self, parent_frame=None, progress_bar=None, task_id=None, refresh=None):
        super().__init__()

        # to clean up gui bugs :) 
        if parent_frame != None:
            # pass parent frame and progress bar from add_task
            self.frame = ttk.Frame(parent_frame) # , bg = '#605d60'
            self.frame.pack(padx = 20, pady = 20, fill = 'x', expand = True)
            self.progress_bar = progress_bar

            self.task_id = 0
            self.check = tkinter.Checkbutton()
            self.label = tkinter.Label()
            self.completed = tkinter.BooleanVar()

            self.editing = True

            # add task frame
            self.add_task_frame = tkinter.Frame(self.frame, bg = '#605d60')

            # user input
            self.user_entry = tkinter.Entry(self.add_task_frame)
            self.user_entry.config(font = ('Arial', 15))

            # hexadecimal for font color
            self.user_entry.config(bg = '#fff')
            self.user_entry.config(fg = '#000')

            #We can always disable the text box when we don't want users to type anything.
            #self.user_entry.config(state= 'disabled')

            #does not limit amount of characters passed; limits amount of characters displayed
            self.user_entry.config(width=25)
            self.user_entry.grid(column = 0, row = 0 , padx = (10, 10), pady = 10)
            self.user_entry.focus_set()
            self.user_entry.bind("<KeyRelease>", self.on_type)

            # calendar + default work date and deadline
            self.calendar = Calendar(self.frame, selectmode = 'day', date_pattern = 'yyyy-mm-dd')
            self.calendar_open = False

            self.work_date = self.calendar.get_date()
            self.deadline = None
            
            self.calendar_popup = None

            self.description = ""
            self.tags = ""
            self.priority = ""

            self.refresh = refresh

            # add deadline button
            self.add_deadline_button = ttk.Button(self.add_task_frame, text = 'Add Deadline', command = self.enter_deadlinedate, style = 'TaskButton.TButton', cursor = 'hand2', width = 20)
            self.add_deadline_button.grid(column = 1, row = 0, padx = (0, 10), pady = 10)

            # add work date
            self.add_work_date_button = ttk.Button(self.add_task_frame, text = 'Add Work Date', command = self.enter_workdate, style = 'TaskButton.TButton', cursor = 'hand2', width = 20)
            self.add_work_date_button.grid(column = 2, row = 0, padx = (0, 10), pady = 10)

            self.save_button = ttk.Button(self.add_task_frame, text = 'Save', command = self.save_task, style = 'TaskButton.TButton', cursor = 'arrow', state = 'disabled')
            self.save_button.grid(column = 3, row = 0, padx = (0, 10), pady = 10)

            self.remove_button = ttk.Button(self.add_task_frame, text = 'Remove', command = self.remove_task, style = 'TaskButton.TButton', cursor = 'hand2', state = 'enabled')
            self.remove_button.grid(column = 4, row = 0, padx = (0, 10), pady = 10)

            self.view_task_frame = tkinter.Frame(self.frame, bg = '#605d60')
            
            # Creating a check mark widget. When clicked, it will mark task as completed - DAB
            self.check = tkinter.Checkbutton(self.view_task_frame, onvalue = 1, offvalue = 0, variable = self.completed, command = self.complete_task, bg = '#605d60', activebackground = '#605d60')
            self.check.pack(side = 'left')

            self.label = tkinter.Label(self.view_task_frame, fg = '#fff', bg = '#605d60', font = ('Arial', '20'))
            self.label.pack(fill = 'both', side = 'left', anchor = 'w', ipadx = 15)
            self.view_task_frame.bind('<Double-Button-1>', self.edit_task)
            self.label.bind('<Double-Button-1>', self.edit_task)

            if task_id != None:
                self.task_id = task_id
                task_name = llcsv.get_task_name(task_id)
                self.label.config(text = task_name)
                self.user_entry.insert(0, task_name)
                if len(task_name) > 0:
                    self.save_button.config(state = 'normal')
                    self.save_button.config(cursor = 'hand2')
                self.deadline = llcsv.get_deadline(task_id)
                self.work_date = llcsv.get_work_date(task_id)
                self.description = llcsv.get_description(task_id)
                self.tags = llcsv.get_tags(task_id)
                self.priority = llcsv.get_priority(task_id)
                if llcsv.is_completed(task_id):
                    self.check.config(state = 'active')
                    self.check.select()
                self.view_task_frame.pack(fill = 'both', expand = True)
            else:
                self.add_task_frame.pack(expand = True, fill = 'both')

    #displays the calendar in the position described along with the buttons for the GUI
    def open_calendar(self, date, func):
        self.calendar_popup = tkinter.Toplevel()
        date_key = date.split('-')
        self.calendar = Calendar(self.calendar_popup, selectmode = 'day', date_pattern = 'yyyy-mm-dd', year = int(date_key[0]), month = int(date_key[1]), day = int(date_key[2]))
        self.calendar.pack()
        self.calendar_open = True
        self.save_button.config(state = 'disabled')
        self.save_button.config(cursor = 'arrow')
        self.remove_button.config(state = 'disabled')
        self.remove_button.config(cursor = 'arrow')
        ok_button = tkinter.Button(self.calendar_popup, text="OK", command=func)
        ok_button.pack()

    def close_calendar(self):
        self.calendar_popup.destroy()
        self.calendar_open = False
        self.remove_button.config(state = 'normal')
        self.remove_button.config(cursor = 'hand2')
        if len(self.user_entry.get()) > 0:
            self.save_button.config(state = 'normal')
            self.save_button.config(cursor = 'hand2')
    
    #functions for entering data
    def on_type(self, event):
        if len(self.user_entry.get()) > 0 and not self.calendar_open:
            self.save_button.config(state = 'normal')
            self.save_button.config(cursor = 'hand2')
        else:
            self.save_button.config(state = 'disabled')
            self.save_button.config(cursor = 'arrow')

    def enter_workdate(self):
        if not self.calendar_open:
            self.open_calendar(self.work_date, self.enter_workdate)
            self.add_deadline_button.config(state = 'disabled')
            self.add_deadline_button.config(cursor = 'arrow')
            self.add_work_date_button.config(text = 'Confirm Work Date')
        else:
            self.work_date = self.calendar.get_date()
            self.close_calendar()
            self.add_deadline_button.config(state = 'normal')
            self.add_deadline_button.config(cursor = 'hand2')
            self.add_work_date_button.config(text = 'Add Work Date')

    def enter_deadlinedate(self):
        if not self.calendar_open:
            self.open_calendar(self.deadline, self.enter_deadlinedate)
            self.add_work_date_button.config(state = 'disabled')
            self.add_work_date_button.config(cursor = 'arrow')
            self.add_deadline_button.config(text = 'Confirm Deadline')
        else:
            self.deadline = self.calendar.get_date()
            self.close_calendar()
            self.add_work_date_button.config(state = 'normal')
            self.add_work_date_button.config(cursor = 'hand2')
            self.add_deadline_button.config(text = 'Add Deadline')

    #brings up a box to add a task and notes if wanted
    def save_task(self):
        self.editing = False

        # TODO: Placeholder!! need ways to pass these in
        description = "" # optional
        priority = "" # optional
        tags = "" # optional
        
        #retrieve text from user entry
        task = self.user_entry.get()
        
        #test call to function in csv.py     
        if (self.task_id == 0):   
            self.task_id = llcsv.new_task(task, description, self.work_date, self.deadline, priority, tags)
            self.progress_bar['value'] = (llcsv.getProgessPerc()) * 100
        else:
            llcsv.edit_task(self.task_id, task, description, self.work_date, self.deadline, priority, tags)
        
        self.refresh(self)
    
    #complete_task function
    def complete_task(self):

        if self.completed.get() == True:
            #takes info from popup spinboxes and calls llcsv function
            def confirm_completion():
                hours = int(hours_spinbox.get())
                minutes = int(minutes_spinbox.get())
                llcsv.task_completed(self.task_id, hours, minutes)
                popup.destroy()
                self.check.config(state = 'active')
                self.progress_bar['value'] = (llcsv.getProgessPerc()) * 100
                self.refresh(self)

            #using a popup for now with the spinboxes
            self.check.config(state = 'disabled')

            popup = tkinter.Toplevel()
            tkinter.Label(popup, text = 'How long did it take to complete this task?').pack()

            #spinbox for hours set up
            tkinter.Label(popup, text="Hours:").pack()
            hours_spinbox = tkinter.Spinbox(popup, from_=0, to=99, width=5,repeatdelay=500, repeatinterval=100, fg="green")
            hours_spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
            hours_spinbox.pack()

            #spinbox for minutes set up
            tkinter.Label(popup, text="Minutes:").pack()
            minutes_spinbox = tkinter.Spinbox(popup, from_=0, to=99, width=5,repeatdelay=500, repeatinterval=100, fg="green")
            minutes_spinbox.config(state="normal", cursor="hand2", bd=3, justify="center", wrap=True)
            minutes_spinbox.pack()

            #when user hits 'ok' button, call the llcsv function to update based on input
            ok_button = tkinter.Button(popup, text="OK", command=confirm_completion)
            ok_button.pack()
        else:
            llcsv.uncomplete_task(self.task_id)
            self.progress_bar['value'] = (llcsv.getProgessPerc()) * 100
            self.refresh(self)
            pass


    #remove_task function
    ''' 
        desc : a simple function that only removes a task, 
        we can call this function in later code
        param : task  
    '''
    def remove_task(self):
        if self.task_id != 0:
            llcsv.remove_task(self.task_id)
            print('task removed')
            # TODO: delete it from owning list in leaplist app
        self.frame.pack_forget()

    def edit_task(self, event):
        self.editing = True
        self.view_task_frame.pack_forget()
        self.add_task_frame.pack(fill = 'both', expand = True)
        pass

    #This is the test function used to prove we can intermingle classes - DAB
    def dontBeAStranger(self):
        print("Hello from the task class!!")

    def addTF(self):
        self.add_task_frame.pack()
        
class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # create canvas widget with background color, no border or highlight
        self.canvas = tkinter.Canvas(self, bg = '#8e9294', highlightthickness = 0, bd = 0)
        self.canvas.pack(side = 'left', fill = 'both', expand = True)

        # create scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient = 'vertical', command = self.canvas.yview)

        # attach scrollbar to canvas
        self.canvas.configure(yscrollcommand = self.scrollbar.set)

        # create scrollable frame inside canvas to hold widgets
        self.scrollable_frame = ttk.Frame(self.canvas, style = 'LeapList.TFrame')
        self.canvas_frame = self.canvas.create_window((0, 0), window = self.scrollable_frame, anchor = 'nw')

        # set scrollable frame background
        style = ttk.Style()
        style.configure("LeapList.TFrame", background = '#8e9294')
        self.canvas.bind('<Configure>', self._resize_scrollable_frame)
        self.canvas.event_generate("<Configure>")
        
        self.opened = False
    
    def bind_events(self):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.scrollable_frame.bind('<Configure>', self._update_scrollregion)
        self.canvas.bind('<Configure>', self._resize_scrollable_frame)

    def unbind_events(self):
        self.canvas.unbind('<MouseWheel>')
        self.scrollable_frame.unbind('<Configure>')
        self.canvas.unbind('<Configure>')

    # handle mouse wheel scrolling
    def _on_mousewheel(self, event):
        # only able to scroll if content exceeds canvas height
        canvas_height = self.canvas.winfo_height()
        content_height = self.canvas.bbox('all')[3] # bottom of the bounding box

        if content_height > canvas_height:
            if event.delta < 0:
                self.canvas.yview_scroll(1, 'units')
            elif event.delta > 0:
                self.canvas.yview_scroll(-1, 'units')

    # update scroll region of canvas when frame size changes
    def _update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.toggle_scrollbar()

    # resize the scrollable frame to match the canvas width
    def _resize_scrollable_frame(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
        
    # toggle visibility of scrollbar based on content height
    def toggle_scrollbar(self):
        # get height of canvas and content in frame
        canvas_height = self.canvas.winfo_height()
        content_height = self.canvas.bbox('all')[3] # bottom of the bounding box

        if content_height > canvas_height:
            self.scrollbar.pack(side = 'right', fill = 'y')
        else:
            self.scrollbar.pack_forget()

class LeapList(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.daily = None
        self.start_date = None
        self.end_date = None
        self.month = None

        # create window
        self.title('LeapList')
        self.resizable(False, False)
        self.geometry('1275x720')
        self.config(bg = '#fff')
        self.enter_task_frame = None
        
        self.style = ttk.Style()
        # self.style.configure('Sidebar.TLabel', foreground = '#aaa', background = '#605d60')
        self.style.configure('Selected.TLabel', foreground = '#fff', background = '#605d60')
        self.style.configure('AddButton.TButton', padding = (5, 5, 5, 5), background = '#363237')
        self.style.configure('TaskButton.TButton', padding = (5, 5, 5, 5), background = '#605d60')

        #### TOPBAR ####

        # import logo png
        self.logo = Image.open('logo.png')
        self.logo_photo = ImageTk.PhotoImage(self.logo)

        # create top bar frame
        self.top_bar = tkinter.Frame(self, bg = '#363237', relief = "sunken", width = 1275, height = 60)
        self.top_bar.pack(ipady = 15)

        # create logo
        self.logo_label = tkinter.Label(self.top_bar, image = self.logo_photo, bg = '#363237', cursor = 'hand2')
        self.logo_label.place(x = 15, y = 15)
        self.logo_label.bind("<Button-1>", self.on_logo_click)

        #### SIDEBAR ####

        # create sidebar frame
        self.sidebar = tkinter.Frame(self, bg = '#605d60', width = 30, height = 690)
        self.sidebar.pack(side = 'left', fill = 'both')

        # create today button
        self.today_button = tkinter.Label(self.sidebar, text = 'Today', font = ('Arial', 30), foreground = '#fff', background = '#605d60', cursor = 'hand2', justify = 'left')
        self.today_button.pack(padx = 15, pady = 15, anchor = 'w')
        self.today_button.bind('<Button-1>', self.open_today)
        self.selected_button = self.today_button

        # create upcoming button
        self.upcoming_button = tkinter.Label(self.sidebar, text = 'Upcoming', font = ('Arial', 30), foreground = '#aaa', background = '#605d60', cursor = 'hand2', justify = 'left')
        self.upcoming_button.pack(padx = 15, pady = 15, anchor = 'w')
        self.upcoming_button.bind('<Button-1>', self.open_upcoming)

        # create completed button
        self.completed_button = tkinter.Label(self.sidebar, text = 'Completed', font = ('Arial', 30), foreground = '#aaa', background = '#605d60', cursor = 'hand2', justify = 'left')
        self.completed_button.pack(padx = 15, pady = 15, anchor = 'w')
        self.completed_button.bind('<Button-1>', self.open_completed)

        # create productivity button
        self.productivity_button = tkinter.Label(self.sidebar, text = 'Productivity', font = ('Arial', 30), foreground = '#aaa', background = '#605d60', cursor = 'hand2', justify = 'left')
        self.productivity_button.pack(padx = 15, pady = 15, anchor = 'w')
        self.productivity_button.bind('<Button-1>', self.open_productivity)

        # create quit button -- TODO move this somewhere else
        self.quit_button = tkinter.Label(self.sidebar, text = 'Quit', font = ('Arial', 30), foreground = '#aaa', background = '#605d60', cursor = 'hand2', justify = 'left')
        self.quit_button.pack(padx = 15, pady = 15, anchor = 'w')
        self.quit_button.bind('<Button-1>', self.quit)

        #### CONTENT | code for frames ####  
        # create footer frame (non-scrollable area)
        self.footer = tkinter.Frame(self, background = '#363237')
        self.footer.pack(side = 'bottom', fill = 'x')

        #Progress bar child to footer - DAB
        self.footer.progress_label = tkinter.Label(self.footer, text = 'Progress:', foreground = '#fff', bg = '#363237', font = ('Arial', 12))
        self.footer.progress_label.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.footer.progress = ttk.Progressbar(self.footer, orient = 'horizontal', length = 300, mode = 'determinate')
        self.footer.progress.grid(column = 2, row = 0, padx = 4, pady = 10)
        self.footer.progress['value'] = (llcsv.getProgessPerc()) * 100
        
        # today frame
        self.today = ScrollableFrame(self)
        self.today.pack(fill = 'both', expand = True)
        self.today_label = tkinter.Label(self.today.scrollable_frame, text = 'Today', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.today_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        self.current_frame = self.today

        # upcoming frame
        self.upcoming = ScrollableFrame(self)
        self.upcoming_label = tkinter.Label(self.upcoming.scrollable_frame, text = 'Upcoming', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.upcoming_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # completed frame
        self.completed = ScrollableFrame(self)
        self.completed_label = tkinter.Label(self.completed.scrollable_frame, text = 'Completed', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.completed_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # productivity frame
        self.productivity = ScrollableFrame(self)
        self.productivity_label = tkinter.Label(self.productivity.scrollable_frame, text = 'Productivity', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.productivity_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # productivity dropdown for time range
        self.productivity_dropdown_time_range = tkinter.Label(self.productivity.scrollable_frame, text = 'Select Time Range', foreground = '#fff', bg = '#8e9294', font = ('Arial', 15))
        self.productivity_dropdown_time_range.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        self.time_dropdown = ttk.Combobox(self.productivity.scrollable_frame, values = ['Today', 'This Month', 'Custom'], state = 'readonly')
        self.time_dropdown.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        self.time_dropdown.set("Today")

        #producitivy dropdown for task tags
        self.productivity_dropdown_tags = tkinter.Label(self.productivity.scrollable_frame, text = 'Select Tag', foreground = '#fff', bg = '#8e9294', font = ('Arial', 15))
        self.productivity_dropdown_tags.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        tags = ["None"] + llcsv.get_all_tags()
        self.tags_dropdown = ttk.Combobox(self.productivity.scrollable_frame, values = tags, state = 'readonly')
        self.tags_dropdown.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        self.tags_dropdown.set("None")

        #productivity checkbox for time to complete tasks
        self.productivity_checkbox_var = tkinter.BooleanVar(value=False)
        self.productivity_checkbox = tkinter.Checkbutton(self.productivity.scrollable_frame, text = 'Include Time to Complete Tasks in Productivity Visualization?', variable= self.productivity_checkbox_var, font = ('Arial', 15), foreground = '#fff', bg = '#8e9294', cursor = 'hand2')
        self.productivity_checkbox.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        #Create Visualization Button
        self.create_visualization_button = ttk.Button(self.productivity.scrollable_frame, text = 'Create Visualization', command = self.productivity_visualization, style = 'AddButton.TButton', cursor = 'hand2', width = 20)
        self.create_visualization_button.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        #Get the user selections
        self.time_dropdown.bind("<<ComboboxSelected>>", self.get_time_dropdown_selection)

        # add task button
        self.add_task_button = ttk.Button(self.footer, text = 'Add Task', command = self.add_task, style = 'AddButton.TButton', cursor = 'hand2', width = 20)
        self.add_task_button.grid(column = 0, row = 0, padx = 10, pady = 10)

        # # completed task -- TODO repurpose
        #     # you need a frame
        # self.remove_task_frame = tkinter.Frame(self.footer, bg = '#363237')
        # self.remove_task_frame.pack()
        #     # a button
        # self.remove_task_button = ttk.Button(self.remove_task_frame, text = 'Remove Task', command = self.remove_task, style = 'Remove.TButton', state = 'disabled', cursor = 'arrow', width = 20)
        # self.remove_task_button.grid(column = 4, row = 0, padx = (0, 10), pady = 10)

        self.q_today()
        self.q_upcoming()
        self.q_complete()

        self.task = Task()

    #This probably needs some work to make sure it's communicating with the plot func correctly
    #I think the custom date range is broken
    def get_time_dropdown_selection(self, event):
        #grab the selection
        selected_option = self.time_dropdown.get()
        #if today, currently setting daily to true
        if selected_option == "Today":
            self.start_date = None
            self.end_date = None
            self.month = None
            self.daily = True
        #if this month, currently setting month to true
        elif selected_option == "This Month":
            self.start_date = None
            self.end_date = None
            self.daily = None
            self.month = True
        #if custom, calls function to bring up popup for calendar selection
        elif selected_option == "Custom":
            self.daily = None
            self.month = None
            self.calendar_for_productivity()

    #This function is called when the user selects custom date range
    #it creates a calendar popup for the user to set the start and end date
    #you have to bring up calendar, hit set start date, then bring up calendar again and set end date
    def calendar_for_productivity(self):
        def set_start_date():
            self.start_date = self.calendar.get_date()
            self.calendar_popup.destroy()

        def set_end_date():
            self.end_date = self.calendar.get_date()
            self.calendar_popup.destroy()

        self.calendar_popup = tkinter.Toplevel()
        self.calendar = Calendar(self.calendar_popup, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack()

        ttk.Button(self.calendar_popup, text='Set Start Date', command=set_start_date).pack()
        ttk.Button(self.calendar_popup, text='Set End Date', command=set_end_date).pack()

    #This function is called when the user clicks the create visualization button
    #it gathers all the drop down / check box selections to send to the plot creator
    def productivity_visualization(self):
        tag_id = None if self.tags_dropdown.get() == "None" else self.tags_dropdown.get()
        time_input = self.productivity_checkbox_var.get()

        #saving the returned PNG here, although this might not be the way to do it properly
        productivity_PNG = pCSV.create_productivity(daily=self.daily, start_date=self.start_date,
                                                    end_date=self.end_date, month=self.month, tag_id=tag_id,
                                                    time_input=time_input)

        print("Productivity Visualization Created, now you need to figure out how to display the png")
        #call a function to display the PNG as a popup
        self.visualization_popup(productivity_PNG)

    #This function creates a popup window with the productivity visualization png
    def visualization_popup(self, productivity_PNG):
        popup = tkinter.Toplevel(self)
        popup.title("Productivity Visualization")
        p_image = Image.open(productivity_PNG)
        photo = ImageTk.PhotoImage(p_image)
        #probably change the geometry to be bigger?
        popup.geometry("800x800")
        popup.resizable(False, False)

        label = tkinter.Label(popup, image=photo)
        label.image = photo
        label.pack()

        close_button = ttk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

    #### QUEUE TASKS ####
    def q_today(self):
        self.today_task = llcsv.getTodayTask()
        for task_id in self.today_task:
            tTask = Task(self.today.scrollable_frame, self.footer.progress, task_id, self.refresh)

    def q_complete(self):
        self.completed_task = llcsv.getCompletedTask() #returns a list of strings
        for task_id in self.completed_task: 
            cTask = Task(self.completed.scrollable_frame, self.footer.progress, task_id, self.refresh)

    def q_upcoming(self):
        self.upcoming_tasks = llcsv.getUpcomingTask() #returns a list of strings
        for task_id in self.upcoming_tasks:
            uTask = Task(self.upcoming.scrollable_frame, self.footer.progress, task_id, self.refresh)

    #### SIDEBAR BUTTON COMMANDS ####
    #displays the tasks that are due today in a GUI format
    def open_today(self, event):
        if self.current_frame != self.today:
            self.open_frame(self.today, self.today_button)

    #displays the upcoming tasks (tasks not due today) in a GUI format
    def open_upcoming(self, event):
        if self.current_frame != self.upcoming:
            self.open_frame(self.upcoming, self.upcoming_button)

    #displays the tasks due today
    def open_Dailys(self, event):
        if self.current_frame == self.today:
            self.open_frame(self.today, self.today_button)

    #displays all completed tasks
    def open_completed(self, event):
        if self.current_frame != self.completed:
            self.open_frame(self.completed, self.completed_button)

    #opens productivity frame
    def open_productivity(self, event):
        if self.current_frame != self.productivity:
            self.open_frame(self.productivity, self.productivity_button)

    #general function for opening any frame
    def open_frame(self, frame, button):
        self.current_frame.unbind_events()
        self.current_frame.pack_forget()
        frame.pack(fill = 'both', expand = True)
        self.current_frame = frame
        self.current_frame.bind_events()
        self.selected_button.config(foreground = '#aaa', background = '#605d60')
        self.selected_button = button
        self.selected_button.config(foreground = '#fff', background = '#605d60')

    # quits application
    def quit(self, event):
        self.destroy()

    #progress bar function
    def progress_bar(self):
        self.footer.progress['value'] = (llcsv.getProgessPerc()) * 100

    #adds task
    def add_task(self):
        new_task = Task(self.current_frame.scrollable_frame, self.footer.progress, None, self.refresh)
        self.current_frame.bind_events()
        
    #progress bar function
    def progress_bar(self):
        self.footer.progress['value'] = (llcsv.getProgessPerc()) * 100

    #Just a test, I don't want to make any drastic changes w/o approval -dab
    def hiTaskClass(self):
        self.task.dontBeAStranger()
    
    # runs upon clicking logo (proof of concept for losing the buttons, could be a cool easter egg maybe)
    def on_logo_click(self, event):
        print('clicked me!')
        #plays sound
        #playsound('leapListFS.mp3')
        self.hiTaskClass()

    def refresh(self, task):
        if llcsv.is_completed(task.task_id):
            cTask = Task(self.completed.scrollable_frame, self.footer.progress, task.task_id, self.refresh)
        elif llcsv.is_today(task.task_id):
            tTask = Task(self.today.scrollable_frame, self.footer.progress, task.task_id, self.refresh)
        else:
            uTask = Task(self.upcoming.scrollable_frame, self.footer.progress, task.task_id, self.refresh)
        task.frame.destroy()

# create the application
if __name__ == '__main__':
    LeapList = LeapList()
    LeapList.mainloop()