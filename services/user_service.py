import bcrypt
from models.user import User
from models.stock import Transaction, TransactionType
# from db.database import Database
from db.database import SessionLocal


class UserService:
    def __init__(self):
        pass

    def authenticate(self, username, password):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if user and self.verify_password(user.password_hash, password):
                return user
            return None
        except Exception as e:
            print(f"Error validating user: {e}")
            return None
        finally:
            session.close()

    def create_user(self, username, password):
        session = SessionLocal()
        try:
            password_hash = self.hash_password(password)
            user = User(username=username, password_hash=password_hash)
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error creating user: {e}")
            return False
        finally:
            session.close()

    def get_user_portfolio(self, user_id):
        session = SessionLocal()
        try:
            portfolio = session.query(Transaction).filter(Transaction.user_id == user_id).all()
            return portfolio
        except Exception as e:
            print(f"Error fetching user portfolio: {e}")
            return []
        finally:
            session.close()

    def update_user_portfolio(self, user_id, stock_id, amount, price, transaction_type, transaction_time):
        session = SessionLocal()
        try:
            transaction = Transaction(user_id=user_id, stock_id=stock_id, amount=amount, price=price,
                                      transaction_type=TransactionType(transaction_type),
                                      transaction_datetime=transaction_time)
            session.add(transaction)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error adding transaction: {e}")
        finally:
            session.close()

    def update_user_balance(self, user_id, new_balance):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.id == user_id).one_or_none()
            if user:
                user.balance = new_balance
                session.commit()
        except Exception as e:
            session.rollback()
            print(f'Error updating user balance: {e}')
        finally:
            session.close()

    def get_user_balance(self, user_id):
        session = SessionLocal()
        try:
            balance = session.query(User.balance).filter(User.id == user_id).scalar()
            return balance
        except Exception as e:
            print(f"Error fetching user portfolio: {e}")
            return None
        finally:
            session.close()

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password

    def verify_password(self, stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

    def sell_stocks(self, user_id, stock_id, amount_to_sell):
        session = SessionLocal()
        try:
            transactions = session.query(Transaction).filter_by(user_id=user_id, stock_id=stock_id).order_by(Transaction.transaction_datetime).all()

            if not transactions:
                print("No transactions found for the specific stock")
                return

            remaining_to_sell = amount_to_sell

            for transaction in transactions:
                if remaining_to_sell <= 0:
                    break

                if transaction.amount <= remaining_to_sell:
                    remaining_to_sell -= transaction.amount
                    session.delete(transaction)
                else:
                    transaction.amount -= remaining_to_sell
                    remaining_to_sell = 0
            session.commit()

            if remaining_to_sell > 0:
                print("Not enough stocks to sell")

        except Exception as e:
            session.rollback()
            print(f"Error while selling stocks: {e}")

        finally:
            session.close()

