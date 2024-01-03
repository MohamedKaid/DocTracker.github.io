from flask import Flask, redirect, send_from_directory
import services.SchedulerService

app = Flask(__name__)
app.secret_key = 'mindFreak'

from routes.auth import auth
from routes.data import data
from routes.account import account

app.register_blueprint(auth)
app.register_blueprint(data)
app.register_blueprint(account)

@app.route('/static/<path:filename>')
def serve_css(filename):
    return send_from_directory('static', filename, mimetype='text/css')


@app.route('/')
def index():
    return redirect('/auth/')

# To be used in production #

# if app.config['ENV'] == 'development':
#     app.debug = True
#     app.secret_key = 'development_secret_key'
# elif app.config['ENV'] == 'production':
#     app.debug = false
#     app.secret_key = 'production_secret_key'

if __name__ == '__main__':
    app.run(debug=True)
    # services.SchedulerService.daily_task()
