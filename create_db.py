import mysql.connector
def create_db():
    con=mysql.connector.connect(host="localhost",database="ims",user="root",password="ominfo")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid int PRIMARY KEY AUTO_INCREMENT,name varchar(20),email varchar(30),gender varchar(6),contact varchar(10),dob varchar(12),doj varchar(12),pass varchar(15),utype varchar(15),address varchar(35),salary int)")
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice int PRIMARY KEY AUTO_INCREMENT,name varchar(20),contact varchar(10),des varchar(30))")
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid int PRIMARY KEY AUTO_INCREMENT,Supplier varchar(20),Category varchar(20),name varchar(20),price varchar(20),qty varchar(20),status varchar(20))")
    con.commit()
create_db()

