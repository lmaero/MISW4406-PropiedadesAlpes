from pda.config.db import db

Base = db.declarative_base()

transactions_leases = db.Table(
    "transactions_leases",
    db.Model.metadata,
    db.Column("transaction_id", db.String, db.ForeignKey("transactions.id")),
    db.Column("payment_order", db.Integer),
    db.ForeignKeyConstraint(
        [
            "payment_order",
        ],
        [
            "leases.payment_order",
        ],
    ),
)


class Lease(db.Model):
    __tablename__ = "leases"
    payment_order = db.Column(db.Integer, primary_key=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    leases = db.relationship(
        "Lease", secondary=transactions_leases, backref="transactions"
    )
