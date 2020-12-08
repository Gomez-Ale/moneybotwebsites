#pip install flask for thw website
#in a WSL instance, enterthe mnt drive where the file is install, run and visit the given IP
from flask import Flask, render_template, request
import requests
import datetime
import time
from stock import Stocks
app = Flask(__name__)

##Global instances of class

global stocks1
global stocks2
global stocks3
global stocks4
global stocks5
global percentages
percentages = [0, 0, 0, 0, 0, 0, 0]
global dates
dates = [0, 0, 0, 0, 0, 0, 0]
stocks1 = Stocks("", 0) 
stocks2 = Stocks("", 0) 
stocks3 = Stocks("", 0) 
stocks4 = Stocks("", 0) 
stocks5 = Stocks("", 0)
global greedyCash
global globalsCash
globalsCash = 0
global initialCash
initialCash = 0
greedyCash = 0 
bstCash = 0
ROItable = []



##Does the ticker calls
def tickerCheck(tickercode, cryptocurrencies, stockClass, money, value):
	blank = ''
	currency = "/USD"
	price = 0
	if stockClass == 1:
		stocks1.fillIn(tickercode, 0)
	if stockClass == 2:
		stocks2.fillIn(tickercode, 0)
	if stockClass == 3:
		stocks3.fillIn(tickercode, 0)
	if stockClass == 4:
		stocks4.fillIn(tickercode, 0)
	if stockClass == 5:
		stocks5.fillIn(tickercode, 0)	

	if tickercode != blank: 
		if tickercode + currency in cryptocurrencies:
			tickercode = tickercode + currency
			##calls the JSON
		r = requests.get('https://api.twelvedata.com/time_series?symbol='+tickercode+'&interval=1day&outputsize=5000&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		##error check
		try:
			#breakpoint()
			price = float(json_object['values'][0]['open'])	
			size = len(json_object['values'])
			total = 0.0
			###inserting the location of the dates in the array
			for x in json_object['values']:
				dt = x['datetime']
				year, month, day  = (int(x) for x in dt.split('-'))				
				theIndex = datetime.date(year,month,day).weekday()
				
				localPercent = dates[int(theIndex)] * percentages[int(theIndex)]
				if float(x['open']) > float(x['close']):
					localPercent = localPercent - 1
				if float(x['open']) < float(x['close']):
					localPercent = localPercent + 1
				if float(x['open']) != float(x['close']):	
					dates[int(theIndex)] = dates[int(theIndex)] + 1
					percentages[int(theIndex)] = float(localPercent) /float(dates[int(theIndex)])
			if value == 1:
				stocks1.fillIn(tickercode,price, percentages)	
			if value == 2:
				stocks2.fillIn(tickercode,price, percentages)	
			if value == 3:		
				stocks3.fillIn(tickercode,price, percentages)						
			if value == 4:		
				stocks4.fillIn(tickercode,price, percentages)						
			if value == 5:		
				stocks5.fillIn(tickercode,price, percentages)						
			price = json_object['values'][0]['open'] 

		except :
			print("error found")
			price = 'n/a'
	else:
		price = 'n/a'

	return price



@app.route('/stock', methods=['POST'])
def initialStock():	
	print(request)
	print(request.form)
	#breakpoint()	
	tic1 = time.perf_counter()
	tic2 = time.perf_counter()
	tic3 = time.perf_counter()
	tic4 = time.perf_counter()
	tic5 = time.perf_counter()
	#checks for blanks
	blank = ''
	#check for Cryptos
	currency = "/USD"
	#list of crypto
	cryptoList = []

	#money
	globalsCash = 999
	initialCash = 999


	#Ticker Lists
	tickercode1 = request.form['ticker1']
	tickercode2 = request.form['ticker2']
	tickercode3 = request.form['ticker3']
	tickercode4 = request.form['ticker4']
	tickercode5 = request.form['ticker5']

	##This will generate a list of eligible cryptos
	r = requests.get('https://api.twelvedata.com/cryptocurrencies?source=docs')
	json_object = r.json()
	for element in json_object['data']:
		if currency in element['symbol']:			
			cryptoList.append(element['symbol'])	
	####Starts timer here so the crypto adder doesnt factor in		
	tic1 = time.perf_counter()	
	##Runs the setup for each indiviudal stock also the other timer

	price_1 =  tickerCheck(tickercode1, cryptoList, 1, globalsCash, 1)	
	toc1 = time.perf_counter()
	tic2 = time.perf_counter()
	price_2 =  tickerCheck(tickercode2, cryptoList, 2, globalsCash, 2)	
	toc2 = time.perf_counter()
	tic3 = time.perf_counter()
	price_3 =  tickerCheck(tickercode3, cryptoList, 3, globalsCash, 3)
	toc3 = time.perf_counter()
	tic4 = time.perf_counter()
	price_4 =  tickerCheck(tickercode4, cryptoList, 4, globalsCash, 4)
	toc4 = time.perf_counter()
	tic5 = time.perf_counter()
	price_5 =  tickerCheck(tickercode5, cryptoList, 5, globalsCash, 5)	
	toc5 = time.perf_counter()

	##finds the total time
	tictok1 = toc1 - tic1
	tictok2 = toc2 - tic2
	tictok3 = toc3 - tic3
	tictok4 = toc4 - tic4
	tictok5 = toc5 - tic5

	##bool statements for identifying if you should buy
	yesNo1 = ""
	yesNo2 = ""
	yesNo3 = ""
	yesNo4 = ""
	yesNo5 = ""
	if(stocks1.percentages[datetime.datetime.today().weekday()] > 0):
		yesNo1 = "Yes"
	else:
		yesNo1 = "No"
	if(stocks2.percentages[datetime.datetime.today().weekday()] > 0):
		yesNo2 ="Yes"
	else:
		yesNo2 = "No"
	if(stocks3.percentages[datetime.datetime.today().weekday()] > 0):
		yesNo3 = "Yes"
	else:
		yesNo3 = "No"
	if(stocks4.percentages[datetime.datetime.today().weekday()] > 0):
		yesNo4 = "Yes"
	else:
		yesNo4 = "No"
	if(stocks5.percentages[datetime.datetime.today().weekday()] > 0):
		yesNo5 = "Yes"
	else:
		yesNo5 = "No"	
	print("buying done")

		##end

	return render_template('stock.html', bool1 = yesNo1, bool2 = yesNo2, bool3 = yesNo3, bool4 = yesNo4, bool5 = yesNo5,  time1=tictok1, time2=tictok2, time3=tictok3, time4=tictok4, time5=tictok5,  stock1=stocks1.tickerName, stock2=stocks2.tickerName, stock3=stocks3.tickerName, stock4=stocks4.tickerName, stock5=stocks5.tickerName,  price1=stocks1.previousPrice, price2=stocks2.previousPrice, price3=stocks3.previousPrice, price4=stocks4.previousPrice, price5=stocks5.previousPrice, ownership1=stocks1.amountOwned, ownership2=stocks2.amountOwned, ownership3=stocks3.amountOwned, ownership4=stocks4.amountOwned, ownership5=stocks5.amountOwned, worth1=round(stocks1.previousPrice*stocks1.amountOwned, 3), worth2=round(stocks2.previousPrice*stocks2.amountOwned, 3), worth3=round(stocks3.previousPrice*stocks3.amountOwned, 3), worth4=round(stocks4.previousPrice*stocks4.amountOwned, 3), worth5=round(stocks5.previousPrice*stocks5.amountOwned, 3), averagePrice1=stocks1.averagePrice, averagePrice2=stocks2.averagePrice, averagePrice3=stocks3.averagePrice, averagePrice4=stocks4.averagePrice, averagePrice5=stocks5.averagePrice)
	


@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)