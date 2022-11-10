from flask import Flask, request, redirect, render_template
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wvn94274;PWD=2K5Z7ZiQuEV2edmQ", '', '')


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def register():
    if request.method=="POST":
        msg=''
        name = request.form.get('name')
        email = request.form.get('email')
        rollno = request.form.get('rollno')
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
            ibm_db.bind_param(reg_stmt, 2, rollno)
            ibm_db.bind_param(reg_stmt, 3, email)
            ibm_db.bind_param(reg_stmt, 4, password)
            ibm_db.execute(reg_stmt)
            msg = 'Successfully Registered'
            return render_template('register.html', msg=msg)
    else:
        return render_template('register.html')


@app.route('/Login', methods=['POST', 'GET'])
def login():
    if request.method=="POST":
        name = request.form.get('name')
        password = request.form.get('password')
        log_stmt = ibm_db.prepare(conn, 'SELECT * FROM user WHERE username=? and password=?')
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


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
