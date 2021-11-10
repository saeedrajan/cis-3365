
from time import time
import tkinter as tk                    
from tkinter import Text, ttk
from tkinter.constants import NONE, X
import pyodbc
from datetime import datetime, date 


class SQLServer:

    def __init__(self, server, db, uid, pwd, dbdriver='ODBC Driver 17 for SQL Server'):
        self.dbdriver='DRIVER={'+dbdriver+'};'
        self.server='SERVER='+server+';'
        self.db='DATABASE='+db+';'
        self.uid='UID='+uid+';'
        self.pwd='PWD='+pwd

    def __enter__(self):
        self.connstr=self.dbdriver+self.server+self.db+self.uid+self.pwd
        self.cnxn=pyodbc.connect(self.connstr)
        self.cursor = self.cnxn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnxn.close()

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

def add_device():
    deviceID=int(input("Please enter the device number (integer) \n"))
    serial=input("Please enter the 10 character Device Serial. \n")
    campus=int(input("Please enter the corresponding campus ID integer \n"))
    student= int(input("If a student is borrowing this device, please enter their student ID. Otherwise, press ENTER.\n"))
    idate=input("Please enter the date of issuance, or press enter if not applicable. YY-MM-DD\n")
    rdate=input("Please enter the date scheduled for return, or press enter if not applicable. YY-MM-DD\n")
    availid=int(input("Please enter the availability ID Integer, or press enter if not applicable\n"))
    modelid=int(input("Please enter the Model ID Integer, or press enter if not applicable\n"))
    
    cursor.execute("INSERT INTO Device_Inventory (Device_ID, Serial_Number, Campus_ID, Student_ID, Date_Issued, Return_By, Avail_ID, Model_ID) VALUES (?,?,?,?,?,?,?, ?) ",
    deviceID, serial, campus, student, idate, rdate, availid, modelid)
    cursor.commit()
    return

def remove_device():
    deviceNumber=int(input("Please enter the device number of the object to be deleted"))
    cursor.execute("DELETE FROM Device_Inventory WHERE Device_ID =?",
    deviceNumber)
    cursor.commit()
    return True

def edit_deivce():
    device=int(input("Please enter the device ID integer value.\n"))
    print("Please follow the prompts to input the new device information.\n")
    serial=input("Please enter the 10 character Device Serial. \n")
    campus=int(input("Please enter the corresponding campus ID integer \n"))
    student= int(input("If a student is borrowing this device, please enter their student ID. Otherwise, press ENTER.\n"))
    idate=input("Please enter the date of issuance, or press enter if not applicable.\n")
    rdate=input("Please enter the date scheduled for return, or press enter if not applicable.\n")
    availid=int(input("Please enter the availability ID Integer, or press enter if not applicable\n"))
    modelid=int(input("Please enter the Model ID Integer, or press enter if not applicable\n"))

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
    
def edit_tickets():
    ticketnumber=int(input("Please enter the integer Ticket Number value.\n"))
    print("Please follow the prompts to enter new ticket information:\n")
    ticketstatus=int(input("Please enter the ticket status identifying integer.\n"))
    desc= input("Please enter a new description or press enter if not applicable.\n")
    #constuct update query using the user input.
    #Shaylas update query #2
    cursor.execute("""UPDATE Ticketing_System
    SET Ticket_Status_ID=?,
    Description =?
    WHERE Ticket_Number=?""",
    ticketstatus, desc, ticketnumber)
    cursor.commit()
    return

def add_tickets():
    ticketNumber=int(input("Please enter the ticket number integer. \n"))
    date_Opened=input("Please input the date the ticket was opened \n")
    ticket_type_ID=int(input("Please input the ticket type ID integer. \n"))
    ticket_status_ID=int(input("Please input the ticket status ID Integer. \n"))
    description=input("Please input the ticket description or press enter if not applicable\n")
    student_ID=int(input("Please enter the student ID relevant to the ticket request.\n"))
    cursor.execute("INSERT INTO Ticketing_System VALUES (?,?,?,?,?,?)",
    ticketNumber,date_Opened,ticket_type_ID,ticket_status_ID,description,student_ID)
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
        self.root.title("Tab Widget")
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
    def get_root(self):
        return self.root

    def get_email(self):
        return self.email

    def get_passwd(self):
        return self.password
 
    def get_login_btn(self):
        return self.loginbutton

    def clean(self, tab):
        for wid in tab.winfo_children():
            wid.destroy()
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

        edit_students_values = tk.Button(self.tab3, text="Edit Student", command=self.submit_btn).place(x=230, y= 150)
        # back = tk.Button(self.tab3, text="Back", command=self.clean(self.tab3)).place(x=230, y= 160)
        
        
    def add_student_btn(self):
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
        result = view()
        lb = tk.Label(self.tab3,text=self.in_time).place(x=90,y=50)
        
        # print(result)
        listbox = tk.Listbox(self.tab3, width=1000)
        listbox.insert(0, ("Fname", "Lname", "Student ID"))
        for row in range(1,len(result)):
            listbox.insert(row, result[row])
        listbox.pack(side="bottom")
    
<<<<<<< HEAD
    def remove_student_btn(self):
        pass
=======
    def rm_student(self):
        sid = self.rm_sid.get()
        remove_students(sid)

    def remove_student_btn(self):
        tk.Label(self.tab3, text="Enter Student ID").place(x=20, y=40)
        tk.Entry(self.tab3, textvariable=self.rm_sid).place(x=120,y=40)
        tk.Button(self.tab3, text="Remove Student", command=self.rm_student).place(x=20,y=60)

>>>>>>> 5cc3f7f97c6388971525fbc3c0219cd7051dfe5f

    def accounts_tab(self):
        edit_student_button=tk.Button(self.tab3, text="Edit Student", command=self.edit_student_btn).place(x=20, y= 10)
        add_student_button=tk.Button(self.tab3, text="Add Student", command=self.add_student_btn).place(x=100, y= 10)
        view_students_button=tk.Button(self.tab3, text="View Student", command=self.view_student_btn).place(x=175, y= 10)
        remove_student_button=tk.Button(self.tab3, text="Remove Student", command=self.remove_student_btn).place(x=280, y= 10)

    def appointments_tab(self):
        add_tickets=tk.Button(self.tab4, text="Add Tickets").place(x=30, y= 50)
        edit_tickets=tk.Button(self.tab4, text="Edit Tickets").place(x=30, y= 90)
        view_tickets=tk.Button(self.tab4, text="View Tickets").place(x=30, y= 130)

    def devices_tab(self):
        add_device_button=tk.Button(self.tab5, text="Add Device").place(x=30, y= 50)
        remove_devices_button=tk.Button(self.tab5, text="Remove Devices").place(x=30, y= 130)
        edit_devices_button=tk.Button(self.tab5, text="Edit Devices").place(x=30, y= 210)
        add_purchase_button=tk.Button(self.tab5, text="Add Purchase").place(x=240, y= 50)
        view_purchases_button=tk.Button(self.tab5, text="View Purchases").place(x=240, y= 130)

    def clock_in_btn(self):
        self.in_time, self.in_date = clock_in()
        time_lb = tk.Label(self.tab2,text=self.in_time).place(x=90,y=50)

    def clock_out_btn(self):
        self.out_time = clock_out(self.sid,self.in_time, self.in_date)
        time_lb = tk.Label(self.tab2, text=self.out_time).place(x=100, y=90)

    def puch_btn(self):
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

    def login_tab(self):
        
        name = tk.Label(self.tab1, text="Email:").place(x=30, y=50)
        passwd = tk.Label(self.tab1, text="Password:").place(x=30, y=130)

        user = tk.Entry(self.tab1, textvariable=self.email_var).place(x=90, y= 50)
        password = tk.Entry(self.tab1, textvariable=self.passwd_var).place(x=90, y= 130)
        login_button=tk.Button(self.tab1, text="Login", command = self.login_btn).place(x=90, y= 230)
    # def logout_btn(self):
    #     self.tabControl.destroy()
    #     self.tab1 = ttk.Frame(self.tabControl)
    #     self.tabControl.add(self.tab1, text="Login")
    #     self.tabControl.pack(expand = 1, fill ="both")  
    # def logout_tab(self):
    #     logout = tk.Button(self.tab6, text="Logout", command=self.logout_btn).place(x=90, y=130)

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


# ttk.Label(tab1, 
#           text ="Welcome to \
#           GeeksForGeeks").grid(column = 0, 
#                                row = 0,
#                                padx = 30,
#                                pady = 30)  
# ttk.Label(tab2,
#           text ="Lets dive into the\
#           world of computers").grid(column = 0,
#                                     row = 0, 
#                                     padx = 30,
#                                     pady = 30)
  
