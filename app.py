#!/usr/bin/python3
from flask import Flask
from flask_mail import Mail, Message
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db


def Upper_Lower_string(length):
    result = ''.join((random.choice(string.ascii_uppercase)
                     for x in range(length)))
    return result


app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wvn94274;PWD=2K5Z7ZiQuEV2edmQ", '', '')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shagish.111937@sxcce.edu.in'
app.config['MAIL_PASSWORD'] = 'SX@09/07/2002'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


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
            reg_stmt = ibm_db.prepare(
                conn, 'INSERT INTO user ("USERNAME","EMAIL","PASSWORD") VALUES(?,?,?)')
            ibm_db.bind_param(reg_stmt, 1, name)
            ibm_db.bind_param(reg_stmt, 2, email)
            ibm_db.bind_param(reg_stmt, 3, password)
            ibm_db.execute(reg_stmt)
            msg = 'Successfully Registered'
            return render_template('register.html', msg=msg)
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        customer = list()
        agent = list()
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
            session['customer'] = rs
            print(rs)
            return render_template('dashboard.html')
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM agent WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs:
            cms = ibm_db.exec_immediate(conn, 'SELECT * FROM user')
            agt = ibm_db.exec_immediate(conn, 'SELECT * FROM agent')
            customers = ibm_db.fetch_assoc(cms)
            agents = ibm_db.fetch_assoc(agt)
            while customers:
                customer.append(customers)
                customers = ibm_db.fetch_assoc(cms)
            while agents:
                agent.append(agents)
                agents = ibm_db.fetch_assoc(agt)
            print(customer)
            print(agent)
            session['role'] = 'agent'
            session['name'] = rs['USERNAME']
            session['customer'] = customer
            session['agent'] = agent
            return render_template('dashboard.html')
        log_stmt = ibm_db.prepare(
            conn, 'SELECT * FROM admin WHERE username=? and password=?')
        ibm_db.bind_param(log_stmt, 1, name)
        ibm_db.bind_param(log_stmt, 2, password)
        ibm_db.execute(log_stmt)
        rs = ibm_db.fetch_assoc(log_stmt)
        if rs:
            cms = ibm_db.exec_immediate(conn, 'SELECT * FROM user')
            agt = ibm_db.exec_immediate(conn, 'SELECT * FROM agent')
            customers = ibm_db.fetch_assoc(cms)
            agents = ibm_db.fetch_assoc(agt)
            while customers:
                customer.append(customers)
                customers = ibm_db.fetch_assoc(cms)
            while agents:
                agent.append(agents)
                agents = ibm_db.fetch_assoc(agt)
            print(customer)
            print(agent)
            session['role'] = 'admin'
            session['customer'] = customer
            session['agent'] = agent

            return render_template('dashboard.html', agent=agent, customer=customer)
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
        ibm_db.bind_param(out, 3, session['customer']['USERNAME'])
        status = ibm_db.execute(out)
        if status:
            msg = 'Success ! Your Ticket Nno is :', ticket, 'You can now return to the home page'
            return render_template('success.html', msg=msg)
        else:
            msg = 'Error Submitting your Query'
            return render_template('success.html', msg=msg)


@app.route('/redirect')
def redir():
    return redirect(url_for('home'))


@app.route('/querying', methods=['POST'])
def admin_query():
    msg = ""
    agent = request.form.getlist('agent_name')
    usr_name = request.form.getlist('cus_name')
    emails = request.form.getlist('email')
    for i in range(0, len(agent)):
        if agent[i] != 'none':
            try:
                qr = ibm_db.prepare(
                    conn, "UPDATE USER SET ASSIGNED_AGENT=? WHERE USERNAME=?")
                ibm_db.bind_param(qr, 1, agent[i])
                ibm_db.bind_param(qr, 2, usr_name[i])
                result = ibm_db.execute(qr)
                print(agent[i], usr_name[i], emails[i])
                msg = Message(
                    f'Hello {usr_name[i]}',
                    sender='shagish.111937@sxcce.edu.in',
                    recipients=[f'{emails[i]}']
                )
                msg.body = f'Agent named {agent[i]} alloted to your query.{agent[i]} will be responding you soon within 24 hrs.'
                mail.send(msg)
                msg = 'Allotments updated Successfully'
            except:
                msg = "Error saving allotments/sending emails"
    return render_template('done.html', msg=msg)


@app.route('/executing...', methods=['POST', 'GET'])
def agent_submit_reply():
    names = request.form.getlist('name')
    text = request.form.getlist('text')
    print(names)
    print(text)
    for i in range(0, len(names)):
        if not text[i] == '':
            try:
                sql = 'UPDATE USER SET REPLY=?,REVIEW_STATUS=1 WHERE USERNAME=?'
                query = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(query, 1, text[i])
                ibm_db.bind_param(query, 2, names[i])
                ibm_db.execute(query)
            except:
                msg = 'Error Sending replies'
    return render_template('done.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
