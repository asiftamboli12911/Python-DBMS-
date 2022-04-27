#http://127.0.0.1:5000 (local server link)
from flask import *
import pymysql as pm

db=pm.connect(host="localhost",
              user="root",
              password="",
              database="wonderlist")
cursor=db.cursor()

app=Flask(__name__)
app.secret_key = "xyz123"

@app.route("/")
def hello_world():
    return render_template("home_details.html")

@app.route("/about")
def about():
    return render_template("about_details.html")

@app.route("/players")
def players():
    qr="SELECT * FROM details"
    cursor.execute(qr)
    result=cursor.fetchall()
    return render_template("players_details.html",data=result)

@app.route("/addathlets",methods=["POST"])
def addathletes():
    athletes=request.form['athletes']
    grade=request.form['grade']
    salary=request.form['salary']
    contact=request.form['contact']
    email=request.form['email']
    password=request.form['password']
    birthdate=request.form['birthdate']
    insq="INSERT INTO details(athletes,grade,salary,contact,email,password,birthdate) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(athletes,grade,salary,contact,email,password,birthdate)
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for("players"))
    
    except:
        db.rollback()
        return "Error in query"
    
@app.route("/delete")
def delete():
    id=request.args['id']
    delq="DELETE FROM details WHERE id={}".format(id)
    try:
        cursor.execute(delq)
        db.commit()
        return redirect(url_for("players"))
    
    except:
        db.rollback()
        return "Error in query"
    
@app.route("/edit")
def edit():
    id=request.args['id']
    singleqr="SELECT * FROM details WHERE id={}".format(id)
    cursor.execute(singleqr)
    single_res=cursor.fetchone()
    return render_template("edit_details.html",singleuser=single_res)

@app.route("/update",methods=["POST"])
def update():
    athletes=request.form['athletes']
    grade=request.form['grade']
    salary=request.form['salary']
    contact=request.form['contact']
    email=request.form['email']
    password=request.form['password']
    birthdate=request.form['birthdate']
    uid=request.form['uid']
    upq="UPDATE details SET athletes='{}',grade='{}',salary='{}',contact='{}',email='{}',password='{}',birthdate='{}' WHERE id='{}'".format(athletes,grade,salary,contact,email,password,birthdate,uid)
 
    try:
        cursor.execute(upq)
        db.commit()
        return redirect(url_for("players"))
    except:
        db.rollback()
        return "Error in query"
    
@app.route("/login")
def login():
    return render_template('login_details.html')

@app.route("/logout")
def logout():
    if 'athletes' in session:
        session.pop('athletes')
        return redirect(url_for("login"))
    
@app.route("/check", methods=["POST"])
def check():
    athletes=request.form['athletes']
    password=request.form['password']
    checkq="SELECT * FROM details WHERE athletes='{}' AND password='{}'".format(athletes,password)
    cursor.execute(checkq)
    data=cursor.fetchall()
    if len(data)>0:
        session['athletes'] = data[0][1]
        return redirect(url_for("players"))
    else:
        return "Login failed"

       
if __name__=="__main__":
    app.run(debug=True)

