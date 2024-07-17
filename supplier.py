from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox,END
import mysql.connector
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+222+140")
        self.root.title("Supplier")
        # self.root.maxsize(1350,700)
        # self.root.minsize(1350,700)
        self.root.focus_force()

        #----All variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
       
        
        #----search frame
        #SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),borderwidth=2,relief="ridge",bg="White")
        #SearchFrame.place(x=250,y=20,width=600,height=70)

        #----options
        lbl_search=ttk.Label(self.root,text="Invoice No.",font=("goudy old style", 15))
        lbl_search.place(x=700,y=80)
        txt_search=Entry(self.root,font=("goudy old style" ,15),textvariable=self.var_searchtxt,bg="white").place(x=800,y=80,width=150)
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style" ,15),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)

        #----title
        title=Label(self.root,text="Supplier Details",font=("goudy old style" ,20,'bold'),bg="#581845",fg="white")
        title.place(x=50,y=10,width=1000)

        #----content
        #row1
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)
        
        #row2
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
       
        #row3
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)
       
        #row4
        lbl_address=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=150)
        
        #button
        btn_save=Button(self.root,text="Save",command=self.add,font=("goudy old style" ,15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style" ,15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style" ,15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style" ,15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)

        #----supplier details(treeview)
        emp_frame=Frame(self.root,bd=3,relief="ridge")
        emp_frame.place(x=700,y=120,width=380,height=350)
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","des"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        self.SupplierTable.heading("invoice",text="Invoice")    
        self.SupplierTable.heading("name",text="Name")    
        self.SupplierTable.heading("contact",text="Contact")    
        self.SupplierTable.heading("des",text="Description")     

        self.SupplierTable.column("invoice",width=90)    
        self.SupplierTable.column("name",width=100)    
        self.SupplierTable.column("contact",width=100)    
        self.SupplierTable.column("des",width=100)    
                
        self.SupplierTable["show"]="headings"
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.getdata)
        self.show()
    #----------------
    def add(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="" or self.var_contact.get()=="" or self.var_name.get()=="" :
                 messagebox.showerror("Error","Some entry is missing",parent=self.root)
            elif len(self.var_contact.get())<10:
                messagebox.showerror("Error","Invalid contact number",parent=self.root)
            elif not self.var_name.get().isalpha():
                messagebox.showerror("Error","Invalid name")
            else:
                cur.execute(("select * from supplier where invoice=%s"),(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                print(row)
                if row:
                    messagebox.showerror("Error","This Invoice no already exists",parent=self.root)
                else:
                    cur.execute("Insert into supplier(invoice,name,contact,des) values(%s,%s,%s,%s)",(self.var_sup_invoice.get(),self.var_name.get(),self.var_contact.get(),self.txt_desc.get('1.0',END), ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
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
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()
    def getdata(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete("1.0",END)
        self.txt_desc.insert(END,row[3])

    def update(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="" or self.var_contact.get()=="" or self.var_name.get()=="" :
                messagebox.showerror("Error","Some entry is missing",parent=self.root)
            elif len(self.var_contact.get())<10:
                messagebox.showerror("Error","Invalid contact number",parent=self.root)
            elif not self.var_name.get().isalpha():
                messagebox.showerror("Error","Invalid name")
            else:
                cur.execute(("select * from supplier where invoice=%s"),(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                
                if row:
                    op=messagebox.askyesno("Update","Are you sure,you want to update?")
                    if op==True:
                        cur.execute ("update supplier set name=%s,contact=%s,des=%s where invoice=%s",(self.var_name.get(),self.var_contact.get(),self.txt_desc.get('1.0',END),self.var_sup_invoice.get()))
                        con.commit()
                        messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                        self.show()
                else:
                     messagebox.showerror("Error","This Invoice no do not exists",parent=self.root)
                    
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
        finally:
            cur.close()
            con.close()
    
    def delete(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be required",parent=self.root)
            else:
                cur.execute(("select * from supplier where invoice=%s"),(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                
                if row:
                    op=messagebox.askyesno("Confirm","Are you sure,you want to delete?")
                    if op==True:
                        cur.execute("delete from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Supplier Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()
                else:
                     messagebox.showerror("Error","This Invoice no.  do not exists",parent=self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
    
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete("1.0",END)
        self.var_searchtxt.set("")
        self.show()
    
    def search(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice no. shoud be required",parent=self.root)
            else:
                # cur.execute("select * from employee where "+self.var_searchby.get()+"LIKE '%"+self.var_searchtxt.get()+"%'")
                cur.execute("SELECT * FROM supplier WHERE invoice=%s",(self.var_searchtxt.get(),))
                
                rows=cur.fetchone()
                print(rows)
                if rows!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=rows)
                    
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()

if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()
