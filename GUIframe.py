import tkinter as tk
from tkinter.constants import X


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()




class Login(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Please Enter Login Credentials")
       label.pack(side="top", fill="both", expand=True)
       name = tk.Label(self, text="Email:").place(x=30, y=50)
       user = tk.Text(self, height=1,width=10).place(x=90, y= 50)
       passwd = tk.Label(self, text="Password:").place(x=30, y=130)
       password = tk.Text(self, height=1,width=10).place(x=90, y= 130)
       login_button=tk.Button(self, text="Login").place(x=90, y= 230)

       tk.Label(self,text="First Name")
       tk.Label(self,text="Last Name")
        # supposed to be code that brings in data entry next to the labels of username and password

    #    e1 = tk.Entry(self)
    #    e2 = tk.Entry(self)
    #    e1.grid(row=0, column=1)
    #    e2.grid(row=1, column=1)

class Select(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Main Menu")
       label.pack(side="top", fill="both", expand=True)
       clock_in_menu_button=tk.Button(self, text="Clock In/Clock Out").place(x=30, y= 50)
       accounts_button=tk.Button(self, text="Accounts").place(x=30, y= 130)
       appointments_button=tk.Button(self, text="Appointments").place(x=240, y= 50)
       devices_button=tk.Button(self, text="Devices").place(x=240, y= 130)


class Clock(Page):
   def __init__(self, *args, **kwargs):
    Page.__init__(self, *args, **kwargs)
    label = tk.Label(self, text="Clock In/Out")
    label.pack(side="top", fill="both", expand=True)
    clock_in_button=tk.Button(self, text="Clock In").place(x=30, y= 50)
    clock_out_button=tk.Button(self, text="Clock Out").place(x=30, y= 90)
    punch_history=tk.Button(self, text="Punch History").place(x=30, y= 130)


class Accounts(Page):
   def __init__(self, *args, **kwargs):
    Page.__init__(self, *args, **kwargs)
    label = tk.Label(self, text="Accounts")
    label.pack(side="top", fill="both", expand=True)
    edit_student_button=tk.Button(self, text="Edit Student").place(x=30, y= 50)
    add_student_button=tk.Button(self, text="Add Student").place(x=30, y= 130)
    view_students_button=tk.Button(self, text="View Student").place(x=240, y= 50)
    remove_student_button=tk.Button(self, text="Remove Student").place(x=240, y= 130)


class Appointments(Page):
   def __init__(self, *args, **kwargs):
    Page.__init__(self, *args, **kwargs)
    label = tk.Label(self, text="Appointments")
    label.pack(side="top", fill="both", expand=True)
    add_tickets=tk.Button(self, text="Add Tickets").place(x=30, y= 50)
    edit_tickets=tk.Button(self, text="Edit Tickets").place(x=30, y= 90)
    view_tickets=tk.Button(self, text="View Tickets").place(x=30, y= 130)

class Devices(Page):
   def __init__(self, *args, **kwargs):
    Page.__init__(self, *args, **kwargs)
    label = tk.Label(self, text="Devices")
    label.pack(side="top", fill="both", expand=True)
    add_device_button=tk.Button(self, text="Add Device").place(x=30, y= 50)
    remove_devices_button=tk.Button(self, text="Remove Devices").place(x=30, y= 130)
    edit_devices_button=tk.Button(self, text="Edit Devices").place(x=30, y= 210)
    add_purchase_button=tk.Button(self, text="Add Purchase").place(x=240, y= 50)
    view_purchases_button=tk.Button(self, text="View Purchases").place(x=240, y= 130)



class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Login(self)
        p2 = Select(self)
        p3 = Clock(self)
        p4 = Accounts(self)
        p5 = Appointments(self)
        p6 = Devices(self)


        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Login", command=p1.show)
        b2 = tk.Button(buttonframe, text="Selection", command=p2.show)
        b3 = tk.Button(buttonframe, text="Clock In/Out", command=p3.show)
        b4 = tk.Button(buttonframe, text="Accounts", command=p4.show)
        b5 = tk.Button(buttonframe, text="Appointments", command=p5.show)
        b6 = tk.Button(buttonframe, text="Devices", command=p6.show)


        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")
        b6.pack(side="left")

        p1.show()



if __name__ == "__main__":
    self = tk.Tk()
    main = MainView(self)
    main.pack(side="top", fill="both", expand=True)
    self.wm_geometry("400x400")
    # declaring string variable
    # for storing name and password
    name_var = tk.StringVar()
    passw_var = tk.StringVar()




def submit():
    name = name_var.get()
    password = passw_var.get()

    print("The name is : " + name)
    print("The password is : " + password)

    name_var.set("")
    passw_var.set("")
name_label = tk.Label(self, text='Email', font=('calibre', 10, 'bold'))

       # creating a entry for input
       # name using widget Entry
name_entry = tk.Entry(self, textvariable=name_var, font=('calibre', 10, 'normal'))

       # creating a label for password
passw_label = tk.Label(self, text='Password', font=('calibre', 10, 'bold'))

       # creating a entry for password
passw_entry = tk.Entry(self, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')



self.mainloop()