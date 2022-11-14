# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


from_email='962219104095@smartinternz.com'
to_emails='berginglobal@gmail.com'
subject='Sending with Twilio SendGrid is Fun'
html_content='<strong>and easy to do anywhere, even with Python</strong>'


def func(from_email,to_emails,subject,html_content):
    message = Mail(
        from_email,
        to_emails,
        subject,
        html_content)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        return True
    except Exception as e:
        print(e.body)

func(from_email,to_emails,subject,html_content)