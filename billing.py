from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk,messagebox
import mysql.connector
import time
import os
import tempfile
class billClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.maxsize(1350,700)
        self.root.minsize(1350,700)

        self.var_search=StringVar()
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        self.var_cal_input=StringVar()
        self.cart_list=[]
        self.chk_print=0
        #----Title----
        img=Image.open("images/Cart (2).png")
        img=img.resize((55,55))
        photo=ImageTk.PhotoImage(img)
        self.root.title("Inventory Management System|Developed by Suhani")
        title=Label(self.root,text="Inventory Management System",bg="#581845",fg="#DAF7A6",image=photo,compound=LEFT,font=("times new roman",30,"bold"),padx=15,pady=15)
        title.image=photo
        title.pack(fill=X)

         #----logout button
        log_button=Button(root,text="Logout",command=self.logout,font=("helvetica", 15,"bold"),cursor="hand2",fg="#900C3F",bg="#FFC300",anchor="w",padx=20).place(x=1200,y=10,relwidth=8,height=30)

        #----clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\tDate: DD-MM-YYYY\t\tTime: HH:MM:SS",bg="#581845",fg="#DAF7A6",font=("times new roman",15),padx=5,pady=5)
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #-----Product detail frame
        ProductFrame1=Frame(self.root,bd=4,relief='ridge',bg='white')
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg='#262626',fg='white').pack(side=TOP,fill=X)

        #-----Search frame in product
        ProductFrame2=Frame(ProductFrame1,bd=4,relief='ridge',bg='white')
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg='white',fg='green').place(x=2,y=5)
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg='white',).place(x=2,y=45)

        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg='light yellow').place(x=128,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=('goudy old style',15),bg='#2196f3',fg='white',cursor='hand2').place(x=285,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=('goudy old style',15),bg='#083531',fg='white',cursor='hand2').place(x=285,y=10,width=100,height=25)

        #----billing details(treeview) in product
        ProductFrame3=Frame(ProductFrame1,bd=3,relief="ridge")
        ProductFrame3.place(x=2,y=140,width=398,height=375)
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.cart_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cart_Table.xview)
        scrolly.config(command=self.cart_Table.yview)
        self.cart_Table.heading("pid",text="P ID")    
        self.cart_Table.heading("name",text="Name")    
        self.cart_Table.heading("price",text="Price")    
        self.cart_Table.heading("qty",text="QTY") 
        self.cart_Table.heading("status",text="Status") 

        self.cart_Table.column("pid",width=40)    
        self.cart_Table.column("name",width=100)    
        self.cart_Table.column("price",width=100)    
        self.cart_Table.column("qty",width=40)    
        self.cart_Table.column("status",width=90)  
                
        self.cart_Table["show"]="headings"
        self.cart_Table.pack(fill=BOTH,expand=1)
        self.cart_Table.bind("<ButtonRelease-1>",self.getdata)
        #self.show()
        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",10),bg='white',fg='red').pack(side=BOTTOM,fill=X)

        #------Customer frame
        CustomerFrame=Frame(self.root,bd=4,relief='ridge',bg='white')
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg='light grey').pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg='white').place(x=2,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg='light yellow').place(x=80,y=35,width=180)
       
        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg='white').place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg='light yellow').place(x=380,y=35,width=140)
       
        Cal_Cart_Frame=Frame(self.root,bd=2,relief='ridge',bg='white')
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #-----Calculator Frame
        
        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief='ridge',bg='white')
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        self.var_cal_input_entry=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief='groove',state='normal',justify='right')
        self.var_cal_input_entry.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text=7,font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text=8,font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text=9,font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,cursor='hand2',pady=12).grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text=4,font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text=5,font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text=6,font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,cursor='hand2',pady=12).grid(row=2,column=3)

        btn_1=Button(Cal_Frame,text=1,font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text=2,font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text=3,font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,cursor='hand2',pady=12).grid(row=3,column=3)

        btn_0=Button(Cal_Frame,text=0,font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,cursor='hand2',pady=12,bg='#581845',fg='white').grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='c',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,cursor='hand2',pady=12).grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,cursor='hand2',pady=12).grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,cursor='hand2',pady=12).grid(row=4,column=3)
        
        #-----Cart Frame
        CartFrame=Frame(Cal_Cart_Frame,bd=3,relief="ridge")
        CartFrame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(CartFrame,text="Cart \t Total Product:[0]",font=("goudy old style",15),bg='light grey')
        self.cartTitle.pack(side=TOP,fill=X)
        scrolly1=Scrollbar(CartFrame,orient=VERTICAL)
        scrollx1=Scrollbar(CartFrame,orient=HORIZONTAL)

        self.cartTable=ttk.Treeview(CartFrame,columns=("pid","name","price","qty"),yscrollcommand=scrolly1.set,xscrollcommand=scrollx.set)
        scrollx1.pack(side=BOTTOM,fill=X)
        scrolly1.pack(side=RIGHT,fill=Y)
        scrollx1.config(command=self.cartTable.xview)
        scrolly1.config(command=self.cartTable.yview)
        self.cartTable.heading("pid",text="P ID")    
        self.cartTable.heading("name",text="Name")    
        self.cartTable.heading("price",text="Price")    
        self.cartTable.heading("qty",text="QTY") 
        
        self.cartTable.column("pid",width=40)    
        self.cartTable.column("name",width=90)    
        self.cartTable.column("price",width=90)    
        self.cartTable.column("qty",width=30)    
        
                
        self.cartTable["show"]="headings"
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        #self.show()

        #-----Cart widgets Frame
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
       

        Add_CartWidgetsFrame=Frame(self.root,bd=3,relief="ridge")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg='white').place(x=5,y=5)               
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg='lightyellow',state='readonly').place(x=5,y=35,width=190,height=22)
        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg='white').place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg='lightyellow',state='readonly').place(x=230,y=35,width=150,height=22)
        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg='white').place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg='lightyellow').place(x=390,y=35,width=120,height=22)
        
        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="In Stock", font=("times new roman", 15), bg='white')
        self.lbl_inStock.place(x=5, y=70)
        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor='hand2').place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Add | Update",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor='hand2').place(x=340,y=70,width=180,height=30)
    
        #--------billing area
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=410,height=410)
        bTitle=Label(billFrame,text="Customer Bills",font=("goudy old style",20,"bold"),bg='#262626',fg='white').pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side='right',fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #-----billing button
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=953,y=520,width=390,height=140)
        self.lbl_amnt=Label(billMenuFrame,text='Bill Amnt\n[0]',font=('goudy old style',15,'bold'),bg='#3f51b5',fg='white')
        self.lbl_amnt.place(x=2,y=5,height=70,width=120)

        self.lbl_discount=Label(billMenuFrame,text='Discount\n[5%]',font=('goudy old style',15,'bold'),bg='#3f51b5',fg='white')
        self.lbl_discount.place(x=124,y=5,height=70,width=120)

        self.lbl_net_pay=Label(billMenuFrame,text='Net Pay\n[0]',font=('goudy old style',15,'bold'),bg='#3f51b5',fg='white')
        self.lbl_net_pay.place(x=246,y=5,height=70,width=140)

        btn_print=Button(billMenuFrame,text='Print',command=self.print_bill,font=('goudy old style',15,'bold'),bg='lightgreen')
        btn_print.place(x=2,y=80,height=50,width=120)

        btn_clear_all=Button(billMenuFrame,text='Clear all',command=self.clear_all,font=('goudy old style',15,'bold'),bg='lightgreen')
        btn_clear_all.place(x=124,y=80,height=50,width=120)

        btn_generate=Button(billMenuFrame,text='Gen./Save Bill',command=self.generate_bill,font=('goudy old style',15,'bold'),bg='lightgreen')
        btn_generate.place(x=246,y=80,height=50,width=140)

        #-----footer
        lbl_footer=Label(self.root,text="IMS-Invntory Management System | Developed by Suhani\nFor any tecnical issue contact: 8929677717",font=("times new roman",12),bg="#581845",fg="#FFFFFF")
        lbl_footer.pack(side=BOTTOM,fill=X) 

        self.show()
        self.update_date_time()
    #-------------
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
    def clear_cal(self):
        self.var_cal_input.set('')
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))
    
    def show(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            self.cart_Table.delete(*self.cart_Table.get_children())
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.cart_Table.delete(*self.cart_Table.get_children())
            for row in rows:
                self.cart_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()
    
    def search(self):
        con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input shoud be required",parent=self.root)
            else:
                search_txt = '%' + self.var_search.get() + '%'
                query = f"SELECT pid,name,price,qty,status FROM product WHERE name LIKE %s and status='Active'"
                cur.execute(query, (search_txt,))
                rows = cur.fetchall()
                if rows:
                    self.cart_Table.delete(*self.cart_Table.get_children())
                    for row in rows:
                        self.cart_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()

    def getdata(self,ev):
        f=self.cart_Table.focus()
        content=(self.cart_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_data_cart(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        self.var_qty.set(row[3])
        
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select product from the list",parent=self.root)
        elif self.var_qty.get()=='' :
            messagebox.showerror("Error",'Quantity is required',parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            price_cal=float(self.var_price.get())
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get(),]
            print(self.cart_list)
            price_cal=self.var_price.get()
           
            #-------update cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno("Confirm","Product already present\nDo you want to Update|Remove from the cart list",parent=self.root)
                if op==True:
                    if self.var_qty.get()=='0':
                        self.cart_list.pop(index_)
                            #self.cart_list[index_][2]=price_cal
                    self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-((self.bill_amnt*5)/100)
        self.lbl_amnt.config(text=f"Bill Amnt,Rs\n[{str(self.bill_amnt)}]")
        self.lbl_net_pay.config(text=f"Net pay(Rs.)\n[{str(self.net_pay)}]")
        self.cartTitle.config(text=f"Cart\t Total Product:[{str(len(self.cart_list))}]")
    
    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

    def generate_bill(self):
        print(len(self.var_contact.get()))
        if self.var_cname.get()=="" or self.var_contact.get()=='':
            messagebox.showerror("Error", "Customer Details are required", parent=self.root)
        elif len(self.var_contact.get()) != 10:
            messagebox.showerror("Error", "Invalid contact no.", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Please add product to the cart!!!", parent=self.root)
        else:
            #-------bill top called
            self.bill_top()
            #-------bill middle
            self.bill_middle()
            #-------bill bottom
            self.bill_bottom()
            with open(f'bill/{str(self.invoice)}.txt', 'w') as fp:
                fp.write(self.txt_bill_area.get('1.0', END))
            messagebox.showinfo('Saved', 'Bill has been generated/Saved')
            self.chk_print=1

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
XYZ-Inventory
Phone No. 98725*****, Delhi-125001
{"="*47}
Customer Name: {self.var_cname.get()}
Ph no. : {self.var_contact.get()}
Bill No. {str(self.invoice)}            Date: {str(time.strftime("%d/%m/%Y"))}
{"="*47}
Product Name              QTY        Price
{"="*47}
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{"="*47}
Bill Amount                  Rs.{self.bill_amnt}
Discount                     Rs.{self.discount}
Net Pay                      Rs.{self.net_pay}



        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    def bill_middle(self):
        con=mysql.connector.connect(database='ims',host='localhost',user='root',password='ominfo')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name = row[1]
                qty = int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                else:
                    status='Active'
                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, f"\n{name:<25} {row[3]:<10} Rs.{price}")
                #-----update quantity in product-----
                cur.execute("Update product set qty=%s where pid=%s",(qty,pid))
                cur.execute("update product set status=%s where pid=%s",(status,pid))
                con.commit()
                
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
        finally:
            cur.close()
            con.close()
            self.show()

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
        self.var_qty.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart\t Total Product:[0]")
        self.var_search('')
        self.clear_cart()
        self.show()
        self.show_cart()
    
    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S %p")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\tDate: {date_}\t\tTime: {time_}")
        self.lbl_clock.after(200, self.update_date_time)
    
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror("Print","Please generate bill,to print the receipt",parent=self.root)
            
    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=billClass(root)
    root.mainloop()