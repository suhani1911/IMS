from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox,END
import mysql.connector
class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+222+140")
        self.root.title("Category")
        # self.root.maxsize(1350,700)
        # self.root.minsize(1350,700)
        self.root.focus_force()
        self.var_name=StringVar()
        #-----title
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg='#581845',fg='white').pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg='white').place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",25),bg='light yellow').place(x=50,y=170,width=300)

        btn_add=Button(self.root,text='Add',command=self.add,font=("goudy old style",25),bg='#4caf50',fg="white",cursor='hand2').place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text='Delete',command=self.delete,font=("goudy old style",25),bg='red',fg="white",cursor='hand2').place(x=520,y=170,width=150,height=30)

        cat_frame=Frame(self.root,bd=3,relief="ridge")
        cat_frame.place(x=700,y=100,width=380,height=100)
        scrolly=Scrollbar(cat_frame,orient=VERTICAL) 
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        self.CategoryTable.heading("cid",text="C ID")    
        self.CategoryTable.heading("name",text="Name")    
             

        self.CategoryTable.column("cid",width=90)    
        self.CategoryTable.column("name",width=100)    
        
                
        self.CategoryTable["show"]="headings"
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.getdata)
        self.show()

        #-----images
        self.im1=Image.open("WhatsApp Image 2024-07-11 at 10.31.55_ee50ba08.jpg")
        self.im1=self.im1.resize((500,200))
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open("WhatsApp Image 2024-07-11 at 10.31.55_ff24599c.jpg")
        self.im2=self.im2.resize((500,200))
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)

    #---------------------
    def add(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_name.get()==""  :
                    messagebox.showerror("Error","No category name mentioned",parent=self.root)
            elif not self.var_name.get().isalpha():
                messagebox.showerror("Error","Invalid name")
            else:
                cur.execute(("select * from category where name=%s"),(self.var_name.get(),))
                row=cur.fetchone()
                print(row)
                if row:
                   messagebox.showerror("Error","Category already present",parent=self.root)
                else:
                    cur.execute("Insert into category(name) values(%s)",(self.var_name.get(), ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
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
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()
    def getdata(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        print(row)
        self.var_name.set(row[1])
   
    def delete(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Select category from the list",parent=self.root)
            else:
                cur.execute(("select * from category where name=%s"),(self.var_name.get(),))
                row=cur.fetchall()
                
                if row:
                    op=messagebox.askyesno("Confirm","Are you sure,you want to delete?")
                    if op==True:
                        cur.execute("delete from category where name=%s",(self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Category Deleted Successfully",parent=self.root)
                        self.show()
                        self.clear()
                else:
                     messagebox.showerror("Error","This category do not exists",parent=self.root)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}")
    
    def clear(self):
        self.var_name.set("") 
        self.show()
        

   
if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()
