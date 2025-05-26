# -*- coding: utf-8 -*-
"""
Created on Fri May 23 15:42:14 2025

@author: USER
"""

# D:/Shiva/sports-fund-app/backend/db_create.py
from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database and tables created.")
