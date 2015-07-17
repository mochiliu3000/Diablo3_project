####### 1. Crawl Leader Board online
# Require Python 3.x
# pip install requests; pip install beautifulsoup4;
# use D3; db.dropDatabase();
import requests
from bs4 import BeautifulSoup
import re

def leaderBoardCrawler(url, maxItems):
	sourceCode = requests.get(url)
	soupObj = BeautifulSoup(sourceCode.text)
	profileResult = soupObj.findAll('a', {'class': 'icon-profile'})	
	tierResult = soupObj.findAll('td', {'class': 'cell-RiftLevel'})
	timeResult = soupObj.findAll('td', {'class': 'cell-RiftTime'})
	completedTimeResult = soupObj.findAll('td', {'class': 'cell-CompletedTime'})	
	numItems = min(len(profileResult), maxItems)
	resultList = []
	print("\r\n-----1. Started crawling LeaderBoard website-----")
	for i in range(numItems):
		dict = {}
		href = profileResult[i].get('href')
		r = re.compile('profile\/')
		if href:
			userTagIndex = r.search(href).end()
			userTag = href[userTagIndex:-1]
			dict["_id"] = i + 1
			dict["name"] = userTag
			dict["tier"] = tierResult[i].contents[0].replace("\n", "")
			dict["time"] = timeResult[i].contents[0].replace("\n", "")
			dict["completeTime"] = completedTimeResult[i].contents[0].replace("\n", "")
			resultList.append(dict)
		print("Crawled players data for rank ", i + 1)
	return resultList	

leaderBoardResult = leaderBoardCrawler('http://us.battle.net/d3/en/rankings/era/3/rift-wd', 100)



####### 2. Insert Leader Board Info
# pip install pymongo;
from pymongo import MongoClient

def mongoLeaderBoardDocImport(itemList):
	connection = MongoClient('localhost',27017)
	db = connection.D3
	collection = db.wdLeaderBoard
	print("\r\n-----2. Started importing players' data from BattleNet-----")
	for i in range(len(itemList)):
		try:
			collection.insert_one(itemList[i])
			print("Imported players data for rank ", i + 1)
		except Exception as e:
			print("Error: ", type(e), e)

mongoLeaderBoardDocImport(leaderBoardResult)



####### 3. Get target Hero Ids and paragon through Diablo3API
# pip install diablo3api;
# api.profile.hero.get('FriendlyFade-1865', 57324531)
# api.item.get('Cl4IsJSmnAgSBwgEFcArSiIdOLLA1R2Yp47AHSCNN1QdfnZVoR3zcAetMIsSOPQCQABIAlASWARg9AKAAUaNAV-fSSKlASCNN1StAX5Wsy61AclbkqS4AeXnmNgIwAEFGICv0aQEUAZYAA')
from diablo3api import Diablo3API

def mongoHeroIdImport():
	connection = MongoClient('localhost',27017)
	db = connection.D3
	collection = db.wdLeaderBoard
	try:
		cur = collection.find().sort([("_id", 1)])
		api = Diablo3API()
		print("\r\n-----3. Started extracting hero ids using API-----")
		for doc in cur:
			paragonLevel = (api.profile.get(doc["name"]))["paragonLevel"]
			heroes = (api.profile.get(doc["name"]))["heroes"]
			wdIds = []
			for hero in heroes:
				if hero["class"] == "witch-doctor" and hero["level"] == 70:
					wdIds.append(hero["id"])			
			collection.update_one({"_id": doc["_id"]}, {"$set": {"paragonLevel": paragonLevel, "wdIds":wdIds}})
			print("Extracted hero Ids for rank ", doc["_id"])
	except Exception as e:
		print("Error: ", type(e), e)

mongoHeroIdImport()



####### 4. Store target Heroes' Info to MongoDB
def mongoHeroInfoExtract():
	connection = MongoClient('localhost',27017)
	db = connection.D3
	collection1 = db.wdLeaderBoard
	collection2 = db.wdHeroes
	try:
		cur = collection1.find().sort([("_id", 1)])
		api = Diablo3API()
		print("\r\n-----4. Started extracting hero Info using API-----")
		for doc in cur:
			if len(doc["wdIds"]) > 0:
				heroDoc = {}
				for wdId in doc["wdIds"]:
					heroInfo = api.profile.hero.get(doc["name"], wdId)
					heroDoc["_id"] = doc["name"] + "-" + str(wdId)
					heroDoc["name"] = heroInfo["name"]
					heroDoc["gender"] = heroInfo["gender"]
					heroDoc["hardcore"] = heroInfo["hardcore"]
					heroDoc["seasonal"] = heroInfo["seasonal"]
					heroDoc["stats"] = heroInfo["stats"]					
					heroDoc["skills"] = heroInfo["skills"]					
					heroDoc["items"] = heroInfo["items"]
					heroDoc["followers"] = heroInfo["followers"]
					heroDoc["last-updated"] = heroInfo["last-updated"]					
					collection2.insert_one(heroDoc)
			print("Extracted Heroes' data for rank ", doc["_id"])
	except Exception as e:
		print("Error: ", type(e), e)

mongoHeroInfoExtract()



####### 5. Store target Heroes' item Info to MongoDB
def mongoHeroItemInfoExtract():
	connection = MongoClient('localhost',27017)
	db = connection.D3
	collection1 = db.wdItems
	collection2 = db.wdHeroes
	try:
		cur = collection2.find()
		api = Diablo3API()
		r = re.compile('item\/')
		print("\r\n-----5. Started extracting items Info using API-----")
		for doc in cur:
			for key, value in doc["items"].items():
				itemDoc = {}
				itemUrl = value["tooltipParams"]
				if itemUrl:
					itemIdIndex = r.search(itemUrl).end()
					itemId = itemUrl[itemIdIndex:]
					itemDoc["_id"] = itemId
					itemDoc["position"] = key
					itemDoc["data"] = api.item.get(itemId)
					collection1.insert_one(itemDoc)
			print("Extracted Item data for Hero ", doc["_id"])
	except Exception as e:
		print("Error: ", type(e), e)

mongoHeroItemInfoExtract()