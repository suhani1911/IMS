from tkinter import *
from PIL import ImageTk,Image
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import mysql.connector
from tkinter import messagebox
import time
import os
class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.maxsize(1350,700)
        self.root.minsize(1350,700)

        #----Title----
        img=Image.open("Cart (2).png")
        img=img.resize((55,55))
        photo=ImageTk.PhotoImage(img)
        self.root.title("Inventory Management System|Developed by Suhani")
        title=Label(self.root,text="Inventory Management System",bg="#581845",fg="#DAF7A6",image=photo,compound=LEFT,font=("times new roman",30,"bold"),padx=15,pady=15)
        title.image=photo
        title.pack(fill=X)
        

        #----Background image
        # img=Image.open("inventory.jpg")
        # img.resize((1540,700))
        # photo=ImageTk.PhotoImage(img)
        # bg_img=Label(self.root,image=photo)
        # bg_img.image=photo
        # bg_img.pack(fill=X)
        
        
        #----logout button
        log_button=Button(root,text="Logout",command=self.logout,font=("helvetica", 15,"bold"),cursor="hand2",fg="#900C3F",bg="#FFC300",anchor="w",padx=20).place(x=1200,y=10,relwidth=8,height=30)

        #----clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\tDate: DD-MM-YYYY\t\tTime: HH:MM:SS",bg="#581845",fg="#DAF7A6",font=("times new roman",15),padx=5,pady=5)
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #----left menu
        LeftMenu=Frame(self.root,borderwidth=2,bg="#581845")
        LeftMenu.place(x=0,y=98,width=200,height=700)
        lbl_menu=Label(LeftMenu,text="Menu",bg="#E1ACAC",fg="Black",borderwidth=2,relief="ridge",font=("times new roman",25,"bold"),pady=30).pack(fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,bg="#CA8787",font=("times new roman",20,"bold"),pady=12,borderwidth=2,relief="groove",cursor="hand2").pack(fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,bg="#CA8787",font=("times new roman",20,"bold"),pady=12,borderwidth=2,relief="groove",cursor="hand2").pack(fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,bg="#CA8787",font=("times new roman",20,"bold"),pady=12,borderwidth=2,relief="groove",cursor="hand2").pack(fill=X)
        btn_product=Button(LeftMenu,text="Product",command=self.product,bg="#CA8787",font=("times new roman",20,"bold"),pady=12,borderwidth=2,relief="groove",cursor="hand2").pack(fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,bg="#CA8787",font=("times new roman",20,"bold"),pady=12,borderwidth=2,relief="groove",cursor="hand2").pack(fill=X)
        btn_exit=Button(LeftMenu,text="Exit",command=self.root.destroy,bg="#CA8787",font=("times new roman",20,"bold"),pady=12,borderwidth=2,relief="groove",cursor="hand2").pack(fill=X)

        #----#footer
        lbl_footer=Label(self.root,text="IMS-Invntory Management System | Developed by Suhani\nFor any tecnical issue contact: 8929677717",font=("times new roman",12),bg="#581845",fg="#FFFFFF")
        lbl_footer.pack(side=BOTTOM,fill=X)

        #----content
        self.lbl_employee=Label(self.root,text="Total Employee\n[0]",borderwidth=2,relief="ridge",bg="#FFC300",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=250,y=140,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier\n[0]",borderwidth=2,relief="ridge",bg="#FFC300",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=630,y=140,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category\n[0]",borderwidth=2,relief="ridge",bg="#FFC300",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1010,y=140,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product\n[0]",borderwidth=2,relief="ridge",bg="#FFC300",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=430,y=340,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[0]",borderwidth=2,relief="ridge",bg="#FFC300",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=780,y=340,height=150,width=300)
    
        self.update_content()
        
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win) 
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win) 
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win) 
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)
    
    def update_content(self):
        con=mysql.connector.connect(database='ims',host='localhost',user='root',password='ominfo')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n[{str(len(product))}]")

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[{str(len(supplier))}]")

            cur.execute("select * from product")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[{str(len(category))}]")

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_product.config(text=f"Total Employees\n[{str(len(employee))}]")

            self.lbl_sales.config(text=f"Total Sales\n[{str(len(os.listdir('bill')))}]")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
           
        time_ = time.strftime("%I:%M:%S %p")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\tDate: {date_}\t\tTime: {time_}")
        self.lbl_clock.after(200, self.update_content)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")
if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=IMS(root)
    root.mainloop()


