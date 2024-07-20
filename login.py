from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector
import os
import email_pass
import smtplib
import time
class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System|Developed By Suhani")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg='white')
        self.otp=''
        #images---
        img=Image.open("images/phone.jpg")
        img=img.resize((325,560))
        self.phone_image=ImageTk.PhotoImage(img)
        self.lbl_phone_image=Label(self.root,image=self.phone_image,bd=0).place(x=300,y=80)

        #----login frame
        self.employee_id=StringVar()
        self.password=StringVar()
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        login_frame.place(x=650,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",bg='white',font=("Elephant",30,'bold')).place(x=0,y=30,relwidth=1)
        lbl_user=Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#567171").place(x=50,y=100)
       
        txt_user_name=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#567171").place(x=50,y=200)
        txt_user_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground='#00B0F0',fg='white',activeforeground='white',cursor='hand2').place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=50,y=370,width="250",height='2')
        orr=Label(login_frame,text="OR",bg="white",fg='lightgray',font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_forget=Button(login_frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bd=0,bg='white',fg="#00759E",activebackground='white',activeforeground="#00759E").place(x=100,y=390)

        #----frame 2
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        register_frame.place(x=650,y=570,width=350,height=60)
        lbl_reg=Label(register_frame,text="SUBSCRIBE | LIKE | SHARE",font=("times new roman",13),bg="white").place(x=40,y=20)
         #----animation images

        img=Image.open("images/login1.png")
        img=img.resize((290,540))
        self.im1=ImageTk.PhotoImage(img)
        

        img=Image.open("images/login2.png")
        img=img.resize((290,540))
        self.im2=ImageTk.PhotoImage(img)
       
        img=Image.open("images/login3.png")
        img=img.resize((290,540))
        self.im3=ImageTk.PhotoImage(img)

        self.lbl_change_img=Label(self.root,bg='white')
        self.lbl_change_img.place(x=330,y=105,width=275,height=510)
        self.animate()
        
        
    #-----------------
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_img.config(image=self.im)
        self.lbl_change_img.after(2000,self.animate)
    
    def login(self):
        con = mysql.connector.connect(database='ims', host='localhost', user='root', password='ominfo')
        cur = con.cursor()
        try:
            if self.employee_id.get() == '' or self.password.get() == '': 
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:  
                cur.execute("select utype from employee where eid=%s AND pass=%s", (self.employee_id.get(), self.password.get()))  
                user = cur.fetchone()
                print(user)
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
                else:
                    if user[0]=="Admin":  
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def forget_window(self):
        con=mysql.connector.connect(database='ims',user='root',host='localhost',password='ominfo')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=%s",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID,try again",parent=self.root)
                else:
                    #-------forget window
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    #-----call send email function
                    chk=self.send_email(email[0])
                    if chk!='s':
                        messagebox.showerror("Error","Connection Error,try again",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()
                        
                        title=Label(self.forget_win,text="Reset Password",font=('goudy old style',15,'bold'),bg="#3f51b5",fg='white')
                        title.pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP Sent on Registered Email",font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.forget_win,text="SUBMIT",command=self.validate_otp,font=("times new roman",15),bg="lightblue")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15)).place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=190,width=250,height=30)
                    
                        lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15)).place(x=20,y=225)
                        txt_c_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="lightyellow").place(x=20,y=255,width=250,height=30)
                    
                        self.btn_update=Button(self.forget_win,text="Update",command=self.update_password,state='disabled',font=("times new roman",15),bg="lightblue")
                        self.btn_update.place(x=150,y=300,width=100,height=30)
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error",f"Error due to :",parent=self.root)
    def signup(self):
        messagebox.showinfo("Info","SIGN UP",parent=self.root)
    
    def send_email(self,to_):
        pass
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_
        s.login(email_,pass_)
        self.otp=str(time.strftime("%H%S%M"))+str(time.strftime("%S"))
        subj="IMS-Reset Password OTP"
        msg=f"Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team"
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return 's'
        else:
            return 'f'
    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state='disabled')
        else:
            messagebox.showerror("Error","Invalid OTP,Try Again",parent=self.forget_win)
    
    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error","Password & confirm password should be same",parent=self.root)
        else:
            con=mysql.connector.connect(host='localhost',user='root',password='ominfo',database='ims')
            cur=con.cursor()
            try:
                cur.execute("update employee set pass=%s where eid=%s",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated successfully",parent=self.forget_win)
                self.forget_win.destory()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
    



root=Tk()
obj=Login_System(root)
root.mainloop()