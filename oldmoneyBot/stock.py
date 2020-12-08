class Stocks:
	def __init__(self, tickerName, amountOwned, previousPrice, averagePrice, roiTable):
		self.tickerName = tickerName
		self.amountOwned = amountOwned
		self.previousPrice = previousPrice
		self.averagePrice = averagePrice
		self.roiTable = roiTable
	def fillIn(self, tickerName, amountOwned, previousPrice, averagePrice, roiTable):
		self.tickerName = tickerName
		self.amountOwned = amountOwned
		self.previousPrice = previousPrice
		self.averagePrice = averagePrice
		self.roiTable = roiTable
	def newOwnership(self, amountOwned, previousPrice):
		self.amountOwned = amountOwned
		self.previousPrice = previousPrice
	def buy(self, amountOwned):
		self.amountOwned = amountOwned
	def appendTable(self, roiTable):
		self.roiTable = roiTable
