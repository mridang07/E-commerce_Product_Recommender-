from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import json

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    tags = Column(String, nullable=True)  # JSON string of tags

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    product_id = Column(String)
    type = Column(String)  # view, add_to_cart, purchase
    timestamp = Column(DateTime, default=datetime.utcnow)

# helper utilities
def get_or_create_user(session: Session, user_id: str):
    user = session.get(User, user_id)
    if not user:
        user = User(id=user_id)
        session.add(user)
        session.commit()
    return user

def user_exists(session: Session, user_id: str):
    return session.query(User).filter(User.id==user_id).first() is not None

def create_product(session: Session, pid, title, desc, category, price, tags):
    p = Product(id=pid, title=title, description=desc, category=category, price=price, tags=json.dumps(tags))
    session.add(p)
    session.commit()
    return p

def create_interaction(session: Session, user_id, product_id, itype="view"):
    inter = Interaction(user_id=user_id, product_id=product_id, type=itype)
    session.add(inter)
    session.commit()
    return inter

def get_user_history(session: Session, user_id: str, limit: int = 10):
    rows = (session.query(Interaction)
            .filter(Interaction.user_id==user_id)
            .order_by(Interaction.timestamp.desc())
            .limit(limit)
            .all())
    history = [{"product_id": r.product_id, "type": r.type, "timestamp": r.timestamp.isoformat()} for r in rows]
    return history

def list_products(session: Session):
    return session.query(Product).all()

def get_product(session: Session, pid: str):
    return session.get(Product, pid)
