from flask import Flask, render_template, request, redirect
import sqlite3

con = sqlite3.connect("hospitalmanagement.db",check_same_thread=False)
cur = con.cursor()
listOfTables=con.execute("SELECT name from sqlite_master WHERE type='table' AND name='PATIENT' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    con.execute(''' CREATE TABLE PATIENT(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT,
MOBILENO INTEGER,
AGE INTEGER,
ADDRESS TEXT,
DOB TEXT,
PLACE TEXT,
PINCODE TEXT); ''')
print("Table has created")
app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def adminlogin():
    if request.method =="POST":
        if request.form['username'] != 'admin' or request.form['pass'] != '12345':
            print("Invalid Credentials")
        else:
            return redirect('/dashboard')
    return render_template("/admin.html")


@app.route("/dashboard", methods = ["GET","POST"])
def registrationpage():
    if request.method=="POST":
        getName=request.form["name"]
        getMobileNo=request.form["mobno"]
        getAge=request.form["age"]
        getAddress=request.form["add"]
        getDOB=request.form["dob"]
        getPlace=request.form["place"]
        getPincode=request.form["pin"]
        print(getName)
        print(getMobileNo)
        print(getAge)
        print(getAddress)
        print(getDOB)
        print(getPlace)
        print(getPincode)
        try:
            con.execute(
                "INSERT INTO PATIENT(Name,Mobileno,Age,Address,DOB,Place,Pincode) VALUES ('" + getName + "','" + getMobileNo + "','" + getAge + "','" + getAddress + "','" + getDOB + "','" + getPlace + "','" + getPincode + "')")
            print("Successfully inserted")
            con.commit()
            return redirect('/viewall')
        except Exception as e:
            print(e)
    return render_template("dashboard.html")


@app.route("/search",methods =["GET","POST"])
def searchpage():
    if request.method == "POST":
        getMobileNo = request.form["mobno"]
        print(getMobileNo)
        try:
            query = "SELECT * FROM PATIENT WHERE Mobileno=" + getMobileNo
            print(query)
            cur.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cur.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Mobile number")
            else:
                print(len(result))
                return render_template("search.html", student=result, status=True)

        except Exception as e:
            print(e)
    return render_template("search.html",student=[], status = False)


@app.route("/delete", methods = ["GET","POST"])
def deletepage():
    if request.method == "POST":
        getMobileNo = request.form["mobno"]
        print(getMobileNo)
        try:
            con.execute("DELETE FROM PATIENT WHERE Mobileno =" +getMobileNo)
            print("SUCCESSFULLY DELETED!")
            result = cur.fetchall()
        except Exception as e:
            print(e)

    return render_template("delete.html")



@app.route("/update",methods=["GET","POST"])
def updatepage():
    if request.method == "POST":
        getMobileNo = request.form["mobno"]
        print(getMobileNo)
        try:
            cur.execute("SELECT * FROM PATIENT WHERE MobileNo="+getMobileNo)
            print("Selected a patient")
            result = cur.fetchall()
            if len(result)==0:
                print("Invalid mobile number")
            else:
                print(len(result))
                return render_template("viewupdate.html", student=result)
            return redirect("/viewupdate")
        except Exception as e:
            print(e)
    return render_template("update.html")
@app.route("/viewupdate",methods=["GET","POST"])
def viewupdate():
    if request.method=="POST":
        getName = request.form["name"]
        getMobileNo = request.form["mobno"]
        getAge = request.form["age"]
        getAddress = request.form["add"]
        getDOB = request.form["dob"]
        getPlace = request.form["place"]
        getPincode = request.form["pin"]
        print(getName)
        print(getMobileNo)
        print(getAge)
        print(getAddress)
        print(getDOB)
        print(getPlace)
        print(getPincode)
        try:
            con.execute("UPDATE PATIENT SET Name = '"+getName+"', Age = '"+getAge+"', Address ='"+getAddress+"', DOB = '"+ getDOB+"', Place = '"+getPlace+"', Pincode = '"+getPincode+"' WHERE MobileNo = " +getMobileNo)
            print("SUCCESSFULLY UPDATED")
            con.commit()
            return redirect('/viewall')
        except Exception as e:
            print(e)
    return render_template("viewupdate.html")

@app.route("/viewall")
def viewpage():
    cur = con.cursor()
    cur.execute("SELECT * FROM PATIENT")
    result = cur.fetchall()
    return render_template("viewall.html", student=result)



if __name__=="__main__":
    app.run(debug=True)


