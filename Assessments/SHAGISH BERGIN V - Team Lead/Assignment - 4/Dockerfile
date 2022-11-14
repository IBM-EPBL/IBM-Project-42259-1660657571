FROM python:3.6
WORKDIR /home
ADD . /home
COPY requirements.txt /home
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3",'app.py' ]
