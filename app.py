#! /bin/python3
import random  
import string 
import json
from urllib import response
from flask import Flask, render_template, request, redirect, url_for,session
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wvn94274;PWD=2K5Z7ZiQuEV2edmQ", '', '')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        global rs
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        stmt = ibm_db.prepare(conn, 'SELECT * FROM user WHERE username=?')
        ibm_db.bind_param(stmt, 1, name)
        ibm_db.execute(stmt)
        rs = ibm_db.fetch_assoc(stmt)
        print(rs)
        if rs:
            msg = 'Account already Exists'
            return render_template('register.html', msg=msg)
        else:
            reg_stmt = ibm_db.prepare(conn, 'INSERT INTO user VALUES(?,?,?,?)')
            ibm_db.bind_param(reg_stmt, 1, name)
            ibm_db.bind_param(reg_stmt, 3, email)
            ibm_db.bind_param(reg_stmt, 4, password)
            ibm_db.execute(reg_stmt)
            msg = 'Successfully Registered'
            return render_template('register.html', msg=msg)
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM user WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs :
            role=session['role']='user'
            name=session['name']=name
            print(rs)
            return render_template('cus_dashboard.html',role=role,name=name,j=rs)
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM agent WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs :
            return render_template('agt_dashboard.html')
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM admin WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs :
            return render_template('adm_dashboard.html')
        else:
            msg = 'UID/Password is incorrect'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')


@app.route('/dashboard', methods=['POST','GET'])
def usr_dashboard():
    return render_template('cus_dashboard.html')


@app.route('/dashboard',methods=['POST','GET'])
def agt_dashboard():
    return render_template()


@app


if __name__ == '__main__':
    app.run(debug=True)

# generate random string

def Upper_Lower_string(length): 
    result = ''.join((random.choice(string.ascii_lowercase) for x in range(length))) # run loop until the define length  
    print(" Random string generated in Lowercase: ", result)
    result1 = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) # run the loop until the define length  
    print(" Random string generated in Uppercase: ", result1)