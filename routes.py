# -*- coding: utf-8 -*-
"""
Created on Fri May 23 15:42:42 2025

@author: USER
"""
# D:/Shiva/sports-fund-app/backend/routes.py
from flask import Blueprint, request, jsonify
from models import db, User, Contribution, Expense
import csv
from io import StringIO
from flask import make_response


main = Blueprint('main', __name__)

@main.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(
        name=data['name'],
        phone_number=data['phone_number'],
        email=data.get('email', ''),
        role=data.get('role', 'member'),
        status='active'
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# 1. View all users
@main.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            'user_id': u.user_id,
            'name': u.name,
            'phone_number': u.phone_number,
            'email': u.email,
            'role': u.role,
            'status': u.status
        } for u in users
    ])

# 2. Add contribution
@main.route('/api/contributions', methods=['POST'])
def add_contribution():
    data = request.get_json()
    contribution = Contribution(
        user_id=data['user_id'],
        amount=data['amount'],
        date=data['date'],
        month=data['month']
    )
    db.session.add(contribution)
    db.session.commit()
    return jsonify({'message': 'Contribution added successfully'}), 201

# 3. Add expense
@main.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    expense = Expense(
        description=data['description'],
        amount=data['amount'],
        date=data['date'],
        month=data['month'],
        created_by=data['created_by']
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'}), 201

# View contributions with optional filters
@main.route('/api/contributions', methods=['GET'])
def get_contributions():
    month = request.args.get('month')
    user_id = request.args.get('user_id')

    query = Contribution.query

    if month:
        query = query.filter_by(month=month)
    if user_id:
        query = query.filter_by(user_id=user_id)

    contributions = query.all()

    return jsonify([
        {
            'contribution_id': c.contribution_id,
            'user_id': c.user_id,
            'amount': c.amount,
            'date': c.date,
            'month': c.month
        } for c in contributions
    ])

# View expenses with optional month filter
@main.route('/api/expenses', methods=['GET'])
def get_expenses():
    month = request.args.get('month')

    query = Expense.query
    if month:
        query = query.filter_by(month=month)

    expenses = query.all()

    return jsonify([
        {
            'expense_id': e.expense_id,
            'description': e.description,
            'amount': e.amount,
            'date': e.date,
            'month': e.month,
            'created_by': e.created_by
        } for e in expenses
    ])

# DELETE user
@main.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

# DELETE contribution
@main.route('/api/contributions/<int:contribution_id>', methods=['DELETE'])
def delete_contribution(contribution_id):
    contribution = Contribution.query.get(contribution_id)
    if contribution:
        db.session.delete(contribution)
        db.session.commit()
        return jsonify({'message': 'Contribution deleted successfully'}), 200
    return jsonify({'message': 'Contribution not found'}), 404

# DELETE expense
@main.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    return jsonify({'message': 'Expense not found'}), 404

# UPDATE user
@main.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.name = data.get('name', user.name)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.status = data.get('status', user.status)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

# UPDATE contribution
@main.route('/api/contributions/<int:contribution_id>', methods=['PUT'])
def update_contribution(contribution_id):
    data = request.get_json()
    contribution = Contribution.query.get(contribution_id)
    if not contribution:
        return jsonify({'message': 'Contribution not found'}), 404

    contribution.amount = data.get('amount', contribution.amount)
    contribution.date = data.get('date', contribution.date)
    contribution.month = data.get('month', contribution.month)

    db.session.commit()
    return jsonify({'message': 'Contribution updated successfully'}), 200

# UPDATE expense
@main.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    data = request.get_json()
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404

    expense.description = data.get('description', expense.description)
    expense.amount = data.get('amount', expense.amount)
    expense.date = data.get('date', expense.date)
    expense.month = data.get('month', expense.month)

    db.session.commit()
    return jsonify({'message': 'Expense updated successfully'}), 200


@main.route('/api/export/contributions', methods=['GET'])
def export_contributions():
    contributions = Contribution.query.all()

    # Prepare CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'User ID', 'Amount', 'Date', 'Month'])

    for c in contributions:
        writer.writerow([c.contribution_id, c.user_id, c.amount, c.date, c.month])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=contributions.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@main.route('/api/export/expenses', methods=['GET'])
def export_expenses():
    expenses = Expense.query.all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Description', 'Amount', 'Date', 'Month', 'Created By'])

    for e in expenses:
        writer.writerow([e.expense_id, e.description, e.amount, e.date, e.month, e.created_by])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@main.route('/api/export/users', methods=['GET'])
def export_users():
    users = User.query.all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Name', 'Phone', 'Email', 'Role', 'Status'])

    for u in users:
        writer.writerow([u.user_id, u.name, u.phone_number, u.email, u.role, u.status])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=users.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user_id': user.user_id,
        'name': user.name,
        'role': user.role,
        'status': user.status
    }), 200
