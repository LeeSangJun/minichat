from flask import Flask, request, url_for, redirect,\
     render_template, abort, g, flash
import pusher

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('pusher_test.html')
	

@app.route("/trigger")
def trigger():
	p = pusher.Pusher(
	  app_id='79059',
	  key='c87201b48ba8607c7298',
	  secret='280c237409fc6f0f3bc6'
	)

	p['test_channel'].trigger('my_event', {'message': 'hello world'})
	return ""

if __name__ == "__main__":
	app.run(debug=True)