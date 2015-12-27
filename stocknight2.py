from yahoo_finance import Share
from yahoo_finance import Currency
import sys
import time
import cPickle as pickle

class Portfolio:
	"""portfolio class for all stocks"""
	stockDictionary = {}

	@staticmethod
	def addToPortfolio(toAdd):
		Portfolio.stockDictionary[toAdd.name] = toAdd
		print Portfolio.stockDictionary
		pickle.dump(Portfolio.stockDictionary, open("save.p", "wb"))
		

class Stock:
	"""Common base class for all stocks"""
	trackCount = 0
	def __init__(self, name, price, numofStocks):
		self.name = name
		if Share(self.name).get_price() is None:
			self.valid = 0
			print "That does not seem to be a valid stock"
		else:
			print "Now adding "+ self.name
			Stock.trackCount= Stock.trackCount + 1
			self.valid = 1
			self.invested_price = price
			self.amount = numofStocks
			if self.invested_price == -1:
				self.watchOnly = True
			else:
				self.watchOnly = False
			Portfolio.addToPortfolio(self) 
	
	def currentPrice(self):
		self.rate = Share(self.name).get_price()
		print self.rate

	def basicInfoPrint(self):
		print self.currentPrice()

class Currencies:
	"""Common base class for all currencies"""
	trackCount = 0
	def __init__(self,name):
		self.name = name
		if Currency(self.name).get_rate() is None: 
			self.valid = 0
		else:
			Currencies.trackCount=Currencies.trackCount+1
			self.valid = 1
			self.bid = Currency(self.name).get_bid()
			self.ask = Currency(self.name).get_ask()
			self.rate = Currency(self.name).get_rate()
			self.datetime = Currency(self.name).get_trade_datetime()
			Portfolio.addToPortfolio(self)

	def update(self):
		if self.valid == 1:
			self.rate = Currency(self.name).get_rate()


	def basicInfoPrint(self):
		self.update()
		print self.rate

 
def addANewStock():
	print "What stock do you want to add?"
	stockToAdd = raw_input()
	t = True
	while t:
		print "Have you already invested in this stock? [Yes/No]"
		optionYouChose = raw_input().lower()
		if optionYouChose == "yes":
			print "At what price point did you buy each stock?"
			priceToSend = raw_input()
			print "How many stocks did you buy at this price point"
			amountYouBought = raw_input()
			Stock(stockToAdd, priceToSend, amountYouBought)
			print "Your stock "+ stockToAdd +" has been added!"
			print "Do you want to add anything else?"
			loopcontinue = raw_input()
			if loopcontinue.lower() == "no":
				t = False
		elif optionYouChose == "no":
			Stock(stockToAdd, -1, -1)
			print "Your stock " + stockToAdd +" has been added!"
			print "Do you want to add anything else? [Yes/No]"
			loopcontinue = raw_input()
			if loopcontinue.lower() == "no":
				t = False
		else: 
			print "You have entered input that is not valid at this point."
	return 


def addANewCurrency():
	print "What currency do you want to trade for what currency?"
	currencyToProcess = raw_input()
	Currencies(currencyToProcess)
	print currencyToProcess+ " has been added to your portfolio"
	return 

def searchMyPortfolio():
	print "What stock are you looking for?"
	stockToSearchFor = raw_input()
	
	if stockToSearchFor in Portfolio.stockDictionary:
		print Portfolio.stockDictionary[stockToSearchFor].basicInfoPrint()
	else:
		print "That stock isn't in your portfolio. Do you want me to add it?"
		userCommand =raw_input().lower()
		if userCommand == "no" or "n":
			return
		else:
			addANewStock()

def viewStockPerformanceData():
	for key in stockDictionary:
			print 'Stock name: ', key, ' Price: ', Portfolio.stockDictionary[key].basicInfoPrint()

def viewCurrencyPerformanceData():
	for key in currencyDictionary:
		print 'Currency from: ', key[:3], 'to ', key[-3:], 'is at ', Portfolio.stockDictionary[key].basicInfoPrint()

def predictionAlgorithm():
	print "This is the prediction algorithm."
	for key in stockDictionary:
		netchange = float(Share(key).get_200day_moving_avg()) - float(Share(key).get_price())
		if netchange > 0:
			print "Your stock price is less than the 200 day moving average."
			print "We believe the price of ", key," is, overall, decreasing"
		elif netchange < 0:
			print "Your stock price is more than the 200 day moving average."
			print "We believe the price of ", key," is increasing"
		else:
			print "Your investment seems to be safe. It hasn't really had a major increase or decrease."
		time.sleep(5)  		

loopCont = True
try:
	Portfolio.stockDictionary = pickle.load(open("save.p", "rb"))
except IOError:
	pickle.dump(Portfolio.stockDictionary, open("save.p", "wb"))
	Portfolio.stockDictionary = pickle.load(open("save.p", "rb"))

print "Welcome to Stocknight!"
while loopCont: 
	print "If you want to add a new stock to your portfolio, type New Stock"
	print "If you want to add a new currency to your portfolio, type New Currency"
	print "If you want to search your porfolio, type Search"
	print "If you want to view your stock portfolio's performance data, type Current Performance"
	print "If you want to view your currency trades performance data, type Stock Performance data"
	print "To use our future prediction algorithms, type Prediction Algorithm"
	print "To exit, type Exit"

	userCommand =raw_input().lower()

	if userCommand == "new stock":
		addANewStock()
	elif userCommand == "new currency":
		addANewCurrency()
	elif userCommand == "search":
		searchMyPortfolio()
	elif userCommand == "current performance":
		viewPerformanceData()
	elif userCommand == "prediction algorithm":
		predictionAlgorithm()
	elif userCommand == "exit":
		loopCont = False


