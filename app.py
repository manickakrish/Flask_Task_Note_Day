from os import name
from tokenize import Name
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import datetime
import random
from dateutil.relativedelta import relativedelta
from zmq import Message






app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'taskday'

mysql = MySQL(app)

app.secret_key = "wearethey"

info = ""

@app.route("/", methods=["POST","GET"])
def login():
    if request.method == 'POST':
             cur = mysql.connection.cursor()
             email = request.form["VISA"]
             #password = request.form["spassword"]
             session.permanent = True
             sql = "SELECT * FROM `user` WHERE SecretKey='"+email+"' limit 1"
             data = cur.execute(sql)
             if data > 0:
                    cur.execute("SELECT name FROM `user` WHERE SecretKey='"+email+"'")
                    info = cur.fetchone()
                    session["user"] = info
                    cursor = mysql.connection.cursor()
                    cursor.execute("SELECT ID,Name,Tasks,Status,IF(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()) = 0,CONCAT(TIMESTAMPDIFF(MINUTE,Createdon,CURRENT_TIMESTAMP()),' Minutes'),CONCAT(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()),' Hours')) FROM `usertasks` WHERE Name = '"+info[0]+"' ORDER BY ID Desc")
                    displaydata = cursor.fetchall()
                    return render_template('main/index.html',info = info,displaydata=displaydata)
             else:
                    return render_template('signin/index.html', person = 'Secret Key are invalid! Thank You.')
    else:
              #if "user" in session:
               #      return redirect(url_for("info"))
              return render_template('signin/index.html', person = 'Welcome to my portofolio')



@app.route('/main', methods=["POST","GET"])
def index():
    ct = datetime.datetime.now()
    Status = "Uncompleted"
    if request.method == 'POST':
            Name = request.form["PIRName"]
            PIR = request.form["PIR"]
            cursor = mysql.connection.cursor()
            insert_word = "INSERT INTO usertasks (`Name`, `Tasks`, `Status`, `createdon`) VALUES (%s,%s,%s,%s)"          
            cursor.execute(insert_word,(Name,PIR,Status,ct))
            mysql.connection.commit()
            cursor.close()
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT ID,Name,Tasks,Status,IF(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()) = 0,CONCAT(TIMESTAMPDIFF(MINUTE,Createdon,CURRENT_TIMESTAMP()),' Minutes'),CONCAT(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()),' Hours')) FROM `usertasks` WHERE Name = '"+Name+"' ORDER BY ID Desc")
            displaydata = cursor.fetchall()
            return render_template('main/index.html',Message="New! Task Created",displaydata = displaydata)
    else:
            return render_template('main/index.html')
              
    

@app.route('/Change', methods=["POST","GET"])
def ChangeTask():
        cursor = mysql.connection.cursor()
        Name = "Manickavasan"
        cursor.execute("SELECT ID,Name,Tasks,Status,IF(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()) = 0,CONCAT(TIMESTAMPDIFF(MINUTE,Createdon,CURRENT_TIMESTAMP()),' Minutes'),CONCAT(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()),' Hours')) FROM `usertasks` WHERE Name = 'Manickavasan' ORDER BY ID Desc")
        displaydata = cursor.fetchall()
        if request.method == 'POST': 
               RIP = request.form["RIP"]
               update_word = "UPDATE usertasks SET Status = 'Completed' WHERE id = '"+RIP+"'"          
               cursor.execute(update_word)
               mysql.connection.commit()
               cursor.execute("SELECT ID,Name,Tasks,Status,IF(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()) = 0,CONCAT(TIMESTAMPDIFF(MINUTE,Createdon,CURRENT_TIMESTAMP()),' Minutes'),CONCAT(TIMESTAMPDIFF(HOUR,Createdon,CURRENT_TIMESTAMP()),' Hours')) FROM `usertasks` WHERE Name = 'Manickavasan' ORDER BY ID Desc")
               displaydata = cursor.fetchall()
               return render_template('main/index.html',Message="Task Completed",displaydata = displaydata,RIP = RIP)
        else:
               return render_template('main/index.html')
 


 

@app.route("/register", methods=["POST","GET"])
def register():
      if request.method == 'POST':
             ct = datetime.datetime.now()
             n = random.randint(1000,9999)
             user = request.form["name"]
             cur = mysql.connection.cursor()
             sql = "INSERT INTO user(name,secretkey,Createdon) VALUES (%s,%s,%s)"
             cur.execute(sql,(user,n,ct))
             mysql.connection.commit()
             Message = "Account Created Suceess"
             return render_template('Signin/index.html',Message = Message,n=n)

      else:
             return render_template('Signin/index.html')

                    
               
if __name__ == "__main__":
  app.run(debug=True)