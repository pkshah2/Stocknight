from yahoo_finance import Share
from yahoo_finance import Currency
import sys
#!/usr/bin/python

#import MySQLdb

stockDictionary = {} 
currencyDictionary = {} 


class Stock:
	"""Common base class for all stocks"""
	trackCount = 0
	def __init__(self, name):
		self.name = name
		if Share(self.name).get_price() is None:
			self.valid = 0
			print "That does not seem to be a valid stock"
			self.delObj()
		else:
			print "Now adding "+ self.name
			Stock.trackCount= Stock.trackCount + 1
			self.valid = 1
			self.year_high = Share(self.name).get_year_high()
			self.year_low = Share(self.name).get_year_low()

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
	
	def update(self):
		if self.valid==1:
			self.rate = Currency(self.name).get_rate()


	def basicInfoPrint(self):
		self.update()
		print self.rate

 
def addANewStock():
	print "What stock do you want to add?"
	stockToAdd = raw_input()
	stockDictionary[stockToAdd] = Stock(stockToAdd)
	return 

def addANewCurrency():
	print "What currency do you want to trade for what currency?"
	currencyToProcess = raw_input()
	currencyDictionary[currencyToProcess] = Currencies(currencyToProcess)
	print currencyToProcess+ " has been added to your portfolio"
	return 

def searchMyPortfolio():
	print "What stock are you looking for?"
	stockToSearchFor = raw_input()
	
	if stockToSearchFor in stockDictionary:
		print stockDictionary[stockToSearchFor].basicInfoPrint()
	else:
		print "That stock isn't in your portfolio. Do you want me to add it?"
		userCommand =raw_input().lower()
		if userCommand == "no" or "n":
			return
		else:
			addANewStock()
def viewPerformanceData():
	for key in stockDictionary:
			print 'Stock name: ', key, ' Price: ', stockDictionary[key].basicInfoPrint()
	for key in currencyDictionary:
		print 'Currency from: ', key[:3], 'to ', key[-3:], 'is at ', currencyDictionary[key].basicInfoPrint()
  
loopCont = True
while loopCont: 
	print "Welcome to Stocknight!"
	print "If you want to add a new stock to your portfolio, type New Stock"
	print "If you want to add a new currency to your portfolio, type New Currency"
	print "If you want to search your porfolio, type Search"
	print "If you want to view your portfolio performance data, type Current Performance"
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
	elif userCommand == "exit":
		loopCont = False

