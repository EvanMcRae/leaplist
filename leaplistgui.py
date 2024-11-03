import tkinter
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import sys
import leaplistcsv as llcsv

# fixes some ugly blurring on windows
if sys.platform == "win32":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

class leaplist():
    def __init__(self):
         # create window
        self.main_window = tkinter.Tk()
        self.main_window.title('LeapList')
        self.main_window.resizable(False, False) # disables resizing
        self.main_window.geometry('1275x720')
        self.main_window.config(bg = '#fff')
        self.enter_task_frame = None
        
        # TODO configure style for sidebar buttons
        self.style = ttk.Style()
        self.style.configure("Sidebar.TButton", anchor="w", padding=(10, 20, 50, 20), background="#605d60")

        #### TOPBAR ####

        # import logo png
        self.logo = Image.open("logo.png")
        self.logo_photo = ImageTk.PhotoImage(self.logo)

        # create top bar frame
        self.top_bar = tkinter.Frame(self.main_window, bg = '#363237', relief = "sunken", width = 1275, height = 60)
        self.top_bar.pack(ipady = 15)

        # create logo
        self.logo_label = tkinter.Label(self.top_bar, image = self.logo_photo, bg = '#363237', cursor = "hand2")
        self.logo_label.place(x = 15, y = 15)
        self.logo_label.bind("<Button-1>", self.on_logo_click) # click handling could be used instead of buttons maybe?

        #### SIDEBAR ####

        # create sidebar frame
        self.sidebar = tkinter.Frame(self.main_window, bg = '#605d60', width = 300, height = 690)
        self.sidebar.pack(side = 'left', fill = 'y')

        # create today button
        self.today_button = ttk.Button(self.sidebar, text = 'Today', width = 30, command = self.today, style="Sidebar.TButton", cursor = "hand2")
        self.today_button.pack(fill = 'x', padx = 15, pady = 15)

        # create upcoming button
        self.upcoming_button = ttk.Button(self.sidebar, text = 'Upcoming', width = 30, command = self.upcoming, style="Sidebar.TButton", cursor = "hand2")
        self.upcoming_button.pack(fill = 'x', padx = 15, pady = 15)

        # create completed button
        self.completed_button = ttk.Button(self.sidebar, text = 'Completed', width = 30, command = self.completed, style="Sidebar.TButton", cursor = "hand2")
        self.completed_button.pack(fill = 'x', padx = 15, pady = 15)

        # create productivity button
        self.productivity_button = ttk.Button(self.sidebar, text = 'Productivity', command = self.productivity, width = 30, style="Sidebar.TButton", cursor = "hand2")
        self.productivity_button.pack(fill = 'x', padx = 15, pady = 15)

        # create quit button -- TODO move this somewhere else
        self.quit_button = ttk.Button(self.sidebar, text = 'Quit (WILL BE MOVED)', command = self.quit, width = 30, style="Sidebar.TButton", cursor = "hand2")
        self.quit_button.pack(fill = 'x', padx = 15, pady = 15)

        #### CONTENT ####

        # content frame (contains all other frames below, allows switching between)
        self.content_frame = tkinter.Frame(self.main_window, bg = '#8e9294', width = 650, height = 690)
        self.content_frame.pack(fill = 'both', expand = True)

        # today frame
        self.today_frame = tkinter.Frame(self.content_frame, bg = '#8e9294', width = 650, height = 690)
        self.today_frame.grid(row=0, column=0, sticky='news')
        self.today_label = tkinter.Label(self.today_frame, text = 'Today', foreground = '#fff', bg = '#8e9294', font=('Arial', 30))
        self.today_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        #adding a frame within today at the bottom to put an add task button
        self.add_task_frame = tkinter.Frame(self.today_frame, bg = '#363237', width = 900, height = 50)
        # I thought side = 'bottom would place it at the bottom, it's not working and I don't know enough yet to fix it
        self.add_task_frame.pack(side = 'bottom', pady = 10)
        #stop the add task frame from resizing with the button
        self.add_task_frame.pack_propagate(False)
        #add task button
        self.add_task_button = ttk.Button(self.add_task_frame, text='Add Task', command=self.enter_task, cursor="hand2")
        self.add_task_button.pack(anchor = 'center', pady = 10)

        # upcoming frame
        self.upcoming_frame = tkinter.Frame(self.content_frame, bg = '#8e9294', width = 650, height = 690)
        self.upcoming_frame.grid(row=0, column=0, sticky='news')
        self.upcoming_label = tkinter.Label(self.upcoming_frame, text = 'Upcoming', foreground = '#fff', bg = '#8e9294', font=('Arial', 30))
        self.upcoming_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # completed frame
        self.completed_frame = tkinter.Frame(self.content_frame, bg = '#8e9294', width = 650, height = 690)
        self.completed_frame.grid(row=0, column=0, sticky='news')
        self.completed_label = tkinter.Label(self.completed_frame, text = 'Completed', foreground = '#fff', bg = '#8e9294', font=('Arial', 30))
        self.completed_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # productivity frame
        self.productivity_frame = tkinter.Frame(self.content_frame, bg = '#8e9294', width = 650, height = 690)
        self.productivity_frame.grid(row=0, column=0, sticky='news')
        self.productivity_label = tkinter.Label(self.productivity_frame, text = 'Productivity', foreground = '#fff', bg = '#8e9294', font=('Arial', 30))
        self.productivity_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # show today frame first
        self.today_frame.tkraise()

        # activate application
        self.main_window.mainloop()

    #### SIDEBAR BUTTON COMMANDS ####

    # opens today frame
    def today(self):
        self.today_frame.tkraise()

    # opens upcoming frame
    def upcoming(self):
        self.upcoming_frame.tkraise()

    # opens completed frame
    def completed(self):
        self.completed_frame.tkraise()

    # opens productivity frame
    def productivity(self):
        self.productivity_frame.tkraise()

    # quits application
    def quit(self):
        self.main_window.destroy()

    #brings up a box to add a task and notes if wanted
    def enter_task(self):
        #if there's already a task entry box open, don't open another
        if self.enter_task_frame:
            return

        #I still need to create the GUI for the actual input
        #Then it will save via the llcsv save_task function


    # runs upon clicking logo (proof of concept for losing the buttons, could be a cool easter egg maybe)
    def on_logo_click(self, event):
        print('clicked me!')

# create the application
LeapList = leaplist()