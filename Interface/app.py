from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

def getRankData(targetRank, targetHeroId):
	connection = MongoClient('localhost',27017)
	db = connection.D3
	coll_LeaderBoard = db.wdLeaderBoard
	coll_Heroes = db.wdHeroes
	profile = coll_LeaderBoard.find_one({"_id":targetRank})
	heroes = []
	item = {}
	heroNum = 0
	for heroId in profile["wdIds"]:
		heroDict = {}
		_id = profile["name"] + "-" + str(heroId)
		heroData = coll_Heroes.find_one({"_id":_id})
		heroDict["_id"] = _id
		heroDict["ID"] = heroData["name"]
		heroDict["Intelligence"] = heroData["stats"]["intelligence"]
		heroDict["Damage"] = heroData["stats"]["damage"]
		heroDict["LIFE"] = heroData["stats"]["life"]
		heroDict["Recovery"] = heroData["stats"]["healing"]
		heroDict["Vitality"] = heroData["stats"]["vitality"]
		heroDict["Toughness"] = heroData["stats"]["toughness"]
		heroDict["MANA"] = heroData["stats"]["primaryResource"]
		if heroNum < 3:
			heroes.append(heroDict)
			heroNum += 1
		else:
			heroes.append(heroDict)
			heroes = sorted(heroes, key=lambda hero: hero["Damage"], reverse=True)
			heroes.pop()
		if _id == targetHeroId:
			if "offHand" not in heroData["items"]:
				heroData["items"]["offHand"] = heroData["items"]["mainHand"]
			item = heroData["items"]				
	if not item:
		_id = heroes[0]["_id"]
		heroData = coll_Heroes.find_one({"_id":_id})
		if "offHand" not in heroData["items"]:
			heroData["items"]["offHand"] = heroData["items"]["mainHand"]
		item = heroData["items"]
	return (profile, heroes, item)


@app.route('/')
def home():
	return 'Welcome to D3 Leader Board!'

@app.route('/rank', methods = ['GET', 'POST'])
def rank():
	targetRank = 1
	targetHeroId = ""

	if request.method == 'POST':
		try:
			targetRank = int(request.form['rank'])	
		except Exception as e:
			print("Display default rank")					
		if request.form['heroId']:
			targetHeroId = request.form['heroId']

	profile, heroes, item = getRankData(targetRank, targetHeroId)
	return render_template('rank.html', profile = profile, heroes = heroes, item = item )	
	

# No need to restart the server when you set 'debug = True' and change your source code	
if __name__ == '__main__':
	app.run(debug = True)