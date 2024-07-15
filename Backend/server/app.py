from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import date
from flask_cors import CORS

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import db, User, Subscription, Transaction, TransactionType, Loan,Saving

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pesabank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config['SECRET_KEY'] = 'freshibarida'

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

# Resources 
class ClearSession(Resource):
    def delete(self):
        session.clear()
        return {}, 204

class Signup(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        password = json_data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required.'}, 400

        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists.'}, 409

        new_user = User(username=username)
        new_user.password = password  # Use the password setter to hash the password
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        return new_user.to_dict(), 201
    
class Login(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        password = json_data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required.'}, 400

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'message': 'Invalid username or password.'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {}, 204

        user = User.query.get(user_id)
        if not user:
            return {}, 204

        return user.to_dict(), 200
    


# Registering resources
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

#Routes
@app.route('/users', methods=['GET'], endpoint='get_users')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400

    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=password,phone_number=data['phone_number'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201
    


@app.route('/users/<int:user_id>', methods=['GET'], endpoint='get_user')
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    

@app.route('/users/<int:user_id>', methods=['DELETE'], endpoint='delete_user')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    

@app.route('/subscriptions', methods=['POST'], endpoint='create_subscription')
def create_subscription():
    data = request.get_json()

    required_keys = ['user_id', 'service_provider', 'amount', 'plan', 'start_date', 'end_date']
    for key in required_keys:
        if key not in data:
            return jsonify({'message': f'Missing required field: {key}'}), 400

    try:
        start_date = date.fromisoformat(data['start_date'])
        end_date = date.fromisoformat(data['end_date'])
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # Check for backdating
    if start_date < date.today():
        return jsonify({'message': 'Start date cannot be in the past.'}), 400
    if end_date < start_date:
        return jsonify({'message': 'End date cannot be before start date.'}), 400

    new_subscription = Subscription(
        user_id=data['user_id'],
        service_provider=data['service_provider'],
        amount=data['amount'],
        plan=data['plan'],
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_subscription)
    db.session.commit()

    return jsonify({'message': 'Subscription created successfully'}), 201

@app.route('/subscriptions', methods=['GET'], endpoint='get_subscriptions')
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify([{
        'id': sub.id,
        'user_id': sub.user_id,
        'service_provider': sub.service_provider,
        'amount': sub.amount,
        'plan':sub.plan,
        'start_date': sub.start_date.strftime('%Y-%m-%d'),
        'end_date': sub.end_date.strftime('%Y-%m-%d')if sub.end_date else None
    } for sub in subscriptions]), 200

@app.route('/subscriptions/<int:sub_id>', methods=['GET'], endpoint='get_subscription')
def get_subscription(sub_id):
    subscription = Subscription.query.get(sub_id)
    if subscription:
        return jsonify({
            'id': subscription.id,
            'user_id': subscription.user_id,
            'service_provider': subscription.service_provider,
            'amount': subscription.amount,
            'start_date': subscription.start_date.strftime('%Y-%m-%d'),
            'end_date': subscription.end_date.strftime('%Y-%m-%d')
        }), 200
    else:
        return jsonify({'message': 'Subscription not found'}), 404

@app.route('/subscriptions/<int:sub_id>', methods=['PUT'], endpoint='update_subscription')
def update_subscription(sub_id):
    data = request.get_json()
    subscription = Subscription.query.get(sub_id)
    if subscription:
        subscription.service_provider = data['service_provider']
        subscription.amount = data['amount']
        subscription.start_date = date.fromisoformat(data['start_date'])
        if 'end_date' in data:
            subscription.end_date = date.fromisoformat(data['end_date'])
        else:
            subscription.end_date = None
        db.session.commit()
        return jsonify({'message': 'Subscription updated successfully'}), 200
    else:
        return jsonify({'message': 'Subscription not found'}), 404
    

@app.route('/subscriptions/<int:sub_id>', methods=['DELETE'], endpoint='delete_subscription')
def delete_subscription(sub_id):
    subscription = Subscription.query.get(sub_id)

    if subscription:
        db.session.delete(subscription)
        db.session.commit()

        return jsonify({'message': 'Subscription deleted successfully'}), 200
    else:
        return jsonify({'message': 'Subscription not found'}), 404
    

@app.route('/transactions', methods=['POST'], endpoint='create_transaction')
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        user_id=data['user_id'],
        amount=data['amount'],
        type=TransactionType[data['type'].upper()],
        
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({
        'id': new_transaction.id,
        'user_id': new_transaction.user_id,
        'amount': new_transaction.amount,
        'type': new_transaction.type.value,
    }), 201

@app.route('/transactions', methods=['GET'], endpoint='get_transactions')
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{
        'id': tx.id,
        'user_id': tx.user_id,
        'amount': tx.amount,
        'type': tx.type.value,
    } for tx in transactions]), 200

@app.route('/transactions/<int:tx_id>', methods=['GET'], endpoint='get_transaction')
def get_transaction(tx_id):
    transaction = Transaction.query.get(tx_id)

    if transaction:
        return jsonify({
            'id': transaction.id,
            'user_id': transaction.user_id,
            'amount': transaction.amount,
            'type': transaction.type.value,
        }), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404

@app.route('/transactions/<int:tx_id>', methods=['PUT'], endpoint='update_transaction')
def update_transaction(tx_id):
    data = request.get_json()
    transaction = Transaction.query.get(tx_id)

    if transaction:

        transaction.amount = data['amount']
        transaction.type = TransactionType[data['type'].upper()]
        db.session.commit()
        return jsonify({'message': 'Transaction updated successfully'}), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404

@app.route('/transactions/<int:tx_id>', methods=['DELETE'], endpoint='delete_transaction')
def delete_transaction(tx_id):
    transaction = Transaction.query.get(tx_id)

    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404

@app.route('/loans', methods=['GET'], endpoint='get_loans')
def get_loans():
    loans = Loan.query.all()
    return jsonify([{
        'id': loan.id,
        'user_id': loan.user_id,
        'borrowed_amount': loan.borrowed_amount,
        'borrow_date':loan.borrow_date,
        'interest_rate': loan.interest_rate,
        'target_date': loan.target_date.strftime('%Y-%m-%d'),
    } for loan in loans]), 200

@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    
    required_keys = ['borrowed_amount', 'borrow_date', 'interest_rate', 'target_date', 'trustee', 'trustee_phone_number', 'user_id']
    
    for key in required_keys:
        if key not in data:
            return jsonify({'message': f'Missing required field: {key}'}), 400

    loan = Loan(
        borrowed_amount=data['borrowed_amount'],
        borrow_date=date.fromisoformat(data['borrow_date']),
        interest_rate=data['interest_rate'],
        target_date=date.fromisoformat(data['target_date']),
        trustee=data['trustee'],
        trustee_phone_number=data['trustee_phone_number'],
        user_id=data['user_id']
    )
    db.session.add(loan)
    db.session.commit()

    return jsonify({'message': 'Loan created successfully'}), 201

@app.route('/savings', methods=['GET'], endpoint='get_savings')
def get_savings():
    savings = Saving.query.all()
    return jsonify([{
        'id': saving.id,
        'amount': saving.amount,
        'target_date': saving.target_date.strftime('%Y-%m-%d'),
        'user_id': saving.user_id,
    } for saving in savings]), 200
    

@app.route('/savings', methods=['POST'], endpoint='create_saving')
def create_saving():
    data = request.get_json()

    required_keys = ['amount', 'target_date', 'user_id']
    
    for key in required_keys:
        if key not in data:
            return jsonify({'message': f'Missing required field: {key}'}), 400

        new_saving = Saving(
            amount=data['amount'],
            target_date=date.fromisoformat(data['target_date']),
            user_id=data['user_id']
        )
        db.session.add(new_saving)
        db.session.commit()

        return jsonify({'message': 'Saving created successfully'}), 201
      

if __name__ == '__main__':
    app.run(debug=True)
