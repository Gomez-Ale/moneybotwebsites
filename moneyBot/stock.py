class Stocks:
	def __init__(self, tickerName, previousPrice, percentages = [0, 0, 0, 0, 0, 0, 0], amountOwned = 0, averagePrice = 0):
		self.tickerName = tickerName
		self.amountOwned = amountOwned
		self.previousPrice = previousPrice
		self.averagePrice = averagePrice
		self.percentages = percentages
	def fillIn(self, tickerName, previousPrice, percentages = [0, 0, 0, 0, 0, 0, 0],amountOwned = 0, averagePrice = 0):
		self.tickerName = tickerName
		self.amountOwned = amountOwned
		self.previousPrice = previousPrice
		self.averagePrice = averagePrice
		self.percentages = percentages
	def newOwnership(self, amountOwned, previousPrice):
		self.amountOwned = amountOwned
		self.previousPrice = previousPrice
	def buy(self, amountOwned):
		self.amountOwned = amountOwned

