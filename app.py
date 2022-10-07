from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def firstfunc():
    return render_template('index.html')

@app.route('/Register')
def register():
    return render_template('register.html')


@app.route('/Success', methods=["POST", "GET"])
def registered():
    uid = request.form.get('uid')
    pwd = request.form.get('passwd')
    return render_template('success.html', uid=uid, pwd=pwd)


@app.route('/Login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
