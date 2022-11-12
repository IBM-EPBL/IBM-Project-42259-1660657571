#!/usr/bin/python3
from flask import Flask,redirect,request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'

@app.route('/')
def welcome():
	return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)

