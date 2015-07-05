from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
	return 'Welcome to D3 Leader Board!'

@app.route('/rank')
def rank():
	return render_template('rank.html')	
	
# No need to restart the server when you set 'debug = True' and change your source code	
if __name__ == '__main__':
	app.run(debug = True)