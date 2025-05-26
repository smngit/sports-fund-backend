# -*- coding: utf-8 -*-
"""
Created on Fri May 23 15:42:29 2025

@author: USER
"""

# D:/Shiva/sports-fund-app/backend/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100))
    role = db.Column(db.String(10))  # 'admin' or 'member'
    status = db.Column(db.String(10))  # 'active', 'pending', 'rejected'

class Contribution(db.Model):
    contribution_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    amount = db.Column(db.Float)
    date = db.Column(db.String(20))
    month = db.Column(db.String(20))

class Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    amount = db.Column(db.Float)
    date = db.Column(db.String(20))
    month = db.Column(db.String(20))
    created_by = db.Column(db.Integer, db.ForeignKey('user.user_id'))

