# Import Required Library
from tkinter import *
from tkcalendar import Calendar
 
# Create Object
root = Tk()
 
# Set geometry
root.geometry("400x400")
 
# Add Calendar
cal = Calendar(root, selectmode = 'day', date_pattern = 'yyyy-mm-dd')
 
cal.pack(pady = 20)

# hides calendar
cal.pack_forget()

# shows calendar
cal.pack(pady = 20)
 
# removes calendar
# cal.destroy()

def grad_date():
    date.config(text = "Selected Date is: " + cal.get_date())
 
# Add Button and Label
Button(root, text = "Get Date",
       command = grad_date).pack(pady = 20)
 
date = Label(root, text = "")
date.pack(pady = 20)
 
# Execute Tkinter
root.mainloop()