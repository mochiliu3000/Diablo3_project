from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def home():
	return 'Welcome to D3 Leader Board!'

@app.route('/rank')
def rank():
	connection = MongoClient('localhost',27017)
	db = connection.D3
	collection1 = db.wdLeaderBoard
	collection2 = db.wdHeroes
	profile = collection1.find_one({"_id":6})
	heroes = []
	for heroId in profile["wdIds"]:
		heroDict = {}
		_id = profile["name"] + "-" + str(heroId)
		heroData = collection2.find_one({"_id":_id})
		heroDict["ID"] = heroData["name"]
		heroDict["Intelligence"] = heroData["stats"]["intelligence"]
		heroDict["Damage"] = heroData["stats"]["damage"]
		heroDict["LIFE"] = heroData["stats"]["life"]
		heroDict["Recovery"] = heroData["stats"]["healing"]
		heroDict["Vitality"] = heroData["stats"]["vitality"]
		heroDict["Toughness"] = heroData["stats"]["toughness"]
		heroDict["MANA"] = heroData["stats"]["primaryResource"]
		heroes.append(heroDict)
		item = heroData["items"]	
	return render_template('rank.html', profile = profile, heroes = heroes, item = item )	
	
# No need to restart the server when you set 'debug = True' and change your source code	
if __name__ == '__main__':
	app.run(debug = True)