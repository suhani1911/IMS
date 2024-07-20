from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+222+140")
        self.root.title("Product")
        self.root.focus_force()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_cat_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.cat_list=[]
        self.sup_list=[]

        product_Frame=Frame(self.root,borderwidth=3,relief=RIDGE)
        product_Frame.place(x=10,y=10,width=450,height=480)

        #-----title-----
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style" ,18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)
        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=310)

        
        #----column2----
        self.fetch_cat_sup()
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,bg='light yellow',font=("goudy old style",15))
        txt_name.place(x=150,y=160,width=200)

        txt_price=Entry(product_Frame,textvariable=self.var_price,bg='light yellow',font=("goudy old style",15))
        txt_price.place(x=150,y=210,width=200)

        txt_qty=Entry(product_Frame,textvariable=self.var_qty,bg='light yellow',font=("goudy old style",15))
        txt_qty.place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_cat_status,values=("Select","Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #-----button----
        btn_save=Button(product_Frame,text="Save",command=self.add,font=("goudy old style" ,15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style" ,15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style" ,15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style" ,15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #-----search frame
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),borderwidth=2,relief="ridge",bg="White")
        SearchFrame.place(x=480,y=10,width=600,height=70)
        cmb_search=ttk.Combobox(SearchFrame,values=("Select","Category","Supplier","Name"),textvariable=self.var_searchby,state="readonly",justify=CENTER,font=("goudy old style", 12))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        txt_search=Entry(SearchFrame,font=("goudy old style" ,15),textvariable=self.var_searchtxt,bg="white").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style" ,15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #------product details-----
        p_frame=Frame(self.root,bd=3,relief="ridge")
        p_frame.place(x=480,y=100,width=600,height=390)
        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(p_frame,columns=("pid","Supplier","Category","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid",text="P ID")    
        self.productTable.heading("Category",text="Category")    
        self.productTable.heading("Supplier",text="Supplier")    
        self.productTable.heading("name",text="Name")    
        self.productTable.heading("price",text="Price")    
        self.productTable.heading("qty",text="Quantity")    
        self.productTable.heading("status",text="Status")       

        self.productTable.column("pid",width=90)    
        self.productTable.column("Category",width=100)    
        self.productTable.column("Supplier",width=100)    
        self.productTable.column("name",width=100)    
        self.productTable.column("price",width=100)    
        self.productTable.column("qty",width=100)    
        self.productTable.column("status",width=100)             
        self.productTable["show"]="headings"
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.getdata)
        self.show()
        

    #-----------
    def fetch_cat_sup(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            cur.execute(("select name from category "))
            cat=cur.fetchall()
            cat_list=[]
            self.cat_list.append("Empty")
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur.execute(("select name from supplier"))
            sup=cur.fetchall()
            sup_list=[]
            self.sup_list.append("Empty")
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
    
    def add(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=='Empty' or self.var_sup.get()=="Select" or self.var_name.get()=="":
                 messagebox.showerror("Error","Some entry is missing",parent=self.root)
            else:
                cur.execute(("select * from product where name=%s"),(self.var_name.get(),))
                row=cur.fetchone()
                print(row)
                if row:
                    messagebox.showerror("Error","Product already present",parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Supplier,name,price,qty,status) values(%s,%s,%s,%s,%s,%s)",(self.var_cat.get(),self.var_sup.get(),self.var_name.get(),self.var_price.get(),self.var_qty.get(),self.var_cat_status.get()) )
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
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
            cur.execute("select * from product ")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()
    def getdata(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        print(row)
        self.var_pid.set(row[0])
        self.var_cat.set(row[2])
        self.var_sup.set(row[1])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_cat_status.set(row[6])
        

    def update(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="" or  self.var_name.get()=="" or self.var_cat=="Select" or self.var_sup=="Select":
                messagebox.showerror("Error","Some entry is missing",parent=self.root)
            else:
                cur.execute(("select * from product where pid=%s"),(self.var_pid.get(),))
                row=cur.fetchone()
                
                if row:
                    op=messagebox.askyesno("Update","Are you sure,you want to update?")
                    if op==True:
                        cur.execute("update product set Category=%s,Supplier=%s,name=%s,price=%s,qty=%s,status=%s where pid=%s",(self.var_cat.get(),self.var_sup.get(),self.var_name.get(),self.var_price.get(),self.var_qty.get(),self.var_cat_status.get(),self.var_pid.get()))
                        con.commit()
                        messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                        self.show()
                else:
                     messagebox.showerror("Error","This Product do not exist",parent=self.root)
                    
        except Exception as ex: 
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
        finally:
            cur.close()
            con.close()
    
    def delete(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Product ID must be required",parent=self.root)
            else:
                cur.execute(("select * from product where pid=%s"),(self.var_pid.get(),))
                row=cur.fetchone()
                
                if row:
                    op=messagebox.askyesno("Confirm","Are you sure,you want to delete?")
                    if op==True:
                        cur.execute("delete from product where pid=%s",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Product Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()
                else:
                     messagebox.showerror("Error","This Product ID do not exists",parent=self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
    
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_cat_status.set("Select")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
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
                query = f"SELECT * FROM product WHERE {search_by} LIKE %s"
                cur.execute(query, (search_txt,))
                rows = cur.fetchall()
                if rows:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()

        
if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=productClass(root)
    root.mainloop()
