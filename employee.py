from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+222+140")
        self.root.title("Employee")
        # self.root.maxsize(1350,700)
        # self.root.minsize(1350,700)
        self.root.focus_force()

        #----All variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #----search frame
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),borderwidth=2,relief="ridge",bg="White")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #----options
        cmb_search=ttk.Combobox(SearchFrame,values=("Select","Email","Name","Contact"),textvariable=self.var_searchby,state="readonly",justify=CENTER,font=("goudy old style", 12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        txt_search=Entry(SearchFrame,font=("goudy old style" ,15),textvariable=self.var_searchtxt,bg="white").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style" ,15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #----title
        title=Label(self.root,text="Employee Details",font=("goudy old style" ,15),bg="#581845",fg="white")
        title.place(x=50,y=100,width=1000)

        #----content
        #row1
        lbl_empid=Label(self.root,text="Emp ID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15),bg="white").place(x=350,y=150)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,values=("Select","Male","Female","Other"),textvariable=self.var_gender,state="readonly",justify=CENTER,font=("goudy old style", 15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=850,y=150,width=180)

        #row2
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",15),bg="white").place(x=350,y=190)
        lbl_doj=Label(self.root,text="D.O.J",font=("goudy old style",15),bg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="lightyellow").place(x=500,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="lightyellow").place(x=850,y=190,width=180)

        #row3
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",15),bg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,values=("Select","Admin","Employee"),textvariable=self.var_utype,state="readonly",justify=CENTER,font=("goudy old style", 15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        #row4
        lbl_address=Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salary",font=("goudy old style",15),bg="white").place(x=500,y=270)

        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",15),bg="lightyellow").place(x=600,y=270,width=180)

        #button
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style" ,15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style" ,15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style" ,15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style" ,15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #----employee details(treeview)
        emp_frame=Frame(self.root,bd=3,relief="ridge")
        emp_frame.place(x=0,y=350,relwidth=1,height=150)
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid",text="EMP ID")    
        self.EmployeeTable.heading("name",text="Name")    
        self.EmployeeTable.heading("email",text="Email")    
        self.EmployeeTable.heading("gender",text="Gender")    
        self.EmployeeTable.heading("contact",text="Contact")    
        self.EmployeeTable.heading("dob",text="D.O.B")    
        self.EmployeeTable.heading("doj",text="D.O.J")    
        self.EmployeeTable.heading("pass",text="Password")       
        self.EmployeeTable.heading("utype",text="User Type")    
        self.EmployeeTable.heading("address",text="Address")    
        self.EmployeeTable.heading("salary",text="Salary")      

        self.EmployeeTable.column("eid",width=90)    
        self.EmployeeTable.column("name",width=100)    
        self.EmployeeTable.column("email",width=100)    
        self.EmployeeTable.column("gender",width=100)    
        self.EmployeeTable.column("contact",width=100)    
        self.EmployeeTable.column("dob",width=100)    
        self.EmployeeTable.column("doj",width=100)    
        self.EmployeeTable.column("pass",width=100)       
        self.EmployeeTable.column("utype",width=100)    
        self.EmployeeTable.column("address",width=100)    
        self.EmployeeTable.column("salary",width=100)          
        self.EmployeeTable["show"]="headings"
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.getdata)
        self.show()
    #----------------
    def add(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="" or self.var_contact.get()=="" or self.var_dob.get()=="" or self.var_doj.get()=="" or self.var_email.get()=="" or self.var_gender=="Select" or self.var_name.get()=="" or self.var_pass.get()=="" or self.var_utype.get()=="Select":
                 messagebox.showerror("Error","Some entry is missing",parent=self.root)
            elif len(self.var_contact.get())<10:
                messagebox.showerror("Error","Invalid contact number",parent=self.root)
            elif not self.var_name.get().isalpha():
                messagebox.showerror("Error","Invalid name")
            else:
                cur.execute(("select * from employee where eid=%s"),(self.var_emp_id.get(),))
                row=cur.fetchone()
                print(row)
                if row:
                    messagebox.showerror("Error","This Employee ID already exists",parent=self.root)
                else:
                    cur.execute("Insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.var_emp_id.get(),self.var_name.get(),self.var_email.get(),self.var_gender.get(),self.var_contact.get(),self.var_dob.get(),self.var_doj.get(),self.var_pass.get(),
                    self.var_utype.get(),self.txt_address.get('1.0',END),self.var_salary.get() ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.show()

        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
        finally:
            cur.close()
            con.close()
    
    def show(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()
    def getdata(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete("1.0",END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])

    def update(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="" or self.var_contact.get()=="" or self.var_dob.get()=="" or self.var_doj.get()=="" or self.var_email.get()=="" or self.var_gender=="Select" or self.var_name.get()=="" or self.var_pass.get()=="" or self.var_utype.get()=="Select":
                messagebox.showerror("Error","Some entry is missing",parent=self.root)
            elif len(self.var_contact.get())<10:
                messagebox.showerror("Error","Invalid contact number",parent=self.root)
            elif not self.var_name.get().isalpha():
                messagebox.showerror("Error","Invalid name")
            else:
                cur.execute(("select * from employee where eid=%s"),(self.var_emp_id.get(),))
                row=cur.fetchone()
                
                if row:
                    op=messagebox.askyesno("Update","Are you sure,you want to update?")
                    if op==True:
                        cur.execute("update employee set name=%s,email=%s,gender=%s,contact=%s,dob=%s,doj=%s,pass=%s,utype=%s,address=%s,salary=%s where eid=%s",(self.var_name.get(),self.var_email.get(),self.var_gender.get(),self.var_contact.get(),self.var_dob.get(),self.var_doj.get(),self.var_pass.get(),
                        self.var_utype.get(),self.txt_address.get('1.0',END),self.var_salary.get(),self.var_emp_id.get()))
                        con.commit()
                        messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                        self.show()
                else:
                     messagebox.showerror("Error","This Employee ID do not exists",parent=self.root)
                    
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
        finally:
            cur.close()
            con.close()
    
    def delete(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute(("select * from employee where eid=%s"),(self.var_emp_id.get(),))
                row=cur.fetchone()
                
                if row:
                    op=messagebox.askyesno("Confirm","Are you sure,you want to delete?")
                    if op==True:
                        cur.execute("delete from employee where eid=%s",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Employee Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()
                else:
                     messagebox.showerror("Error","This Employee ID do not exists",parent=self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
    
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Select")
        self.txt_address.delete("1.0",END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("")
        self.show()
    
    def search(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input shoud be required",parent=self.root)
            else:
                # cur.execute("select * from employee where "+self.var_searchby.get()+"LIKE '%"+self.var_searchtxt.get()+"%'")
                # query = "SELECT * FROM employee WHERE %s LIKE %s"
                # cur.execute(query, (self.var_searchby.get().lower(),'%' + self.var_searchtxt.get() + '%',))
                # rows=cur.fetchall()
                search_by = self.var_searchby.get().lower()
                search_txt = '%' + self.var_searchtxt.get() + '%'
                query = f"SELECT * FROM employee WHERE {search_by} LIKE %s"
                cur.execute(query, (search_txt,))
                rows = cur.fetchall()
                if rows:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()

if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()
