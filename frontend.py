import tkinter as tk                    
from tkinter import IntVar, Listbox, Text, ttk
from tkinter.constants import CURRENT, NONE, X
import pyodbc
from datetime import datetime, date 


def login(username, password):
    cursor.execute('SELECT Student_ID, Employee_ID FROM Students WHERE password = ? AND Email = ?', password, username)
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        return newrow[0],newrow[1]   

def reset_password():
    email = input("Enter Email\n")
    password = input("Enter new password\n")
    cursor.execute("UPDATE Students SET PASSWORD = ? WHERE Email = ?;", password, email)
    return

def remove_students(sid):
    cursor.execute("DELETE FROM Students WHERE Student_ID = ?", sid)
    cursor.commit()
    return True

def view():
    my_list = []
    cursor.execute("SELECT Fname, Lname, Student_ID FROM Students")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        my_list.append(newrow)
    return my_list

def get_tickets_data():
    data = []
    cursor.execute("SELECT Ticket_Number, Ticket_Type_ID, Ticket_Status_ID, Student_ID FROM Ticketing_System")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        data.append(newrow)
    return data

def get_device_purchases_data():
    data = []
    cursor.execute("SELECT Serial_Number, Type_ID, Make_ID FROM Device_Purchases")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        data.append(newrow)
    return data

def add_student(first, last, sid, dob, address, city, zipcode, phone, status, campus, email, eid, password, stateID):

    cursor.execute("""
    INSERT INTO Students(Fname,Lname,Student_ID,Date_Of_Birth,Address,City,Zipcode,Phone,Status,Campus_ID,Email,Employee_ID,password,State_ID)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
    first, last, sid, dob, address, city, zipcode, phone, status, campus, email, eid, password, stateID)
    cursor.commit()
    return True

def edit_student(first, last, dob, address, city, zipcode, phone, status, campus, email, eid, password, stateID, sid):
    cursor.execute("UPDATE Students SET Fname = ?, Lname = ?, Date_Of_Birth = ?, Address = ?, City = ?,Zipcode = ?, Phone = ?, Status = ?, Campus_ID = ?, Email = ?, Employee_ID = ?, password = ?, State_ID = ? WHERE Student_ID = ?",
    first, last, dob, address, city, zipcode, phone, status, campus, email,eid,password, stateID, sid)
    cursor.commit()
    return

def clock_in():
    
    time = now.strftime("%H:%M:%S")
    current_date = today.strftime("%Y-%m-%d")
    return time, current_date

def clock_out(sid, time_in, date_in):
    current_time = now.strftime("%H:%M:%S")

    cursor.execute('SELECT COUNT(*) FROM TimeClock')
    for row in cursor: 
        index = row[0]+1
    
    cursor.execute('INSERT INTO TimeClock (Entry_ID, Student_ID , Date ,Clock_In, Clock_out) VALUES (?,?,?,?,?)', 
    index, sid, date_in, time_in, current_time)
    cursor.commit()
    return current_time


# Device Management

def add_device_purchase():

    serial=input("Please enter the 10 character Device Serial. \n")
    pid=int(input("Please enter the purchase number. \n"))
    Date=input("Please enter the date of purchase YY-MM-DD\n ")
    typeid=int(input("Please enter the integer Type ID number\n"))
    makeid=int(input("Please enter the integer Make ID number\n"))
    Price=float(input("Please enter the unit price in USD: \n"))
    #Shaylas insert query #1:
    cursor.execute("INSERT INTO Device_Purchases (Serial_Number, PO_Number, Purchase_date, Type_ID, Make_ID, Unit_Price) VALUES (?,?,?,?,?,?)",
    serial, pid, Date, typeid, makeid, Price)
    cursor.commit()
    return

def view_purchases():
    cursor.execute("SELECT * FROM Device_Purchases")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
    return newrow

def add_device(serial, campus, student, idate, rdate, availid, modelid):    
    cursor.execute("INSERT INTO Device_Inventory (Serial_Number, Campus_ID, Student_ID, Date_Issued, Return_By, Avail_ID, Model_ID) VALUES (?,?,?,?,?,?, ?) ",
    serial, campus, student, idate, rdate, availid, modelid)
    cursor.commit()
    return

def remove_device(deviceNumber):
    cursor.execute("DELETE FROM Device_Inventory WHERE Device_ID =?",
    deviceNumber)
    cursor.commit()
    return True

def edit_deivce(serial, campus, student, idate, rdate,availid, modelid, device):
    cursor.execute("""UPDATE Device_Inventory SET
        Serial_Number=?, 
        Campus_ID=?, 
        Student_ID=?, 
        Date_Issued=?, 
        Return_By=?,
        Avail_ID=?, 
        Model_ID=? 
        WHERE Device_ID=?""", serial, campus, student, idate, rdate,availid, modelid, device)
    cursor.commit()
    return

def view_device():
    result = []
    cursor.execute("")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        result.append(newrow)
    return result

# Appointments

def view_tickets():
    result = []
    cursor.execute("SELECT * FROM Ticketing_System ORDER BY Date_Opened DESC")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        result.append(newrow)
    return result
    
def edit_tickets(ticketstatus, desc, ticketnumber):
    #constuct update query using the user input.
    #Shaylas update query #2
    cursor.execute("""UPDATE Ticketing_System
    SET Ticket_Status_ID=?,
    Description =?
    WHERE Ticket_Number=?""",
    ticketstatus, desc, ticketnumber)
    cursor.commit()
    return

def add_tickets(ticketNumber,date_Opened,ticket_type_ID,ticket_status_ID,description,student_ID):

    cursor.execute("INSERT INTO Ticketing_System VALUES (?,?,?,?,?,?)",
    ticketNumber,date_Opened,ticket_type_ID,ticket_status_ID,description,student_ID)
    cursor.commit()    
    return True

def add_purchase(serial_number, po_number, purchase_date, type_id, make_id, unit_price):

    cursor.execute("INSERT INTO Device_Purchases VALUES (?,?,?,?,?,?)",
    serial_number, po_number, purchase_date, type_id, make_id, unit_price)
    cursor.commit()    
    return True

def puch_hist(sid):
    result = []
    cursor.execute("SELECT Date, Clock_In, Clock_out FROM TimeClock WHERE Student_ID = ?", sid)
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        result.append(newrow)
    return result
    



class frontend:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LinkTech")
        self.root.wm_geometry("400x400")
        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tab5 = ttk.Frame(self.tabControl)
        self.tab6 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text ='Login')
        self.tabControl.pack(expand = 1, fill ="both")
        self.email_var=tk.StringVar()
        self.passwd_var=tk.StringVar()
        self.sid = int
        self.eid = int
        self.email = ""
        self.password = ''
        self.in_time = ''
        self.in_date = ''
        self.sid_var = tk.IntVar()
        self.zip_var = tk.IntVar()
        self.eid_var =tk.IntVar()
        self.state_var =tk.IntVar()
        self.cam_var=tk.IntVar()
        self.first_var=tk.StringVar()
        self.last_var=tk.StringVar()
        self.dob_var=tk.StringVar()
        self.add_var=tk.StringVar()
        self.city_var=tk.StringVar()
        self.phone_var=tk.StringVar()
        self.stat_var=tk.StringVar()
        self.email_e_var=tk.StringVar()
        self.password_var=tk.StringVar()
        self.rm_sid = tk.IntVar()
        # Add Ticket Fields
        self.ticket_number_var = tk.StringVar()
        self.date_opened_var = tk.StringVar()
        self.ticket_type_ID_var = tk.IntVar()
        self.ticket_status_ID_var = tk.IntVar()
        self.description_var = tk.StringVar()
        self.student_ID_var = tk.IntVar()
        # Add Purchase Fields
        self.serial_number_var = tk.IntVar()
        self.po_number_var = tk.IntVar()
        self.purchase_date_var = tk.StringVar()
        self.ticket_type_ID_var = tk.IntVar()
        self.make_id_var = tk.IntVar()
        self.unit_price_var = tk.IntVar()


    def get_root(self):
        return self.root

    def get_email(self):
        return self.email

    def get_passwd(self):
        return self.password
 
    def get_login_btn(self):
        return self.loginbutton

    def clean(self):
        for wid in self.tab2.winfo_children():
            wid.destroy()
        for wid in self.tab3.winfo_children():
            wid.destroy()
        for wid in self.tab4.winfo_children():
            wid.destroy()
        for wid in self.tab5.winfo_children():
            wid.destroy()
        for wid in self.tab6.winfo_children():
            wid.destroy()
        
        self.clock_in_out_tab()
        self.accounts_tab()
        self.appointments_tab()
        self.devices_tab()  
        self.master()  
            
    def drop_down(self, tab, var, column, table, x_corr, y_corr):
        OPTIONS = []
        
        d = cursor.execute("SELECT {} FROM {}".format(column,table))
        self.drop_down_var = tk.StringVar(tab)
        for x in d:
            for y in x:
                OPTIONS.append(x[0])

        menu = tk.OptionMenu(tab, var, *OPTIONS)
        menu.pack()
        menu.place(x=x_corr,y=y_corr)
    
    def auth(self):
        self.tab1.destroy()        
        self.tabControl.add(self.tab2, text ='Clock In/Out')
        self.tabControl.add(self.tab3, text ='Accounts')
        self.tabControl.add(self.tab4, text ='Appointments')
        self.tabControl.add(self.tab5, text ='Devices')
        self.tabControl.add(self.tab6, text="Logout")
        self.tabControl.pack(expand = 1, fill ="both")

    def submit_btn(self):
        sid=self.sid_var.get()
        first=self.first_var.get()
        last = self.last_var.get()
        dob= self.dob_var.get()
        add= self.add_var.get()
        city = self.city_var.get()
        zip = self.zip_var.get()
        phone = self.phone_var.get()
        stat = self.stat_var.get()
        cam = self.cam_var.get()
        email = self.email_e_var.get()
        eid = self.eid_var.get()
        password = self.password_var.get()
        state = self.state_var.get()
        
        edit_student(first, last, dob,add,city,zip, phone,stat,cam,email,eid,password,state, sid)
            
            
        self.sid_var.set("")
        self.first_var.set("")
        self.last_var.set("")
        self.dob_var.set("")
        self.add_var.set("")
        self.city_var.set("")
        self.zip_var.set("")
        self.phone_var.set("")
        self.stat_var.set("")
        self.cam_var.set("")
        self.email_e_var.set("")
        self.eid_var.set("")
        self.password_var.set("")
        self.state_var.set("")
        
    def edit_student_btn(self):
       
        self.clean()
        sid_lb = tk.Label(self.tab3, text="Student ID").place(x=20, y=40)
        self.drop_down(self.tab3, self.sid_var, "Student_ID", "Students", 80,40)
        # sid_en = tk.Entry(self.tab3, width=10, textvariable=self.sid_var).place(x=90, y=40)
        f_lb = tk.Label(self.tab3, text="First Name").place(x=20, y=70)
        first_en = tk.Entry(self.tab3, width=10, textvariable=self.first_var).place(x=90, y=70)
        last_lb = tk.Label(self.tab3, text="Last Name").place(x=20, y=100)
        last_en = tk.Entry(self.tab3,width=10, textvariable=self.last_var).place(x=90, y=100)
        dob_lb = tk.Label(self.tab3, text="Date of Birth").place(x=20, y=130)
        dob_en = tk.Entry(self.tab3,width=10, textvariable=self.dob_var).place(x=90, y=130)
        add_lb = tk.Label(self.tab3, text="Address").place(x=20, y=160)
        add_en = tk.Entry(self.tab3,width=10, textvariable=self.add_var).place(x=90, y=160)
        city_lb = tk.Label(self.tab3, text="City").place(x=20, y=190)
        city_en = tk.Entry(self.tab3,width=10, textvariable=self.city_var).place(x=90, y=190)
        zip_lb = tk.Label(self.tab3, text="Zipcode").place(x=20, y=220)
        zip_en = tk.Entry(self.tab3,width=10, textvariable=self.zip_var).place(x=90, y=220)
        phone_lb = tk.Label(self.tab3, text="Phone").place(x=20, y=250)
        phone_en = tk.Entry(self.tab3,width=10, textvariable=self.phone_var).place(x=90, y=250)
        stat = tk.Label(self.tab3, text="Status").place(x=20, y=280)
        stat_en = tk.Entry(self.tab3,width=10, textvariable=self.stat_var).place(x=90, y=280)
        cam_lb = tk.Label(self.tab3, text="Campus ID").place(x=20, y=310)
        cam_en = tk.Entry(self.tab3,width=10, textvariable=self.cam_var).place(x=90, y=310)
        email_lb = tk.Label(self.tab3, text="Email").place(x=20, y=340)
        email_en = tk.Entry(self.tab3,width=10, textvariable=self.email_e_var).place(x=90, y=340)
        eid_lb = tk.Label(self.tab3, text="Employee ID").place(x=160, y=40)
        eid_en = tk.Entry(self.tab3,width=10, textvariable=self.eid_var).place(x=230, y=40)
        passwd_lb = tk.Label(self.tab3, text="Password").place(x=160, y=70)
        passwd_en = tk.Entry(self.tab3,width=10, textvariable=self.password_var).place(x=230, y=70)
        state_lb = tk.Label(self.tab3, text="State ID").place(x=160, y=100)
        state_en = tk.Entry(self.tab3,width=10, textvariable=self.state_var).place(x=230, y=100)

        edit_students_values = tk.Button(self.tab3, text="Edit Student", command=self.submit_btn).place(x=230, y= 150)
        # back = tk.Button(self.tab3, text="Back", command=self.clean(self.tab3)).place(x=230, y= 160)


    def add_student_btn(self):
        self.clean()
        sid_lb = tk.Label(self.tab3, text="Student ID").place(x=20, y=40)
        sid_en = tk.Entry(self.tab3, width=10, textvariable=self.sid_var).place(x=90, y=40)
        f_lb = tk.Label(self.tab3, text="First Name").place(x=20, y=70)
        first_en = tk.Entry(self.tab3, width=10, textvariable=self.first_var).place(x=90, y=70)
        last_lb = tk.Label(self.tab3, text="Last Name").place(x=20, y=100)
        last_en = tk.Entry(self.tab3,width=10, textvariable=self.last_var).place(x=90, y=100)
        dob_lb = tk.Label(self.tab3, text="Date of Birth").place(x=20, y=130)
        dob_en = tk.Entry(self.tab3,width=10, textvariable=self.dob_var).place(x=90, y=130)
        add_lb = tk.Label(self.tab3, text="Address").place(x=20, y=160)
        add_en = tk.Entry(self.tab3,width=10, textvariable=self.add_var).place(x=90, y=160)
        city_lb = tk.Label(self.tab3, text="City").place(x=20, y=190)
        city_en = tk.Entry(self.tab3,width=10, textvariable=self.city_var).place(x=90, y=190)
        zip_lb = tk.Label(self.tab3, text="Zipcode").place(x=20, y=220)
        zip_en = tk.Entry(self.tab3,width=10, textvariable=self.zip_var).place(x=90, y=220)
        phone_lb = tk.Label(self.tab3, text="Phone").place(x=20, y=250)
        phone_en = tk.Entry(self.tab3,width=10, textvariable=self.phone_var).place(x=90, y=250)
        stat = tk.Label(self.tab3, text="Status").place(x=20, y=280)
        stat_en = tk.Entry(self.tab3,width=10, textvariable=self.stat_var).place(x=90, y=280)
        cam_lb = tk.Label(self.tab3, text="Campus ID").place(x=20, y=310)
        cam_en = tk.Entry(self.tab3,width=10, textvariable=self.cam_var).place(x=90, y=310)
        email_lb = tk.Label(self.tab3, text="Email").place(x=20, y=340)
        email_en = tk.Entry(self.tab3,width=10, textvariable=self.email_e_var).place(x=90, y=340)
        eid_lb = tk.Label(self.tab3, text="Employee ID").place(x=160, y=40)
        eid_en = tk.Entry(self.tab3,width=10, textvariable=self.eid_var).place(x=230, y=40)
        passwd_lb = tk.Label(self.tab3, text="Password").place(x=160, y=70)
        passwd_en = tk.Entry(self.tab3,width=10, textvariable=self.password_var).place(x=230, y=70)
        state_lb = tk.Label(self.tab3, text="State ID").place(x=160, y=100)
        state_en = tk.Entry(self.tab3,width=10, textvariable=self.state_var).place(x=230, y=100)

        edit_students_values = tk.Button(self.tab3, text="Add Student", command=self.add_student_submission_btn).place(x=230, y= 150)
        #back = tk.Button(self.tab3, text="Back", command=self.clean(self.tab3)).place(x=230, y= 160)

    def add_student_submission_btn(self):
        sid=self.sid_var.get()
        first=self.first_var.get()
        last = self.last_var.get()
        dob= self.dob_var.get()
        add= self.add_var.get()
        city = self.city_var.get()
        zip = self.zip_var.get()
        phone = self.phone_var.get()
        stat = self.stat_var.get()
        cam = self.cam_var.get()
        email = self.email_e_var.get()
        eid = self.eid_var.get()
        password = self.password_var.get()
        state = self.state_var.get()
        
        add_student(first, last, sid, dob, add, city, zip, phone, stat, cam, email, eid, password, state)
            
            
        self.sid_var.set("")
        self.first_var.set("")
        self.last_var.set("")
        self.dob_var.set("")
        self.add_var.set("")
        self.city_var.set("")
        self.zip_var.set("")
        self.phone_var.set("")
        self.stat_var.set("")
        self.cam_var.set("")
        self.email_e_var.set("")
        self.eid_var.set("")
        self.password_var.set("")
        self.state_var.set("")

    def view_student_btn(self):
        self.clean()
        result = view()
        lb = tk.Label(self.tab3,text=self.in_time).place(x=90,y=50)
        
        # print(result)
        listbox = tk.Listbox(self.tab3, width=1000)
        listbox.insert(0, ("Fname", "Lname", "Student ID"))
        for row in range(1,len(result)):
            listbox.insert(row, result[row])
        listbox.pack(side="bottom")
    
    def rm_student(self):
        sid = self.rm_sid.get()
        remove_students(sid)

    def remove_student_btn(self):
        self.clean()
        tk.Label(self.tab3, text="Enter Student ID").place(x=20, y=40)
        tk.Entry(self.tab3, textvariable=self.rm_sid).place(x=120,y=40)
        tk.Button(self.tab3, text="Remove Student", command=self.rm_student).place(x=20,y=60)


    def add_tickets_submission_btn(self):
        ticket_number = self.ticket_number_var.get()
        date_opened = self.date_opened_var.get()
        ticket_type_ID = self.ticket_type_ID_var.get()
        ticket_status_ID = self.ticket_status_ID_var.get()
        description = self.description_var.get()
        student_ID = self.student_ID_var.get()
        
        add_tickets(ticket_number, date_opened, ticket_type_ID, ticket_status_ID, description, student_ID)
        
    def add_tickets_btn(self):
        self.clean()
        # Ticket Number Field
        tk.Label(self.tab4, text='Ticket Number').place(x=120, y=40)
        tk.Entry(self.tab4, width=10, textvariable=self.ticket_number_var).place(x=260, y=40)
        # Date Opened field
        tk.Label(self.tab4, text='Date Opened').place(x=120, y=70)
        tk.Entry(self.tab4, width=10, textvariable=self.date_opened_var).place(x=260, y=70)
        # Ticket Type ID field
        tk.Label(self.tab4, text='Ticket Type').place(x=120, y=100)
        tk.Entry(self.tab4, width=10, textvariable=self.ticket_type_ID_var).place(x=260, y=100)
        # Ticket Status ID field
        tk.Label(self.tab4, text='Ticket Status').place(x=120, y=130)
        tk.Entry(self.tab4, width=10, textvariable=self.ticket_status_ID_var).place(x=260, y=130)
        # Description field
        tk.Label(self.tab4, text='Description').place(x=120, y=160)
        tk.Entry(self.tab4, width=10, textvariable=self.description_var).place(x=260, y=160)
        # Student ID field
        tk.Label(self.tab4, text='Student ID').place(x=120, y=190)
        tk.Entry(self.tab4, width=10, textvariable=self.student_ID_var).place(x=260, y=190)

        # Button to submit the values
        tk.Button(self.tab4, text="Submit Ticket", command=self.add_tickets_submission_btn).place(x=230, y= 250)

    def view_tickets_btn_function(self):
        self.clean()
        result = get_tickets_data()

        # print result
        listbox = tk.Listbox(self.tab4, width=1000)
        listbox.insert(0, ("Ticket Number", "Ticket Type", "Ticket Status", "Student ID"))
        for row in range(1,len(result)):
            listbox.insert(row, result[row])
        listbox.pack(side="bottom")

    def edit_ticket_btn(self):
        edit_tickets(self.dob_var.get(),self.add_var.get(),self.sid_var.get())

    def edit_ticket(self):
        self.clean()
        tk.Label(self.tab4, text="Ticket Number").place(x=200, y=60)
        tk.Entry(self.tab4, width=10, textvariable=self.sid_var).place(x=290, y=100)
        tk.Label(self.tab4, text="Ticket Status").place(x=200, y=130)
        tk.Entry(self.tab4,width=10, textvariable=self.dob_var).place(x=290, y=130)
        tk.Label(self.tab4, text="Description").place(x=200, y=160)
        tk.Entry(self.tab4,width=10, textvariable=self.add_var).place(x=290, y=160)
        tk.Button(self.tab4,text="Submit",command=self.edit_ticket_btn).place(x=200, y=220)

    def add_device_btn(self):
        add_device(self.dob_var.get(),self.add_var.get(),self.eid_var.get(),self.phone_var.get(),self.password_var.get(),self.cam_var.get(),self.state_var.get())

    def add_device_(self):
        self.clean()
        tk.Label(self.tab5, text="Serial").place(x=200, y=60)
        tk.Entry(self.tab5,width=10, textvariable=self.dob_var).place(x=290, y=60)
        tk.Label(self.tab5, text="Campus").place(x=200, y=80)
        tk.Entry(self.tab5,width=10, textvariable=self.add_var).place(x=290, y=80)
        tk.Label(self.tab5, text="Student ID").place(x=200, y=100)
        tk.Entry(self.tab5, width=10, textvariable=self.eid_var).place(x=290, y=100)
        tk.Label(self.tab5, text="Issued Date").place(x=200, y=120)
        tk.Entry(self.tab5,width=10, textvariable=self.phone_var).place(x=290, y=120)
        tk.Label(self.tab5, text="Return By").place(x=200, y=140)
        tk.Entry(self.tab5,width=10, textvariable=self.password_var).place(x=290, y=140)
        tk.Label(self.tab5, text="Available ID").place(x=200, y=160)
        tk.Entry(self.tab5,width=10, textvariable=self.cam_var).place(x=290, y=160)
        tk.Label(self.tab5, text="Model ID").place(x=200, y=180)
        tk.Entry(self.tab5,width=10, textvariable=self.state_var).place(x=290, y=180)
        
        tk.Button(self.tab5,text="Submit",command=self.add_device_btn).place(x=200, y=200)

    def remove_devices_btn(self):
        self.clean()
        device = self.dob_var.get()
        remove_device(device)

    def remove_devices_button(self):
        self.clean()
        tk.Label(self.tab5, text="Device ID").place(x=200, y=60)
        tk.Entry(self.tab5,width=10, textvariable=self.dob_var).place(x=290, y=60)
        tk.Button(self.tab5,text="Submit",command=self.remove_devices_btn).place(x=200, y=90)
    def edit_devices_btn(self):        
        edit_deivce(self.dob_var.get(), self.add_var.get, self.eid_var.get(), self.phone_var.get(), self.password_var.get(),self.cam_var.get(), self.state_var.get(), self.sid_var.get())

    def edit_devices_button(self):
        self.clean()
        tk.Label(self.tab5, text="Deivce ID").place(x=200, y=40)
        tk.Entry(self.tab5,width=10, textvariable=self.sid_var).place(x=290, y=40)
        tk.Label(self.tab5, text="Serial").place(x=200, y=60)
        tk.Entry(self.tab5,width=10, textvariable=self.dob_var).place(x=290, y=60)
        tk.Label(self.tab5, text="Campus").place(x=200, y=80)
        tk.Entry(self.tab5,width=10, textvariable=self.add_var).place(x=290, y=80)
        tk.Label(self.tab5, text="Student ID").place(x=200, y=100)
        tk.Entry(self.tab5, width=10, textvariable=self.eid_var).place(x=290, y=100)
        tk.Label(self.tab5, text="Issued Date").place(x=200, y=120)
        tk.Entry(self.tab5,width=10, textvariable=self.phone_var).place(x=290, y=120)
        tk.Label(self.tab5, text="Return By").place(x=200, y=140)
        tk.Entry(self.tab5,width=10, textvariable=self.password_var).place(x=290, y=140)
        tk.Label(self.tab5, text="Available ID").place(x=200, y=160)
        tk.Entry(self.tab5,width=10, textvariable=self.cam_var).place(x=290, y=160)
        tk.Label(self.tab5, text="Model ID").place(x=200, y=180)
        tk.Entry(self.tab5,width=10, textvariable=self.state_var).place(x=290, y=180)
        
        tk.Button(self.tab5,text="Submit",command=self.edit_devices_btn).place(x=200, y=200)


    def view_purchases_btn_function(self):
        self.clean()
        result = get_device_purchases_data()

        # print result
        listbox = tk.Listbox(self.tab5, width=1000)
        listbox.insert(0, ("Serial_Number", "Type_ID", "Make_ID"))
        for row in range(1,len(result)):
            listbox.insert(row, result[row])
        listbox.pack(side="bottom")

    def add_purchases_submission_btn(self):
        self.clean()
        serial_number = self.serial_number_var.get()
        po_number = self.po_number_var.get()
        purchase_date = self.purchase_date_var.get()
        type_id = self.ticket_type_ID_var.get()
        make_id = self.make_id_var.get()
        unit_price = self.unit_price_var.get()
        
        add_purchase(serial_number, po_number, purchase_date, type_id, make_id, unit_price)
    
    def show_add_purchase_fields(self):
        self.clean()
        # Serial Number field
        tk.Label(self.tab5, text='Serial Number').place(x=120, y=40)
        tk.Entry(self.tab5, width=10, textvariable=self.serial_number_var).place(x=260, y=40)
        # PO Number field
        tk.Label(self.tab5, text='PO Number').place(x=120, y=70)
        tk.Entry(self.tab5, width=10, textvariable=self.po_number_var).place(x=260, y=70)
        # Purchase Date field
        tk.Label(self.tab5, text='Purchase date').place(x=120, y=100)
        tk.Entry(self.tab5, width=10, textvariable=self.purchase_date_var).place(x=260, y=100)
        # Type ID field 
        tk.Label(self.tab5, text='Type ID').place(x=120, y=130)
        tk.Entry(self.tab5, width=10, textvariable=self.ticket_type_ID_var).place(x=260, y=130)
        # Make ID field
        tk.Label(self.tab5, text='Make ID').place(x=120, y=160)
        tk.Entry(self.tab5, width=10, textvariable=self.make_id_var).place(x=260, y=160)
        # Unit Price
        tk.Label(self.tab5, text='Unit Price').place(x=120, y=190)
        tk.Entry(self.tab5, width=10, textvariable=self.unit_price_var).place(x=260, y=190)

        # Button to submit the values
        tk.Button(self.tab5, text="Submit Purchase", command=self.add_purchases_submission_btn).place(x=230, y= 250)

    def accounts_tab(self):
        edit_student_button=tk.Button(self.tab3, text="Edit Student", command=self.edit_student_btn).place(x=20, y= 10)
        add_student_button=tk.Button(self.tab3, text="Add Student", command=self.add_student_btn).place(x=100, y= 10)
        view_students_button=tk.Button(self.tab3, text="View Student", command=self.view_student_btn).place(x=180, y= 10)
        remove_student_button=tk.Button(self.tab3, text="Remove Student", command=self.remove_student_btn).place(x=270, y= 10)

    def appointments_tab(self):
        add_tickets=tk.Button(self.tab4, text="Add Tickets", command=self.add_tickets_btn).place(x=30, y= 50)
        edit_tickets=tk.Button(self.tab4, text="Edit Tickets", command=self.edit_ticket).place(x=30, y= 90)
        view_tickets=tk.Button(self.tab4, text="View Tickets", command=self.view_tickets_btn_function).place(x=30, y= 130)

    def devices_tab(self):
        add_device_button=tk.Button(self.tab5, text="Add Device", command=self.add_device_).place(x=20, y= 10)
        remove_devices_button=tk.Button(self.tab5, text="Remove Devices", command=self.remove_devices_button).place(x=20, y= 40)
        edit_devices_button=tk.Button(self.tab5, text="Edit Devices", command=self.edit_devices_button).place(x=20, y= 70)
        add_purchase_button=tk.Button(self.tab5, text="Add Purchase", command=self.show_add_purchase_fields).place(x=20, y= 100)
        view_purchases_button=tk.Button(self.tab5, text="View Purchases", command=self.view_purchases_btn_function).place(x=20, y= 130)

    def clock_in_btn(self):
        self.in_time, self.in_date = clock_in()
        time_lb = tk.Label(self.tab2,text=self.in_time).place(x=90,y=50)

    def clock_out_btn(self):
        self.out_time = clock_out(self.sid,self.in_time, self.in_date)
        time_lb = tk.Label(self.tab2, text=self.out_time).place(x=100, y=90)

    def puch_btn(self):
        self.clean()
        result = puch_hist(self.sid)
        lb = tk.Label(self.tab2,text=self.in_time).place(x=90,y=50)
        
        # print(result)
        listbox = tk.Listbox(self.tab2, width=1000)
        listbox.insert(0, ("Date", "Time In", "Time Out"))
        for row in range(1,len(result)):
            listbox.insert(row, result[row])
        listbox.pack(side="bottom")
        
    def clock_in_out_tab(self):
        clock_in_button=tk.Button(self.tab2, text="Clock In", command=self.clock_in_btn).place(x=30, y= 50)
        clock_out_button=tk.Button(self.tab2, text="Clock Out", command=self.clock_out_btn).place(x=30, y= 90)
        punch_history=tk.Button(self.tab2, text="Punch History", command=self.puch_btn).place(x=30, y= 130)
        
    def login_btn(self):
        self.email=self.email_var.get()
        self.password=self.passwd_var.get()
        
        self.sid, self.eid = login(self.email, self.password)
        print(self.sid)
        
        self.email_var.set("")
        self.passwd_var.set("")
        if self.sid is None:
            self.login_tab()
        else:
            self.auth()
            self.clock_in_out_tab()
            self.accounts_tab()
            self.appointments_tab()
            self.devices_tab()
            self.master()
    def master_update(self):
        result = cursor.execute("SELECT * FROM {}".format(self.variable.get()))
        listbox = tk.Listbox(self.tab6, width=1000)

        for row in result:
            l =+ 1
            listbox.insert(l, row)
        listbox.pack(side="bottom")

    def master(self):
        OPTIONS = []
        
        d = cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME <> 'sys.diagrams'")
        self.variable = tk.StringVar(self.tab6)
        for x in d:
            for y in x:
                OPTIONS.append(x[0])

        tk.OptionMenu(self.tab6, self.variable, *OPTIONS).pack()
        tk.Button(self.tab6, text="Update", command=self.master_update).place(x=20,y=40)
        
    def login_tab(self):
        
        name = tk.Label(self.tab1, text="Email:").place(x=30, y=50)
        passwd = tk.Label(self.tab1, text="Password:").place(x=30, y=130)

        user = tk.Entry(self.tab1, textvariable=self.email_var).place(x=90, y= 50)
        password = tk.Entry(self.tab1, textvariable=self.passwd_var).place(x=90, y= 130)
        login_button=tk.Button(self.tab1, text="Login", command = self.login_btn).place(x=90, y= 230)

gui = frontend()
if __name__ == "__main__":
    
    server = 'Cot-CIS3365-03.cougarnet.uh.edu'
    database = 'LINKTECH' 
    username = 'atest' 
    password = 'atest' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    now = datetime.now()
    today = date.today()
    gui.login_tab()
   
gui.get_root().mainloop()


