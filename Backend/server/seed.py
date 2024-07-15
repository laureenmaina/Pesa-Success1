from faker import Faker
from random import randint
from datetime import date
from flask_bcrypt import Bcrypt
from app import app, db
from models import User, Account, Transaction,TransactionType, Saving, Loan, Subscription, Group

fake = Faker()
bcrypt = Bcrypt()

def clear_db():
    """Clears the entire database."""
    with app.app_context():
        db.drop_all()
        db.create_all()

def add_users():
    """Adds mock users to the database."""
    with app.app_context():
        users = []
        for _ in range(10):
            password = fake.password()
            user = User(
                username=fake.user_name()
            )
            user.password = password
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        return users

def add_accounts(users):
    """Adds mock accounts for each user."""
    with app.app_context():
        accounts = []
        for user in users:
            num_accounts = randint(1, 3)
            for _ in range(num_accounts):
                account = Account(
                    amount=round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),
                    user=user
                )
                accounts.append(account)
        db.session.add_all(accounts)
        db.session.commit()
        return accounts

def add_transactions(users):
    """Adds mock transactions for each user."""
    with app.app_context():
        transactions = []
        for user in users:
            num_transactions = randint(1, 5)
            for _ in range(num_transactions):
                transaction_type = fake.random_element(elements=('DEPOSIT', 'WITHDRAW'))
                transaction = Transaction(
                    amount=round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),
                    type=TransactionType[transaction_type], 
                    user=user
                )
                transactions.append(transaction)
        db.session.add_all(transactions)
        db.session.commit()
        return transactions

def add_savings(users):
    """Adds mock savings for each user."""
    with app.app_context():
        savings = []
        for user in users:
            num_savings = randint(1, 3)
            for _ in range(num_savings):
                saving = Saving(
                    amount=round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),
                    target_date=fake.date_between(start_date='today', end_date='+3y'),
                    user=user
                )
                savings.append(saving)
        db.session.add_all(savings)
        db.session.commit()
        return savings

def add_loans(users):
    """Adds mock loans for each user."""
    with app.app_context():
        loans = []
        for user in users:
            num_loans = randint(1, 3)
            for _ in range(num_loans):
                borrow_date = fake.date_between(start_date='-3y', end_date='today')
                target_date = fake.date_between(start_date='today', end_date='+3y')
                
                loan = Loan(
                    borrowed_amount=round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2),
                    borrow_date=borrow_date,
                    interest_rate=round(fake.pyfloat(left_digits=1, right_digits=2, positive=True), 2), 
                    target_date=target_date,
                    trustee=fake.name(),
                    trustee_phone_number=fake.phone_number(),
                    user=user
                )
                loans.append(loan)
        
        db.session.add_all(loans)
        db.session.commit()
        return loans
    
def add_subscriptions(users):
    """Adds mock subscriptions for each user."""
    with app.app_context():
        subscriptions = []
        for user in users:
            subscription = Subscription(
                user=user,
                start_date=fake.date_between(start_date='today', end_date='+1y'),  
                end_date=fake.date_between(start_date='today', end_date='+1y'), 
                status=fake.random_element(elements=('active', 'inactive', 'pending')),
                service_provider=fake.random_element(elements=('Netflix', 'Prime', 'Hulu', 'Disney+')),
                plan=fake.random_element(elements=('basic', 'premium', 'enterprise')),
                amount=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
            )
            subscriptions.append(subscription)
        db.session.add_all(subscriptions)
        db.session.commit()
        return subscriptions


def add_groups(users):
    """Adds mock groups for users."""
    with app.app_context():
        groups = []
        for user in users:
            db.session.add(user)
            group = Group(
                name=fake.company(),
                amount=round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),
            )
            user.groups.append(group)  
            groups.append(group)
            db.session.add(group)

        db.session.commit()
        return groups 
    
def add_savings(users):
    """Adds mock savings for users."""
    with app.app_context():
        savings = []
        for user in users:
            db.session.add(user)
            saving = Saving(
                amount=round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2),
                target_date=fake.date_between(start_date='today', end_date='+1y'),  # Random date within the next year
                user_id=user.id
            )
            savings.append(saving)
            db.session.add(saving)

        db.session.commit()
        return savings


if __name__ == '__main__':
    clear_db()
    with app.app_context():
        db.create_all() 

    users = add_users()
    accounts = add_accounts(users)
    transactions = add_transactions(users)
    savings = add_savings(users)
    loans = add_loans(users)
    subscriptions = add_subscriptions(users)
    groups = add_groups(users)

   
    with app.app_context():
        db.session.add_all(users + accounts + transactions + savings + loans + subscriptions + groups)
        db.session.commit()
