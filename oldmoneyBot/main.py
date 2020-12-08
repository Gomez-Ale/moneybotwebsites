#pip install flask for thw website
#in a WSL instance, enterthe mnt drive where the file is install, run and visit the given IP
from flask import Flask, render_template, request
import requests
from stock import Stocks
import datetime

app = Flask(__name__)

##Global instances of class
PYTHONBREAKPOINT=0
global stocks1
global stocks2
global stocks3
global stocks4
global stocks5
stocks1 = Stocks("", 0, 0, 0, []) 
stocks2 = Stocks("", 0, 0, 0, []) 
stocks3 = Stocks("", 0, 0, 0, []) 
stocks4 = Stocks("", 0, 0, 0, []) 
stocks5 = Stocks("", 0, 0, 0, [])
global greedyCash
global globalsCash
globalsCash = 0
global initialCash
initialCash = 0
greedyCash = 0 
bstCash = 0
ROItable = []
##Does the ticker calls
def tickerCheck(tickercode, cryptocurrencies, stockClass, money):
	global greedyCash
	global globalsCash
	global stocks1
	global stocks2
	global stocks3
	global stocks4
	global stocks5
	global bstCash
	initialCash = money
	blank = ''
	currency = "/USD"
	if stockClass == 1:
		stocks1.fillIn(tickercode, 0,0,0, [])
	if stockClass == 2:
		stocks2.fillIn(tickercode, 0,0,0, [])
	if stockClass == 3:
		stocks3.fillIn(tickercode, 0,0,0, [])
	if stockClass == 4:
		stocks4.fillIn(tickercode, 0,0,0, [])
	if stockClass == 5:
		stocks5.fillIn(tickercode, 0,0,0, [])	

	if tickercode != blank: 
		if tickercode + currency in cryptocurrencies:
			tickercode = tickercode + currency
			##calls the JSON
		r = requests.get('https://api.twelvedata.com/time_series?symbol='+tickercode+'&interval=1min&outputsize=5000&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		##error check
		try:
			price = float(json_object['values'][0]['open'])			
			ROItable = runningAverage(json_object, tickercode)
			size = len(json_object['values'])
			total = 0.0
			for x in ROItable:
				total = total + float(x)			
			averages = float(total)  / float(size)	
			##buys one fifth of the stock			
			print(initialCash)
			buying = float(initialCash) / (float(price) * 5.0)					
			print (buying)
			if stockClass == 1:
				stocks1.fillIn(tickercode, buying, price, averages, ROItable)
				bstCash = bstCash - (initialCash * 0.2)
			if stockClass == 2:
				stocks2.fillIn(tickercode, buying, price, averages, ROItable)
				bstCash = bstCash - (initialCash * 0.2)
			if stockClass == 3:
				stocks3.fillIn(tickercode, buying, price, averages, ROItable)
				bstCash = bstCash - (initialCash * 0.2)
			if stockClass == 4:
				stocks4.fillIn(tickercode, buying, price, averages, ROItable)
				bstCash = bstCash - (initialCash * 0.2)
			if stockClass == 5:
				stocks5.fillIn(tickercode, buying, price, averages, ROItable)		
				bstCash = bstCash - (initialCash * 0.2)
					
		except :
			print("error found")
			price = 'n/a'
	else:
		price = 'n/a'

	return price

	##Calculate the average
def runningAverage(json_object, tickercode):	
	#r = requests.get('https://api.twelvedata.com/time_series?symbol='+tickercode+'&interval=5min&outputsize=1250&apikey=05f6d37ac5f143ac938d8ee2095128e5')
	#json_object = r.json()	
	#get the average by iterating list
	size = len(json_object['values'])	
	total = 0.0	
	for x in json_object['values']:
		ROItable.append(100* (float(x['close']) - float(x['open'])) / float(x['open'])) 			
	print(tickercode)
	print(total)	
	return ROItable

def updatingTickers(value):
	global greedyCash
	global globalsCash
	global stocks1
	global stocks2
	global stocks3
	global stocks4
	global stocks5	
	
##adds newest data to the value
	if value == 1:		
		ROItable = stocks1.ROItable
		r = requests.get('https://api.twelvedata.com/price?symbol='+stocks1.tickerName+'&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		previousPrice = stocks1.previousPrice
		ROItable.append(json_object['price'])
		currentprice = json_object['price']
		size = len(ROItable)	
		total = 0.0	
		for x in ROItable: 
			total = float(total) + float(ROItable)	
		roi = total / size
		if stock1.averagePrice < 0:
			if roi < 0:
				greedyCash = greedyCash + (currentprice * stocks1.amountOwned)
				stocks1.newOwnership(0, currentprice)
		if stock1.averagePrice > 0:
			if roi > stocks1.averagePrice:
				##sell if roi is above
				greedyCash = greedyCash + (currentprice * stocks1.amountOwned)
				stocks1.newOwnership(0, currentprice)
			if roi < stocks1.averagePrice:
				##sell if roi is above
				amount = (greedyCash / (10 * currentprice))
				greedyCash = greedyCash - (amount * currentprice)
				amount = stocks1.amountOwned + amount
				stocks1.newOwnership(0, amount)
	if value == 2:		
		ROItable = stocks2.ROItable
		r = requests.get('https://api.twelvedata.com/price?symbol='+stocks2.tickerName+'&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		previousPrice = stocks2.previousPrice
		ROItable.append(json_object['price'])
		currentprice = json_object['price']
		size = len(ROItable)	
		total = 0.0	
		for x in ROItable: 
			total = float(total) + float(ROItable)	
		roi = total / size
		if stock1.averagePrice < 0:
			if roi < 0:
				greedyCash = greedyCash + (currentprice * stocks2.amountOwned)
				stocks2.newOwnership(0, currentprice)
		if stock2.averagePrice > 0:
			if roi > stocks2.averagePrice:
				##sell if roi is above
				greedyCash = greedyCash + (currentprice * stocks2.amountOwned)
				stocks2.newOwnership(0, currentprice)
			if roi < stocks2.averagePrice:
				##sell if roi is above
				amount = (greedyCash / (10 * currentprice))
				greedyCash = greedyCash - (amount * currentprice)
				amount = stocks2.amountOwned + amount
				stocks1.newOwnership(0, amount)
	if value == 3:		
		ROItable = stocks3.ROItable
		r = requests.get('https://api.twelvedata.com/price?symbol='+stocks3.tickerName+'&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		previousPrice = stocks3.previousPrice
		ROItable.append(json_object['price'])
		currentprice = json_object['price']
		size = len(ROItable)	
		total = 0.0	
		for x in ROItable: 
			total = float(total) + float(ROItable)	
		roi = total / size
		if stock1.averagePrice < 0:
			if roi < 0:
				greedyCash = greedyCash + (currentprice * stocks3.amountOwned)
				stocks3.newOwnership(0, currentprice)
		if stock2.averagePrice > 0:
			if roi > stocks3.averagePrice:
				##sell if roi is above
				greedyCash = greedyCash + (currentprice * stocks3.amountOwned)
				stocks3.newOwnership(0, currentprice)
			if roi < stocks3.averagePrice:
				##sell if roi is above
				amount = (greedyCash / (10 * currentprice))
				greedyCash = greedyCash - (amount * currentprice)
				amount = stocks3.amountOwned + amount
				stocks1.newOwnership(0, amount)
	if value == 4:		
		ROItable = stocks4.ROItable
		r = requests.get('https://api.twelvedata.com/price?symbol='+stocks4.tickerName+'&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		previousPrice = stocks4.previousPrice
		ROItable.append(json_object['price'])
		currentprice = json_object['price']
		size = len(ROItable)	
		total = 0.0	
		for x in ROItable: 
			total = float(total) + float(ROItable)	
		roi = total / size
		if stock1.averagePrice < 0:
			if roi < 0:
				greedyCash = greedyCash + (currentprice * stocks4.amountOwned)
				stocks4.newOwnership(0, currentprice)
		if stock2.averagePrice > 0:
			if roi > stocks4.averagePrice:
				##sell if roi is above
				greedyCash = greedyCash + (currentprice * stocks4.amountOwned)
				stocks4.newOwnership(0, currentprice)
			if roi < stocks4.averagePrice:
				##sell if roi is above
				amount = (greedyCash / (10 * currentprice))
				greedyCash = greedyCash - (amount * currentprice)
				amount = stocks4.amountOwned + amount
				stocks1.newOwnership(0, amount)
	if value == 5:		
		ROItable = stocks5.ROItable
		r = requests.get('https://api.twelvedata.com/price?symbol='+stocks5.tickerName+'&apikey=05f6d37ac5f143ac938d8ee2095128e5')
		json_object = r.json()
		previousPrice = stocks5.previousPrice
		ROItable.append(json_object['price'])
		currentprice = json_object['price']
		size = len(ROItable)	
		total = 0.0	
		for x in ROItable: 
			total = float(total) + float(ROItable)	
		roi = total / size
		if stock1.averagePrice < 0:
			if roi < 0:
				greedyCash = greedyCash + (currentprice * stocks5.amountOwned)
				stocks5.newOwnership(0, currentprice)
		if stock2.averagePrice > 0:
			if roi > stocks5.averagePrice:
				##sell if roi is above
				greedyCash = greedyCash + (currentprice * stocks5.amountOwned)
				stocks5.newOwnership(0, currentprice)
			if roi < stocks5.averagePrice:
				##sell if roi is above
				amount = (greedyCash / (10 * currentprice))
				greedyCash = greedyCash - (amount * currentprice)
				amount = stocks5.amountOwned + amount
				stocks1.newOwnership(0, amount)


## Create the uying

def emptyInitialCoffers(stockClass, money, value):
	global stocks1
	global stocks2
	global stocks3
	global stocks4
	global stocks5	
	global globalsCash
	global bstCash
	print(globalsCash)
	print(stocks1.amountOwned)
	if stockClass == 1:
		print("previousPrice")
		print(stocks1.previousPrice)
		print(value)
		temp = value * stocks1.previousPrice
		print("temp")
		print(temp)
		buying = float(bstCash) / (float(temp))
		print("buying")
		print (buying)
		newSum = buying + float(stocks1.amountOwned)
		print(newSum)
		stocks1.buy(newSum)		 
	if stockClass == 2:
		buying = float(bstCash) / (value * float(stocks2.previousPrice))
		newSum = buying + stocks2.amountOwned
		stocks2.buy(newSum)
	if stockClass == 3:
		buying = float(bstCash) / (value * float(stocks3.previousPrice))
		newSum = buying + stocks3.amountOwned
		stocks3.buy(newSum)
	if stockClass == 4:
		buying = float(bstCash) / (value * float(stocks4.previousPrice))
		newSum = buying + stocks4.amountOwned
		stocks4.buy(newSum)
	if stockClass == 5:
		buying = float(bstCash) / (value * float(stocks5.previousPrice))
		newSum = buying + stocks5.amountOwned
		stocks5.buy(newSum)


@app.route('/stock', methods=['POST'])
def initialStock():	
	###globals
	global greedyCash
	global globalsCash
	global stocks1
	global stocks2
	global stocks3
	global stocks4
	global stocks5
	global bstCash


	print(request)
	print(request.form)
	#breakpoint()	
	#checks for blanks
	blank = ''
	#check for Cryptos
	currency = "/USD"
	#list of crypto
	cryptoList = []

	#money
	money = float(request.form['money'])		
	globalsCash = money
	initialCash = money


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
	##Runs the setup for each indiviudal stock
	bstCash =globalsCash
	price_1 =  tickerCheck(tickercode1, cryptoList, 1, globalsCash)	
	price_2 =  tickerCheck(tickercode2, cryptoList, 2, globalsCash)	
	price_3 =  tickerCheck(tickercode3, cryptoList, 3, globalsCash)
	price_4 =  tickerCheck(tickercode4, cryptoList, 4, globalsCash)
	price_5 =  tickerCheck(tickercode5, cryptoList, 5, globalsCash)	
	print("initialCash")
	print(initialCash)
	print("bstCash")
	print(bstCash)
	### Identify how many valid tickers exists
	ratio = bstCash /  globalsCash 
	print(ratio)
	value = 5
	if ratio == 0.8:
		value = 1
	if ratio == 0.6:
		value = 2
	if ratio == 0.4:
		value = 3
	if ratio == 0.2:
		value = 4	
		#print(initialCash)
	
	##will buy the remaininng balance
		
	if stocks1.previousPrice > 0:
		emptyInitialCoffers(1, globalsCash, value)		
	if stocks2.previousPrice > 0:
		emptyInitialCoffers(2, globalsCash, value)		
	if stocks3.previousPrice > 0:
		emptyInitialCoffers(3, globalsCash, value)
	if stocks4.previousPrice > 0:
		emptyInitialCoffers(4, globalsCash, value)
	if stocks5.previousPrice > 0:
		emptyInitialCoffers(5, globalsCash, value)
	globalsCash = 0
	tester = 0
	tester = globalsCash
	print("buying done")

		##end

	return render_template('stock.html', greedCash=tester, stock1=stocks1.tickerName, stock2=stocks2.tickerName, stock3=stocks3.tickerName, stock4=stocks4.tickerName, stock5=stocks5.tickerName,  price1=stocks1.previousPrice, price2=stocks2.previousPrice, price3=stocks3.previousPrice, price4=stocks4.previousPrice, price5=stocks5.previousPrice, ownership1=stocks1.amountOwned, ownership2=stocks2.amountOwned, ownership3=stocks3.amountOwned, ownership4=stocks4.amountOwned, ownership5=stocks5.amountOwned, worth1=round(stocks1.previousPrice*stocks1.amountOwned, 3), worth2=round(stocks2.previousPrice*stocks2.amountOwned, 3), worth3=round(stocks3.previousPrice*stocks3.amountOwned, 3), worth4=round(stocks4.previousPrice*stocks4.amountOwned, 3), worth5=round(stocks5.previousPrice*stocks5.amountOwned, 3), averagePrice1=stocks1.averagePrice, averagePrice2=stocks2.averagePrice, averagePrice3=stocks3.averagePrice, averagePrice4=stocks4.averagePrice, averagePrice5=stocks5.averagePrice)
	

@app.route('/stocks', methods=['POST'])
def updates():		
	if stocks1.previousPrice > 0:
		updatingTickers(1)		
	if stocks2.previousPrice > 0:
		updatingTickers(2)		
	if stocks3.previousPrice > 0:
		updatingTickers(3)
	if stocks4.previousPrice > 0:
		updatingTickers(4)
	if stocks5.previousPrice > 0:
		updatingTickers(5)
	return render_template('stock.html', greedCash=globalsCash, stock1=stocks1.tickerName, stock2=stocks2.tickerName, stock3=stocks3.tickerName, stock4=stocks4.tickerName, stock5=stocks5.tickerName,  price1=stocks1.previousPrice, price2=stocks2.previousPrice, price3=stocks3.previousPrice, price4=stocks4.previousPrice, price5=stocks5.previousPrice, ownership1=stocks1.amountOwned, ownership2=stocks2.amountOwned, ownership3=stocks3.amountOwned, ownership4=stocks4.amountOwned, ownership5=stocks5.amountOwned, worth1=round(stocks1.previousPrice*stocks1.amountOwned, 3), worth2=round(stocks2.previousPrice*stocks2.amountOwned, 3), worth3=round(stocks3.previousPrice*stocks3.amountOwned, 3), worth4=round(stocks4.previousPrice*stocks4.amountOwned, 3), worth5=round(stocks5.previousPrice*stocks5.amountOwned, 3), averagePrice1=stocks1.averagePrice, averagePrice2=stocks2.averagePrice, averagePrice3=stocks3.averagePrice, averagePrice4=stocks4.averagePrice, averagePrice5=stocks5.averagePrice)


	#return render_template('stock.html', stock1=stocks1.tickerName, stock2=stocks2.tickerName, stock3=stocks3.tickerName, stock4=stocks4.tickerName, stock5=stocks5.tickerName,  price1=stocks1.previousPrice, price2=stocks2.previousPrice, price3=stocks3.previousPrice, price4=stocks4.previousPrice, price5=stocks5.previousPrice)
# @app.route('/stock')
# def updates():
# 	if request.method == 'POST':
# 		if request.form["Update"] == "Update1":
# 			oldAmount = stocks1.amountOwned
# 			oldAmount = oldAmount + 1
# 			stocks1.buy(oldAmount)
# 	return render_template('stock.html', greedCash=globalsCash, stock1=stocks1.tickerName, stock2=stocks2.tickerName, stock3=stocks3.tickerName, stock4=stocks4.tickerName, stock5=stocks5.tickerName,  price1=stocks1.previousPrice, price2=stocks2.previousPrice, price3=stocks3.previousPrice, price4=stocks4.previousPrice, price5=stocks5.previousPrice, ownership1=stocks1.amountOwned, ownership2=stocks2.amountOwned, ownership3=stocks3.amountOwned, ownership4=stocks4.amountOwned, ownership5=stocks5.amountOwned, worth1=round(stocks1.previousPrice*stocks1.amountOwned, 3), worth2=round(stocks2.previousPrice*stocks2.amountOwned, 3), worth3=round(stocks3.previousPrice*stocks3.amountOwned, 3), worth4=round(stocks4.previousPrice*stocks4.amountOwned, 3), worth5=round(stocks5.previousPrice*stocks5.amountOwned, 3), averagePrice1=stocks1.averagePrice, averagePrice2=stocks2.averagePrice, averagePrice3=stocks3.averagePrice, averagePrice4=stocks4.averagePrice, averagePrice5=stocks5.averagePrice)
@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)