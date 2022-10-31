#! /bin/python3

import random
import string
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db


def Upper_Lower_string(length):
    result = ''.join((random.choice(string.ascii_uppercase)
                     for x in range(length)))  # run the loop until the define length
    return result


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
        if rs:
            session['role'] = 'user'
            session['name'] = rs['USERNAME']
            session['ticket'] = rs['TICKET']
            session['review'] = rs['REVIEW_STATUS']
            session['query'] = rs['QUERY']
            print(rs)
            return render_template('dashboard.html',
                                   role=session['role'],
                                   name=session['name'],
                                   ticket=session['ticket'],
                                   review=session['review'],
                                   query=session['query'])
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM agent WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs:
            return render_template('dashboard.html')
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM admin WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs:
            return render_template('dashboard.html')
        else:
            msg = 'UID/Password is incorrect'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')


@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == "POST":
        ticket = session['ticket'] = Upper_Lower_string(16)
        print(ticket, session['ticket'])
        query = request.form['query']
        sql = "UPDATE user SET QUERY=?,TICKET=? WHERE USERNAME=?"
        out = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(out, 1, query)
        ibm_db.bind_param(out, 2, session['ticket'])
        ibm_db.bind_param(out, 3, session['name'])
        status = ibm_db.execute(out)
        if status:
            msg = 'Success ! Your Ticket Nno is :', ticket, 'You can now return to the home page'
            return render_template('success.html', msg=msg)
        else:
            msg = 'Error Submitting your Query'
            return render_template('success.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
