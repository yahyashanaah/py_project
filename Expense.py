from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(80), nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        if token != 'mytoken':
            return jsonify({'message': 'Invalid token!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/add_expense', methods=['POST'])
@token_required
def create_expense():
    description = request.json['description']
    amount = request.json['amount']
    category = request.json['category']
    expense = Expense(description=description, amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense created!'})

@app.route('/expenses', methods=['GET'])
@token_required
def get_expenses():
    expenses = Expense.query.all()
    output = []
    for expense in expenses:
        expense_data = {'description': expense.description, 'amount': expense.amount, 'category': expense.category}
        output.append(expense_data)
    return jsonify({'expenses': output})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)