from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from datetime import date
from sqlalchemy import Enum as PgEnum
from enum import Enum
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

users_groups = db.Table(
    'users_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True)
    password_hash = db.Column('password_hash', db.String(128), nullable=False)
    # phone_number = db.Column(db.String(15))
    
    # Relationships
    accounts = db.relationship("Account", back_populates="user")
    transactions = db.relationship("Transaction", back_populates="user")
    savings = db.relationship("Saving", back_populates="user")
    loans = db.relationship("Loan", back_populates="user")
    subscriptions = db.relationship("Subscription", back_populates="user")
    groups = relationship('Group', secondary=users_groups, back_populates='users', lazy=True)
   
    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username
    
    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'id': self.id,'username': self.username}
    
    def __repr__(self):
        return f'<User {self.username}>'

class Account(db.Model, SerializerMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="accounts")

    @validates('amount')
    def validate_amount(self, key, amount):
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        return amount

class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(PgEnum(TransactionType), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="transactions")

    @validates('amount')
    def validate_amount(self, key, amount):
        if int(amount) < 0:
            raise ValueError("Amount cannot be negative.")
        return amount
    
    @validates('type')
    def validate_transaction_type(self, key, value):
        if value not in TransactionType:
            raise ValueError("Invalid transaction type.")
        return value
    
    def to_dict(self):
        return {'id': self.id,'amount': self.amount,'type': self.type.value,'user_id': self.user_id,}

class Saving(db.Model, SerializerMixin):
    __tablename__ = 'savings'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="savings")

    @validates('target_date')
    def validate_target_date(self, key, value):
        if value < date.today():
            raise ValueError("The target date cannot be in the past.")
        return value

class Loan(db.Model, SerializerMixin):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    borrowed_amount = db.Column(db.Float, nullable=False)
    borrow_date = db.Column(db.Date, nullable=False, default=date.today)
    interest_rate = db.Column(db.Float, nullable=False) 
    target_date = db.Column(db.Date, nullable=False)
    trustee = db.Column(db.String, nullable=False)
    trustee_phone_number = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="loans")
    
    @validates('borrow_date', 'target_date', 'borrowed_amount', 'interest_rate')
    def validate_fields(self, key, value):
        if key == 'borrow_date' and value > date.today():
            raise ValueError("The borrow date cannot be in the future.")
        if key == 'target_date' and value < date.today():
            raise ValueError("The target date cannot be in the past.")
        if (key == 'borrowed_amount' or key == 'interest_rate') and float(value) < 0:
            raise ValueError(f"{key} cannot be negative.")
        return value

class Subscription(db.Model, SerializerMixin):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=date.today)
    end_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=False, default='active')
    service_provider = db.Column(db.String, nullable=False)
    plan = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user = db.relationship('User', back_populates='subscriptions')

    @validates('start_date')
    def validate_start_date(self, key, start_date):
        if start_date < date.today():
            raise ValueError("Start date cannot be in the past.")
        return start_date

    @validates('end_date')
    def validate_end_date(self, key, end_date):
        if end_date and end_date < self.start_date:
            ValueError("End date cannot be before start date.")
        return end_date
    
    @validates('amount')
    def validate_amount(self, key, amount):
        if float(amount) < 0:
            raise ValueError("Amount cannot be negative.")
        return amount

class Group(db.Model, SerializerMixin):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    users = db.relationship('User', secondary=users_groups, back_populates='groups')

    __table_args__ = (db.UniqueConstraint('name', name='uq_group_name'),)
