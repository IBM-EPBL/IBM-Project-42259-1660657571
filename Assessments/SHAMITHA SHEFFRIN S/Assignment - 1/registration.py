from crypt import methods
from time import gmtime, strftime
from flask import Flask, request, render_template
import pyautogui
import os

app = Flask(__name__)


@app.route('/')
def registration():
    return render_template('register.html')


@app.route('/success', methods=['POST'])
def registered():
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    return render_template('registration_success.html', name=name, contact=contact, email=email, current_directory=os.getcwd(), user=os.getenv('USER'), time=strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()), cursor=pyautogui.position())


if __name__ == '__main__':
    app.run(debug=True)
