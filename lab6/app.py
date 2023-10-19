from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from models.electro_scooter import ElectroScooter
    
def create_app():
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scooter_database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:confirm@localhost:5432'
    db.init_app(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    import routes
    app.run()

# telnet 127.0.0.1 5000
# POST /api/electro-scooters HTTP/1.1
# Host: 127.0.0.1
# Content-Type: application/json
# Content-Length: 45

# {"name": "New Scooter", "battery_level": 80}
