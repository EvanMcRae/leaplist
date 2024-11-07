import tkinter
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sys
import leaplistcsv as llcsv

# fixes some ugly blurring on windows
# if sys.platform == "win32":
#     from ctypes import windll
#     windll.shcore.SetProcessDpiAwareness(1)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, bg_color = '#8e9294'):
        super().__init__(container)

        # create frame for scrollable content
        content_frame = ttk.Frame(self)
        content_frame.pack(side = 'top', fill = 'both', expand = True)

        # create canvas widget with background color, no border or highlight
        canvas = tkinter.Canvas(content_frame, bg = bg_color, highlightthickness = 0, bd = 0)
        scrollbar = ttk.Scrollbar(content_frame, orient = 'vertical', command = canvas.yview)

        # create scrollable frame inside canvas to hold widgets
        scrollable_frame = ttk.Frame(canvas, style = 'LeapList.TFrame')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        # create window inside canvas to hold scrollable frame
        self.scrollable_window = canvas.create_window((0, 0), window = scrollable_frame, anchor = 'nw')

        # set yscrollcommand to connect canvas with scrollbar
        canvas.configure(yscrollcommand = scrollbar.set)

        # pack canvas and scrollbar
        canvas.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')

        # set scrollable frame as class attribute to add widgets later
        self.scrollable_frame = scrollable_frame

        # set scrollable frame background
        style = ttk.Style()
        style.configure("LeapList.TFrame", background = bg_color)

class LeapList():
    def __init__(self):
         # create window
        self.main_window = tkinter.Tk()
        self.main_window.title('LeapList')
        self.main_window.resizable(False, False)
        self.main_window.geometry('1275x720')
        self.main_window.config(bg = '#fff')
        self.enter_task_frame = None
        
        self.style = ttk.Style()
        self.style.configure('Sidebar.TLabel', foreground = '#aaa', background = '#605d60')
        self.style.configure('Selected.TLabel', foreground = '#fff', background = '#605d60')
        self.style.configure('AddButton.TButton', padding = (5, 5, 5, 5), background = '#363237')

        #### TOPBAR ####

        # import logo png
        self.logo = Image.open("logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo)

        # create top bar frame
        self.top_bar = tkinter.Frame(self.main_window, bg = '#363237', relief = "sunken", width = 1275, height = 60)
        self.top_bar.pack(ipady = 15)

        # create logo
        self.logo_label = tkinter.Label(self.top_bar, image = self.logo_photo, bg = '#363237', cursor = 'hand2')
        self.logo_label.place(x = 15, y = 15)
        self.logo_label.bind("<Button-1>", self.on_logo_click)

        #### SIDEBAR ####

        # create sidebar frame
        self.sidebar = tkinter.Frame(self.main_window, bg = '#605d60', width = 30, height = 690)
        self.sidebar.pack(side = 'left', fill = 'both')

        # create today button
        self.today_button = ttk.Label(self.sidebar, text = 'Today', font = ('Arial', 30), style = 'Selected.TLabel', cursor = 'hand2')
        self.today_button.pack(fill = 'x', padx = 15, pady = 15)
        self.today_button.bind('<Button-1>', self.open_today)
        self.selected_button = self.today_button

        # create upcoming button
        self.upcoming_button = ttk.Label(self.sidebar, text = 'Upcoming', font = ('Arial', 30), style = 'Sidebar.TLabel', cursor = 'hand2')
        self.upcoming_button.pack(fill = 'x', padx = 15, pady = 15)
        self.upcoming_button.bind('<Button-1>', self.open_upcoming)

        # create completed button
        self.completed_button = ttk.Label(self.sidebar, text = 'Completed', font = ('Arial', 30), style = 'Sidebar.TLabel', cursor = 'hand2')
        self.completed_button.pack(fill = 'x', padx = 15, pady = 15)
        self.completed_button.bind('<Button-1>', self.open_completed)

        # create productivity button
        self.productivity_button = ttk.Label(self.sidebar, text = 'Productivity', font = ('Arial', 30), style = 'Sidebar.TLabel', cursor = 'hand2')
        self.productivity_button.pack(fill = 'x', padx = 15, pady = 15)
        self.productivity_button.bind('<Button-1>', self.open_productivity)

        # create quit button -- TODO move this somewhere else
        self.quit_button = ttk.Label(self.sidebar, text = 'Quit', font = ('Arial', 30), style = 'Sidebar.TLabel', cursor = 'hand2')
        self.quit_button.pack(fill = 'x', padx = 15, pady = 15)
        self.quit_button.bind('<Button-1>', self.quit)

        #### CONTENT ####
        # content frame (contains all other frames below, allows switching between)
        self.content_frame = tkinter.Frame(self.main_window, bg = '#8e9294', width = 650, height = 690)
        self.content_frame.pack(fill = 'both', expand = True)
        
        # create footer frame (non-scrollable area)
        self.footer = tkinter.Frame(self.content_frame, background = '#363237')
        self.footer.pack(side = 'bottom', fill = 'x')

        # today frame
        self.today = ScrollableFrame(self.content_frame)
        self.today.pack(fill="both", expand=True)
        self.today_label = tkinter.Label(self.today.scrollable_frame, text = 'Today', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.today_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        self.current_frame = self.today

        # upcoming frame
        self.upcoming = ScrollableFrame(self.content_frame)
        self.upcoming_label = tkinter.Label(self.upcoming.scrollable_frame, text = 'Upcoming', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.upcoming_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # completed frame
        self.completed = ScrollableFrame(self.content_frame)
        self.completed_label = tkinter.Label(self.completed.scrollable_frame, text = 'Completed', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.completed_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # productivity frame
        self.productivity = ScrollableFrame(self.content_frame)
        self.productivity_label = tkinter.Label(self.productivity.scrollable_frame, text = 'Productivity', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.productivity_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        
        # add task frame
        self.add_task_frame = tkinter.Frame(self.footer, bg = '#363237')
        self.add_task_frame.pack()

        # user input
        self.user_entry = tkinter.Entry(self.add_task_frame)
        self.user_entry.config(font=('Comic Sans MS', 15))

        # hexadecimal for font color
        self.user_entry.config(bg='#fff')
        self.user_entry.config(fg='#00ff00')

        #We can always disable the text box when we don't want users to type anything.
        #self.user_entry.config(state= 'disabled')

        #does not limit amount of characters passed; limits amount of characters displayed
        self.user_entry.config(width=25)
        self.user_entry.grid(column = 0, row = 0 , padx = (10, 10), pady = 10)
        self.user_entry.focus_set()

        # add task button
        self.add_task_button = ttk.Button(self.add_task_frame, text = 'Add Task', command = self.enter_task, style = 'AddButton.TButton', cursor = 'hand2')
        self.add_task_button.grid(column = 1, row = 0, padx = (0, 10), pady = 10)

        # tasks lists
        self.today_tasks = []
        self.upcoming_tasks = []

        # activate application
        self.main_window.mainloop()

    #### SIDEBAR BUTTON COMMANDS ####
    def open_today(self, event):
        if self.current_frame != self.today:
            self.open_frame(self.today, self.today_button)
            self.add_task_frame.pack()

    def open_upcoming(self, event):
        if self.current_frame != self.upcoming:
            self.open_frame(self.upcoming, self.upcoming_button)
            self.add_task_frame.pack()
            

    def open_completed(self, event):
        if self.current_frame != self.completed:
            self.open_frame(self.completed, self.completed_button)
            self.add_task_frame.pack_forget()

    def open_productivity(self, event):
        if self.current_frame != self.productivity:
            self.open_frame(self.productivity, self.productivity_button)
            self.add_task_frame.pack_forget()

    def open_frame(self, frame, button):
        self.current_frame.pack_forget()
        frame.pack(fill="both", expand=True)
        self.current_frame = frame
        self.selected_button.config(style = 'Sidebar.TLabel')
        self.selected_button = button
        self.selected_button.config(style = 'Selected.TLabel')

    # quits application
    def quit(self, event):
        self.main_window.destroy()

    #brings up a box to add a task and notes if wanted
    def enter_task(self):
        #testing something out for userinput -DAB
        #retrieve text from user entry
        task = self.user_entry.get()
        #printing for proof of concept
        print(task)

        #test call to function in csv.py
        llcsv.new_task(task, task, 1, 2, 3, task)

        # TODO: Only add to one of these based on date
        today_label = tkinter.Label(self.today.scrollable_frame, text = task, fg = 'green', bg = '#8e9294', font = ('Arial', '20'))
        today_label.pack(fill = 'none', expand = False, side = 'top', anchor = 'w', ipadx = 15)
        self.today_tasks.append(today_label)

        upcoming_label = tkinter.Label(self.upcoming.scrollable_frame, text = task, fg = 'green', bg = '#8e9294', font = ('Arial', '20'))
        upcoming_label.pack(fill = 'none', expand = False, side = 'top', anchor = 'w', ipadx = 15)
        self.upcoming_tasks.append(upcoming_label)

        # TODO: Is this still how we want to do things? To discuss tomorrow
        #if there's already a task entry box open, don't open another
        if self.enter_task_frame:
            return

        #I still need to create the GUI for the actual input
        #Then it will save via the llcsv save_task function

    # runs upon clicking logo (proof of concept for losing the buttons, could be a cool easter egg maybe)
    def on_logo_click(self, event):
        print('clicked me!')



# create the application
LeapList = LeapList()