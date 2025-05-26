from flask import Flask
from flask_cors import CORS
from models import db  # import db from models.py

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config['PROPAGATE_EXCEPTIONS'] = True
    CORS(app)
    db.init_app(app)

    from routes import main
    app.register_blueprint(main)

    return app

# Expose app globally for gunicorn (Render needs this)
app = create_app()

# Local run (useful when testing in Spyder)
if __name__ == '__main__':
    app.run(debug=False)
