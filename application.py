import smtplib
import requests
from flask import Flask, redirect, url_for, render_template, request, flash
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask_apscheduler import APScheduler

cluster = MongoClient("mongodb+srv://Amazon:Amazon000@amazon-ken5h.mongodb.net/Amazon?retryWrites=true&w=majority")
db = cluster["amazon"]
collection = db["user"]
application = app = Flask(__name__)
scheduler = APScheduler()
@app.route('/')
def index():	
 	return render_template("index.html")

@app.route('/TryNow',methods=["POST","GET"])
def index1():
	if request.method == "POST":
		collection.insert_one(request.form.to_dict())
		return redirect(url_for("user"))
	else:	
 		return render_template("index1.html")
@app.route('/h')
def index2():
	print("heyyyyyyyy")
	for a in collection.find({}):
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
		url = a['URL']
		page = requests.get(url,headers=headers)
		Soup = BeautifulSoup(page.text,"html.parser")
		price = Soup.findAll('span',{'class':"a-size-medium a-color-price priceBlockBuyingPriceString"})
		def send_mail():
			server = smtplib.SMTP('smtp.gmail.com',587)
			server.ehlo()
			server.starttls()
			server.ehlo()
			server.login("amazonpricemonit@gmail.com","dghxwfkefupwacfa")
			subject = "Price Decreased"
			body = "You can buy Your Amazon Product.\nThe price of the product is Decreased Now."+ a['URL']
			msg = f"Subject:{subject}\n\n{body}"
			server.sendmail("pallavarun457@gmail.com",a['Email'],msg)
			server.quit()
		if len(price)==1:
			c=price[0].text[2:].replace(',',"")
			c=float(c)
			budget = float(a['Budget']) 
			if c <= budget:
				send_mail()
				collection.delete_one(a)
@app.route("/user")
def user():
	return render_template("index2.html")

@app.before_first_request
def initialize():
	scheduler.add_job(id = 'Scheduler task',func = index2,trigger = 'interval',seconds = 5)
	scheduler.start()

if __name__=="__main__":
	app.run(debug = True)
