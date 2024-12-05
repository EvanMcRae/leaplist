import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import ImageTk, Image
import os
import sys
import leaplistcsv as llcsv
import plotCSV as pCSV
import math
import datetime as dt
from datetime import datetime, timedelta
from tkcalendar import Calendar, DateEntry
from babel.dates import format_timedelta

if sys.platform == "win32":
    from playsound import playsound
elif sys.platform == "darwin":
    # TODO add different playsound package here for macos
    pass

# SOURCE: https://stackoverflow.com/questions/72102048/is-there-a-way-to-have-the-date-entry-calendar-show-up-in-a-blank-date-entry-fie
class CustomDateEntry(DateEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_parse_date = self.parse_date
        self.parse_date = self.new_parse_date
        
    def _validate_date(self):
        if not self.get():
            return True
        return super()._validate_date()

    def new_parse_date(self, text):
        if not text:
            return datetime.now() # return some default date
        return self.old_parse_date(text) # runs original function

class Task():
    def __init__(self, parent_frame=None, progress_bar=None, task_id=None, refresh=None, get_tags=None, new_upcoming=False):
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

            if not new_upcoming:
                self.work_date = datetime.now().strftime('%Y-%m-%d')
            else:
                self.work_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            self.deadline = None

            self.description = ""
            self.tags = ""
            self.priority = ""

            self.refresh = refresh
            self.get_tags = get_tags

            self.add_task_frame.left = tkinter.Frame(self.add_task_frame, bg = '#605d60')
            self.add_task_frame.left.grid(column = 0, row = 0, sticky = 'w')
            self.add_task_frame.right = tkinter.Frame(self.add_task_frame, bg = '#605d60')
            self.add_task_frame.right.grid(column = 1, row = 0, sticky = 'w')

            # task name input
            self.task_name_label = tkinter.Label(self.add_task_frame.left, fg = '#fff', bg = '#605d60', text = 'Name: ', font = ('Arial', 15), justify = 'left')
            self.task_name_label.grid(column = 0, row = 0, padx = (10, 10), pady = 10, sticky = 'w')
            self.task_name_entry = tkinter.Entry(self.add_task_frame.left, bg = '#fff', fg = '#000', font = ('Arial', 15), width = 25, justify = 'left')
            self.task_name_entry.grid(column = 1, row = 0, padx = (10, 10), pady = 10, sticky = 'w', columnspan = 2)
            self.task_name_entry.focus_set()
            self.task_name_entry.bind("<KeyRelease>", self.on_type)

            # add deadline entry
            self.deadline_label = tkinter.Label(self.add_task_frame.left, fg = '#fff', bg = '#605d60', text = 'Deadline: ', font = ('Arial', 15), justify = 'left')
            self.deadline_label.grid(column = 0, row = 1 , padx = (10, 10), pady = 10, sticky = 'w')
            self.deadline_entry = CustomDateEntry(self.add_task_frame.left, selectmode='day', mindate=datetime.now(), font = ('Arial', 15), showweeknumbers=False, justify = 'left')
            if sys.platform == "darwin":
                self.deadline_entry._top_cal.overrideredirect(False) # @Olivia does this help?
            self.deadline_entry.grid(column = 1, row = 1, padx = (10, 10), pady = 10, sticky = 'w')
            self.deadline_entry.delete(0, "end")
            self.deadline_reset_button = ttk.Button(self.add_task_frame.left, text = 'Reset', command = self.reset_deadline, style = 'TaskButton.TButton', cursor = 'hand2')
            self.deadline_reset_button.grid(column = 2, row = 1, padx = (5, 0), ipadx = 10, pady = 10, sticky = 'w')

            # add work date entry
            self.work_date_label = tkinter.Label(self.add_task_frame.left, fg = '#fff', bg = '#605d60', text = 'Work Date: ', font = ('Arial', 15), justify = 'left')
            self.work_date_label.grid(column = 0, row = 2, padx = (10, 10), pady = 10, sticky = 'w')
            self.work_date_entry = DateEntry(self.add_task_frame.left, selectmode='day', mindate=datetime.now(), font = ('Arial', 15), showweeknumbers=False, justify = 'left')
            if sys.platform == "darwin":
                self.work_date_entry._top_cal.overrideredirect(False) # @Olivia does this help?
            self.work_date_entry.grid(column = 1, row = 2, padx = (10, 10), pady = 10, sticky = 'w')
            if new_upcoming:
                self.work_date_entry.set_date(datetime.now() + timedelta(days=1))

            self.work_date_reset_button = ttk.Button(self.add_task_frame.left, text = 'Reset', command = self.reset_work_date, style = 'TaskButton.TButton', cursor = 'hand2')
            self.work_date_reset_button.grid(column = 2, row = 2, padx = (5, 0), ipadx = 10, pady = 10, sticky = 'w')

            # description input
            self.description_label = tkinter.Label(self.add_task_frame.right, fg = '#fff', bg = '#605d60', text = 'Description: ', font = ('Arial', 15), justify = 'left')
            self.description_label.grid(column = 0, row = 0, padx = (10, 10), pady = 10, sticky = 'w')
            self.description_entry = scrolledtext.ScrolledText(self.add_task_frame.right, bg = '#fff', fg = '#000', font = ('Arial', 15), width = 46, height = 8)
            self.description_entry.grid(column = 0, row = 1, padx = (10, 10), pady = 10, sticky = 'w', columnspan = 2)

            # tags input
            self.tags_label = tkinter.Label(self.add_task_frame.left, fg = '#fff', bg = '#605d60', text = 'Tag: ', font = ('Arial', 15), justify = 'left')
            self.tags_label.grid(column = 0, row = 3, padx = (10, 10), pady = 10, sticky = 'w')
            self.tags_entry = tkinter.Entry(self.add_task_frame.left, bg = '#fff', fg = '#000', font = ('Arial', 15), width = 25, justify = 'left')
            self.tags_entry.grid(column = 1, row = 3, padx = (10, 10), pady = 10, sticky = 'w', columnspan = 2)

            self.save_button = ttk.Button(self.add_task_frame.left, text = 'Save', command = self.save_task, style = 'TaskButton.TButton', cursor = 'arrow', state = 'disabled')
            self.save_button.grid(column = 0, row = 4, padx = (10, 0), ipadx = 10, pady = 10, sticky = 'w')

            self.cancel_button = ttk.Button(self.add_task_frame.left, text = 'Cancel', command = self.cancel_edit, style = 'TaskButton.TButton', cursor = 'hand2', state = 'enabled')

            self.remove_button = ttk.Button(self.add_task_frame.left, text = 'Remove', command = self.remove_task, style = 'TaskButton.TButton', cursor = 'hand2', state = 'enabled')
            self.remove_button.grid(column = 2, row = 4, padx = (5, 0), ipadx = 10, pady = 10, sticky = 'w')

            #### VIEW TASK FRAME
            self.view_task_frame = tkinter.Frame(self.frame, bg = '#605d60')
            
            # Creating a check mark widget. When clicked, it will mark task as completed - DAB
            self.check = tkinter.Checkbutton(self.view_task_frame, onvalue = 1, offvalue = 0, variable = self.completed, command = self.complete_task, bg = '#605d60', activebackground = '#605d60')
            self.check.grid(column = 0, row = 0, padx = (10, 0))

            self.label = tkinter.Label(self.view_task_frame, fg = '#fff', bg = '#605d60', font = ('Arial', 20), width = 48, justify = 'left', anchor = 'w')
            self.label.grid(column = 1, row = 0, ipadx = 20, sticky = 'w')
            self.view_task_frame.bind('<Double-Button-1>', self.edit_task)
            self.label.bind('<Double-Button-1>', self.edit_task)

            self.view_task_frame.tag = tkinter.Label(self.view_task_frame, fg = '#ccc', bg = '#605d60', text = 'Tag: ', font = ('Arial', 15), justify = 'left', anchor = 'w')
            self.view_task_frame.tag.grid(column = 1, row = 1, ipadx = 20, sticky = 'w')

            self.view_task_frame.deadline_label = tkinter.Label(self.view_task_frame, fg = '#fff', bg = '#605d60', text = 'Deadline', font = ('Arial', 20), justify = 'left')
            self.view_task_frame.deadline_label.grid(column = 2, row = 0, sticky = 'w')

            self.view_task_frame.deadline = tkinter.Label(self.view_task_frame, fg = '#ccc', bg = '#605d60', text = 'Deadline', font = ('Arial', 15), justify = 'left')
            self.view_task_frame.deadline.grid(column = 2, row = 1, sticky = 'w')

            #### Upon task refresh from CSV
            if task_id != None:
                self.task_id = task_id
                # Only do this if the task was saved in the first place
                self.cancel_button.grid(column = 1, row = 4, padx = (30, 0), ipadx = 10, pady = 10, sticky = 'w')
                self.repopulate_data()
            else:
                self.remove_button.config(text = 'Cancel')
                self.add_task_frame.pack(expand = True, fill = 'both')
    
    def repopulate_data(self):
        task_name = llcsv.get_task_name(self.task_id)
        self.label.config(text = task_name)
        self.task_name_entry.delete(0, "end")
        self.task_name_entry.insert(0, task_name)
        if len(str(task_name)) > 0:
            self.save_button.config(state = 'normal')
            self.save_button.config(cursor = 'hand2')
        
        self.deadline = llcsv.get_deadline(self.task_id)
        self.view_task_frame.deadline.config(text = 'None')
        try:
            self.deadline_entry.set_date(datetime.strptime(self.deadline, '%Y-%m-%d'))
            time_difference = datetime.strptime(self.deadline, '%Y-%m-%d').date() - datetime.now().date()
            relative_deadline = format_timedelta(time_difference, locale='en_US')
            if relative_deadline == '0 seconds':
                self.view_task_frame.deadline.config(text = 'Today')
            elif time_difference < timedelta(0):
                self.view_task_frame.deadline.config(text = relative_deadline + ' ago')
            else:
                self.view_task_frame.deadline.config(text = relative_deadline)

        except TypeError:
            self.deadline_entry.delete(0, "end")
        except ValueError:
            self.deadline_entry.delete(0, "end")

        self.work_date = llcsv.get_work_date(self.task_id)
        self.work_date_entry.set_date(datetime.strptime(self.work_date, '%Y-%m-%d'))
        
        self.tags = llcsv.get_tags(self.task_id)
        self.view_task_frame.tag.config(text = "Untagged")
        try:
            if math.isnan(self.tags):
                self.tags = ""
        except TypeError:
            pass
        finally:
            self.tags_entry.delete(0, 'end')
            self.tags_entry.insert(0, self.tags)
            if len(self.tags) > 0:
                self.view_task_frame.tag.config(text = "Tag: " + self.tags)

        self.description = llcsv.get_description(self.task_id)
        try:
            if math.isnan(self.description):
                self.description = ""
        except TypeError:
            pass
        finally:
            self.description_entry.delete('1.0', 'end')
            self.description_entry.insert('1.0', self.description)
            
        self.priority = llcsv.get_priority(self.task_id) # TODO

        if llcsv.is_completed(self.task_id):
            self.check.config(state = 'normal')
            self.check.select()

        self.view_task_frame.pack(fill = 'both', expand = True)

    #functions for entering data
    def on_type(self, event):
        if len(self.task_name_entry.get()) > 0:
            self.save_button.config(state = 'normal')
            self.save_button.config(cursor = 'hand2')
        else:
            self.save_button.config(state = 'disabled')
            self.save_button.config(cursor = 'arrow')

    def reset_work_date(self):
        self.work_date_entry.set_date(datetime.now())

    def reset_deadline(self):
        self.deadline_entry.delete(0, "end")

    def cancel_edit(self):
        self.editing = False
        self.add_task_frame.pack_forget()
        self.repopulate_data()

    #brings up a box to add a task and notes if wanted
    def save_task(self):
        self.editing = False

        self.description = self.description_entry.get('1.0', tkinter.END)
        self.priority = "" # TODO
        self.tags = self.tags_entry.get()
        
        # self.deadline = ""
        self.deadline = self.deadline_entry.get_date()
        self.work_date = self.work_date_entry.get_date()

        #retrieve text from user entry
        task = self.task_name_entry.get()
        
        #test call to function in csv.py
        if (self.task_id == 0):   
            self.task_id = llcsv.new_task(task, self.description, self.work_date, self.deadline, self.priority, self.tags)
            self.progress_bar['value'] = (llcsv.getProgessPerc()) * 100
        else:
            llcsv.edit_task(self.task_id, task, self.description, self.work_date, self.deadline, self.priority, self.tags)
        
        self.refresh(self)
        self.get_tags()
    
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
        self.frame.pack_forget()
        self.get_tags()

    def edit_task(self, event):
        if not llcsv.is_completed(self.task_id):
            self.editing = True
            self.view_task_frame.pack_forget()
            self.add_task_frame.pack(fill = 'both', expand = True)

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
        self.scrollbar.pack(side = 'right', fill = 'y')

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
        # get widget under cursor
        try:
            widget_under_cursor = self.canvas.winfo_containing(self.canvas.winfo_pointerx(), self.canvas.winfo_pointery())
        except KeyError:
            return

        # if mouse is over a scrollable ScrolledText widget, do not apply canvas scroll
        if isinstance(widget_under_cursor, scrolledtext.ScrolledText):
            yview = widget_under_cursor.yview()
            if not (yview[0] == 0.0 and yview[1] == 1.0): # if content is not fully visible
                return
        
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
        # self.toggle_scrollbar()

    # resize the scrollable frame to match the canvas width
    def _resize_scrollable_frame(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
        
    # toggle visibility of scrollbar based on content height -- UNUSED
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
        self.style.configure('MainPage.TButton', padding = (5, 5, 5, 5), background = '#8e9294')
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

        # create settings button
        self.settings_button = tkinter.Label(self.sidebar, text = 'Settings', font = ('Arial', 30), foreground = '#aaa', background = '#605d60', cursor = 'hand2', justify = 'left')
        self.settings_button.pack(padx = 15, pady = 15, anchor = 'w')
        self.settings_button.bind('<Button-1>', self.open_settings)

        # create quit button
        self.quit_button = tkinter.Label(self.top_bar, text = '×', font = ('Arial', 45), foreground = '#aaa', background = '#363237', cursor = 'hand2')
        self.quit_button.place(x = 1210, y = 10)
        self.quit_button.bind('<Button-1>', self.quit)
        self.quit_button.bind('<Enter>', lambda event: change_color(self.quit_button, "white"))
        self.quit_button.bind('<Leave>', lambda event: change_color(self.quit_button, "#aaa"))

        #### CONTENT | code for frames ####  
        # create footer frame (non-scrollable area)
        self.footer = tkinter.Frame(self, background = '#363237')
        self.footer.pack(side = 'bottom', fill = 'x')
        self.footer.inner = tkinter.Frame(self.footer, background='#363237')
        self.footer.inner.pack(expand=True) 

        #Progress bar child to footer - DAB
        self.footer.progress_label = tkinter.Label(self.footer.inner, text = 'Today\'s Progress:', foreground = '#fff', bg = '#363237', font = ('Arial', 12))
        self.footer.progress_label.pack(side = 'left', padx = (0, 10), pady = 10)
        self.footer.progress = ttk.Progressbar(self.footer.inner, orient = 'horizontal', length = 500, mode = 'determinate')
        self.footer.progress.pack(side = 'left', pady = 10)
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
        self.time_dropdown = ttk.Combobox(self.productivity.scrollable_frame, values = ['None', 'Today', 'This Month', 'Custom'], state = 'readonly')
        self.time_dropdown.pack(padx = (15, 0), ipadx = 15, ipady = 15, anchor = 'nw')
        self.time_dropdown.set("None")

        #productivity dropdown for task tags
        self.productivity_dropdown_tags = tkinter.Label(self.productivity.scrollable_frame, text = 'Select Tag (Optional)', foreground = '#fff', bg = '#8e9294', font = ('Arial', 15))
        self.productivity_dropdown_tags.pack(ipadx = 15, ipady = 15, anchor = 'nw')
        self.tags_dropdown = ttk.Combobox(self.productivity.scrollable_frame, state = 'readonly')
        self.get_tags()
        self.tags_dropdown.pack(padx = (15, 0), ipadx = 15, ipady = 15, anchor = 'nw')
        self.tags_dropdown.set("None")

        #productivity checkbox for time to complete tasks
        self.productivity_checkbox_frame = tkinter.Frame(self.productivity.scrollable_frame, bg = '#8e9294')
        self.productivity_checkbox_frame.pack(fill = 'x', expand = True)
        self.productivity_checkbox_var = tkinter.BooleanVar()
        self.productivity_checkbox = tkinter.Checkbutton(self.productivity_checkbox_frame, variable= self.productivity_checkbox_var, onvalue = 1, offvalue = 0, font = ('Arial', 15), bg = '#8e9294', activebackground = '#8e9294')
        self.productivity_checkbox_label = tkinter.Label(self.productivity_checkbox_frame, text = 'Include Time to Complete Tasks in Productivity Visualization? (Optional)', font = ('Arial', 15), fg = '#fff', bg = '#8e9294', justify = 'left')
        self.productivity_checkbox.pack(side = 'left', padx = (15, 0), ipady = 15, anchor = 'nw')
        self.productivity_checkbox_label.pack(ipady = 15, side = 'left', anchor = 'nw')

        #Create Visualization Button
        self.create_visualization_button = ttk.Button(self.productivity.scrollable_frame, text = 'Create Visualization', command = self.productivity_visualization, style = 'MainPage.TButton', cursor = 'hand2', width = 20)
        self.create_visualization_button.pack(padx = (15, 0), ipadx = 15, ipady = 15, anchor = 'nw')

        #Get the user selections
        self.time_dropdown.bind("<<ComboboxSelected>>", self.get_time_dropdown_selection)

        # settings frame
        self.settings = ScrollableFrame(self)
        self.settings_label = tkinter.Label(self.settings.scrollable_frame, text = 'Settings', foreground = '#fff', bg = '#8e9294', font = ('Arial', 30))
        self.settings_label.pack(ipadx = 15, ipady = 15, anchor = 'nw')

        # add task buttons
        self.today.add_task_button = tkinter.Label(self.today.scrollable_frame, text = '+', font = ('Arial', 30), foreground = '#fff', background = '#8e9294', cursor = 'hand2')
        self.today.add_task_button.place(x = 978, y = 20)
        self.today.add_task_button.bind('<Button-1>', lambda event: self.add_task(self.today.add_task_button, False))
        self.today.add_task_button.bind('<Enter>', lambda event: change_color(self.today.add_task_button, "lightgreen"))
        self.today.add_task_button.bind('<Leave>', lambda event: change_color(self.today.add_task_button, "white"))

        self.upcoming.add_task_button = tkinter.Label(self.upcoming.scrollable_frame, text = '+', font = ('Arial', 30), foreground = '#fff', background = '#8e9294', cursor = 'hand2')
        self.upcoming.add_task_button.place(x = 978, y = 20)
        self.upcoming.add_task_button.bind('<Button-1>', lambda event: self.add_task(self.upcoming.add_task_button, True))
        self.upcoming.add_task_button.bind('<Enter>', lambda event: change_color(self.upcoming.add_task_button, "lightgreen"))
        self.upcoming.add_task_button.bind('<Leave>', lambda event: change_color(self.upcoming.add_task_button, "white"))

        def change_color(widget, fg_color):
            widget.config(fg = fg_color)

        self.q_today()
        self.q_upcoming()
        self.q_complete()

    def get_tags(self):
        tags = ["None", "All Tags"] + llcsv.get_all_tags()
        self.tags_dropdown.config(values = tags)
    
    #This probably needs some work to make sure it's communicating with the plot func correctly
    #I think the custom date range is broken
    def get_time_dropdown_selection(self, event):
        #grab the selection
        selected_option = self.time_dropdown.get()
        #if today, grab today's date
        if selected_option == "Today":
            self.start_date = None
            self.end_date = None
            self.month = None
            self.daily = self.daily = datetime.now().strftime("%Y-%m-%d")
        #if this month, grab current month and year
        elif selected_option == "This Month":
            self.start_date = None
            self.end_date = None
            self.daily = None
            self.month = datetime.now().strftime("%Y-%m")
        #if custom, calls function to bring up popup for calendar selection
        elif selected_option == "Custom":
            self.daily = None
            self.month = None
            self.calendar_for_productivity()

    #This function is called when the user selects custom date range
    #it creates a calendar popup for the user to set the start and end date
    #you have to bring up calendar, hit set start date, then bring up calendar again and set end date
    def calendar_for_productivity(self):
        def set_dates():
            self.start_date = start_date.get_date()
            self.end_date = end_date.get_date()
            self.calendar_popup.destroy()

        self.calendar_popup = tkinter.Toplevel()
        self.calendar_popup.title("Select Start and End Date")

        tkinter.Label(self.calendar_popup, text = "Select Start Date:", font=('Arial', 12)).pack()
        start_date = Calendar(self.calendar_popup, selectmode='day', date_pattern='yyyy-mm-dd',
                                  showweeknumbers=False)
        start_date.pack()

        tkinter.Label(self.calendar_popup, text="Select End Date", font=("Arial", 12)).pack()
        end_date = Calendar(self.calendar_popup, selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False)
        end_date.pack()
        ttk.Button(self.calendar_popup, text="Set Dates", command=set_dates).pack()

    #This function is called when the user clicks the create visualization button
    #it gathers all the drop down / check box selections to send to the plot creator
    def productivity_visualization(self):
        tag_id = None if self.tags_dropdown.get() == "None" else self.tags_dropdown.get()
        time_input = self.productivity_checkbox_var.get()

        #print the selections
        print("Time Input: ", time_input, "Tag ID: ", tag_id, "Start Date: ", self.start_date, "End Date: ", self.end_date, "Month: ", self.month, "Daily: ", self.daily)
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
        popup.geometry("1000x1000")
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
            tTask = Task(self.today.scrollable_frame, self.footer.progress, task_id, self.refresh, self.get_tags)

    def q_complete(self):
        self.completed_task = llcsv.getCompletedTask() #returns a list of strings
        for task_id in self.completed_task: 
            cTask = Task(self.completed.scrollable_frame, self.footer.progress, task_id, self.refresh, self.get_tags)

    def q_upcoming(self):
        self.upcoming_tasks = llcsv.getUpcomingTask() #returns a list of strings
        for task_id in self.upcoming_tasks:
            uTask = Task(self.upcoming.scrollable_frame, self.footer.progress, task_id, self.refresh, self.get_tags)

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

    #opens productivity frame
    def open_settings(self, event):
        if self.current_frame != self.settings:
            self.open_frame(self.settings, self.settings_button)

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
    def add_task(self, widget, upcoming):
        widget.config(fg = 'green')
        new_task = Task(self.current_frame.scrollable_frame, self.footer.progress, None, self.refresh, self.get_tags, upcoming)
        self.current_frame.bind_events()
        widget.config(fg = 'lightgreen')
        
    #progress bar function
    def progress_bar(self):
        self.footer.progress['value'] = (llcsv.getProgessPerc()) * 100
    
    # runs upon clicking logo (proof of concept for losing the buttons, could be a cool easter egg maybe)
    def on_logo_click(self, event):
        print('clicked me!')
        #plays sound
        if sys.platform == "win32":
            playsound('leapListFS.mp3')

    def refresh(self, task):
        if llcsv.is_completed(task.task_id):
            cTask = Task(self.completed.scrollable_frame, self.footer.progress, task.task_id, self.refresh, self.get_tags)
        elif llcsv.is_today(task.task_id):
            tTask = Task(self.today.scrollable_frame, self.footer.progress, task.task_id, self.refresh, self.get_tags)
        else:
            uTask = Task(self.upcoming.scrollable_frame, self.footer.progress, task.task_id, self.refresh, self.get_tags)
        task.frame.destroy()

# create the application
if __name__ == '__main__':
    LeapList = LeapList()
    LeapList.mainloop()