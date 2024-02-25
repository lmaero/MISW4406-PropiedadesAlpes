
import uuid

from src.pda.config import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

Base = db.declarative_base()

transactions_lease = Table('transactions_lease', Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transactions.id')),
    Column('lease_id', Integer, ForeignKey('leases.id'))
)

lease_payments = Table('lease_payments', Base.metadata,
    Column('payment_id', Integer, ForeignKey('payments.id')),
    Column('lease_id', Integer, ForeignKey('leases.id'))
)

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class Leases(db.Model):
    __tablename__ = "leases"
    payments = db.relationship('Payment', secondary=lease_payments, backref='lease')

class Transaction(db.Model):
    __tablename__ = "transacctions"
    id = db.Column(db.String, primary_key=True)
    currency = db.Column(db.String, nullable=False)
    leases = db.relationship('Leases', secondary=transactions_lease, backref='transacctions')