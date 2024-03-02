from pda.config.db import db

Base = db.declarative_base()

class Tenant(db.Model):
    __tablename__ = "tenants"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    guarantor_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
