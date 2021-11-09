
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

def remove_students():
    sid = input("Enter Student ID to remove")
    cursor.execute("DELETE FROM Students WHERE Student_ID = ?", sid)
    return True

def view():
    cursor.execute("SLELECT * FROM Students")
    for row in cursor:
        newrow = [e.strip() if isinstance(e, str) else e for e in row]
        return newrow
    return

def add_student():
    first = 'Hank'
    last = 'James'
    sid = 12697
    dob = '2003-12-1'
    address = '74874 Atlantic Ave'
    city = 'Cleveland'
    zipcode = 77327
    phone = '2815558967'
    status = 'senior'
    campus = 1
    email = 'setsg@gmail.com'
    eid = 2
    password = 'password'
    stateID = 49

    cursor.execute("""
    INSERT INTO Students(Fname,Lname,Student_ID,Date_Of_Birth,Address,City,Zipcode,Phone,Status,Campus_ID,Email,Employee_ID,password,State_ID)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", 
    first, last, sid, dob, address, city, zipcode, phone, status, campus, email, eid, password, stateID)
    cursor.commit()
    return True

def edit_student():
    # sid = 
    first = 'Hank'
    last = 'James'
    dob = '2003-12-1'
    address = '74874 Atlantic Ave'
    city = 'Cleveland'
    zipcode = 77327
    phone = '2815558967'
    status = 'senior'
    campus = 1
    email = 'setsg@gmail.com'
    eid = 2
    password = 'password'
    stateID = 49

    cursor.execute("UPDATE Students SET Fname = ?, Lname = ?, Date_Of_Birth = ?, Address = ?, City = ?,Zipcode = ?, Phone = ?, Status = ?, Campus_ID = ?, Email = ?, Employee_ID = ?, password = ?, State_ID WHERE Student_ID = ?",
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
    def get_root(self):
        return self.root

    def get_email(self):
        return self.email

    def get_passwd(self):
        return self.password
 
    def get_login_btn(self):
        return self.loginbutton


    def auth(self):
        self.tab1.destroy()        
        self.tabControl.add(self.tab2, text ='Clock In/Out')
        self.tabControl.add(self.tab3, text ='Accounts')
        self.tabControl.add(self.tab4, text ='Appointments')
        self.tabControl.add(self.tab5, text ='Devices')
        self.tabControl.add(self.tab6, text="Logout")
        self.tabControl.pack(expand = 1, fill ="both")

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
  
