#!/usr/bin/python3
import ibm_db
import os
os.chdir('/home/bergin/customer care registry/Final Deliverables')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wvn94274;PWD=2K5Z7ZiQuEV2edmQ", '', '')
cms = ibm_db.exec_immediate(conn, 'SELECT * FROM user')
agt = ibm_db.exec_immediate(conn, 'SELECT * FROM agent')
customers = ibm_db.fetch_assoc(cms)
agents = ibm_db.fetch_assoc(agt)
customer=list()
agent=list()
i=0
print('Customer List:\n')
while customers:
    customer.append(customers)
    customers = ibm_db.fetch_assoc(cms)
print(customer,'\n')
print('Agent List:\n')
while agents:
    agent.append(agents)
    agents = ibm_db.fetch_assoc(agt)
print(agent)
