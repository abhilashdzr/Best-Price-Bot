'''
This is main program which will take url for keeping
track of price of your favourite product and it will
plot its price history plot  
Author : Abhilash Sinha (abhilashdzr)
Date : 9th Dec, 2021
'''

# from itertools import product
from flask import Flask, render_template,request

import validators
from bs4 import BeautifulSoup
import requests
# import smtplib
import datetime
import os
import csv
# import time

import pandas as pd
import plotly.express as px
from apscheduler.schedulers.background import BackgroundScheduler
import glob
import plotly.graph_objects as go

import urllib.parse

from werkzeug.utils import redirect
import smtplib
from smtplib import SMTPException

def notify_user(name,url,limit,email):
    sender = 'from@fromdomain.com'
    receivers = ['to@todomain.com']

    message = "Fuck off motherfucker"

    try:
        smtpObj = smtplib.SMTP('localhost',port = 1045)
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")

    except:
        print ("Error: unable to send email")


def repeat():
    """ Function to repeat the scraping """
    df = pd.read_csv("./Database.csv")
    print("repetition")
    for _,row in df.iterrows():
        price,product = check_price(row[1])
        if price <= row[2]:
            print("price fall")
            notify_user(row[0],row[1],row[2],row[3])
        store_price(product,price,row[1],row[2],row[3])
        

sched = BackgroundScheduler(daemon=True)
sched.add_job(repeat,'interval',minutes=1)
sched.start()

app = Flask(__name__)

def store_price(prod_name,price,url,limit,email):
    path = "./"+prod_name.replace(' ','_').replace('/','_')+".csv"
    if not os.path.exists(path):
        with open("./Database.csv",'a') as file:
            writer = csv.writer(file,lineterminator ="\n")
            entry = [prod_name,url,limit,email]
            writer.writerow(entry)

        with open(path,'w') as file:
            writer = csv.writer(file,lineterminator ="\n")
            headings = ["Timestamps", "price(INR)"]
            writer.writerow(headings)
    
    else:
        print("exists")
        df = pd.read_csv("./Database.csv")
        for ind,_ in df.iterrows():
            df.at[ind,"Limit"] = limit
            df.at[ind,"Email"] = email

    if price<=limit:
        notify_user(prod_name,url,limit,email)

    with open(path,'a') as file:
        writer = csv.writer(file,lineterminator ="\n")
        timestamp = f"{datetime.datetime.date(datetime.datetime.now())} , {datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp,price])
        print("Added entry to csv file")

def check_price(url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    webpage = requests.get(url, headers = headers)

    bs = BeautifulSoup(webpage.content,'html.parser')
    
    prod_name = bs.find('span',{"class":"B_NuCI"}).get_text()
    price = (float)(bs.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()[1:].replace(',',''))

    print(prod_name)
    return price,prod_name

@app.route('/',methods=['GET','POST'])
def main():
    if request.method=='POST':
        # if request.form['target_url']==' ':
        #     return render_template('index.html')
        valid = validators.url(request.form['target_url'])
        if valid==True:
            price,product = check_price(request.form['target_url'])
            store_price(product,price,request.form['target_url'],float(request.form['limit']),request.form['email'])
            return redirect('./'+product.replace(' ','_').replace('/',"_"))
        else:
            return render_template('alert.html')

    return render_template('index.html')

@app.route('/<product>')
def prod_page(product):
    # print(urllib.parse.unquote(product))
    prod = glob.glob(urllib.parse.unquote(product)+".csv",recursive=True)
    # print(prod[0])
    print(prod)

    filename = prod[0]
    
    df = pd.read_csv(filename)

    fig = go.Figure([go.Scatter(x=df['Timestamps'], y=df['price(INR)'],fill='tozeroy')],)
    fig.update_xaxes(title = "Timeline",showticklabels = False)
    fig.update_yaxes(title = "Price")
    fig.update_layout(title = filename[:-4])
    fig.show()
    print("till this point")
    return render_template('index.html')

@app.route('/updateDatabase')
def update():
    with open('./Database.csv','r') as f:
        data_entry = csv.reader(f)
        for entry in data_entry:
            price,product = check_price(entry[0])
            path = "./"+product.replace(' ','_')+".csv"
            with open(path,'a') as file:
                writer = csv.writer(file,lineterminator ="\n")
                timestamp = f"{datetime.datetime.date(datetime.datetime.now())} , {datetime.datetime.time(datetime.datetime.now())}"
                writer.writerow([timestamp,price])
    
    return "Successfully updated all the csv files!"




if __name__ == "__main__":
    app.run(debug=False)
