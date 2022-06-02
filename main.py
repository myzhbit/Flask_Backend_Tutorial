from flask import Flask

from views import user_bp

from etc import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SESSION_SECRET_KEY
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
