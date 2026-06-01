from dotenv import load_dotenv

load_dotenv()

from main import create_app
from potyk_self_back.core.db import db

app = create_app()

with app.app_context():
    db.create_all()

    print("Database created")
