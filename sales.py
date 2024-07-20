from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+222+140")
        self.root.title("Sales")
        self.root.focus_force()

        self.var_invoice=StringVar()
        self.bill_list=[]
        #-----title-----
        lbl_title=Label(self.root,text="View Customer Bills",font=("goudy old style",30),bg='#581845',fg='white').pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_invoice=Label(self.root,text="Invoice No.",font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="light yellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg='white',cursor='hand2').place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="light grey",cursor='hand2').place(x=490,y=100,width=120,height=28)

        #-----Bill List-----
        sales_Frame=Frame(self.root,borderwidth=3,relief="ridge")
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="white")
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        #-----Bill Area-----
        bill_Frame=Frame(self.root,borderwidth=3,relief="ridge")
        bill_Frame.place(x=280,y=140,width=410,height=330)
        lbl_title=Label(bill_Frame,text="View Customer Bills",font=("goudy old style",20),bg='orange',fg='white').pack(side=TOP,fill=X)
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="light yellow")
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.Sales_List.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        self.im1=Image.open("images/salesimg.jpg")
        self.im1=self.im1.resize((390,300))
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=0,relief=RAISED)
        self.lbl_im1.place(x=700,y=140)
        self.show()

    #-----------------
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])
            else:
                messagebox.showerror("Error","Invalid invoice no. ")
    
    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        print(file_name)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
    
    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)

if __name__=="__main__":                                                                                                                                                                                               
    root=Tk()
    obj=salesClass(root)
    root.mainloop()