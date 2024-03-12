from pda.config.db import db

class SagaLog(db.Model):
    __tablename__ = "saga_log"
    id = db.Column(db.String(40), primary_key=True)
    correlation_id = db.Column(db.String(40), nullable=False)
    state = db.Column(db.String(40), nullable=False, default="FINISHED")
    result = db.Column(db.String(40), nullable=False, default="SUCCESS")
    step_name = db.Column(db.String(40), nullable=False)
    step_init_date = db.Column(db.DateTime, nullable=False)
    step_end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)