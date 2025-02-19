from flask_migrate import Migrate
from backend.app import create_app
from backend.models import db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()