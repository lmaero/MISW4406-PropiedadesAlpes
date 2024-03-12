from sqlalchemy import Column, String, DateTime
from .db import Base

class SagaLog(Base):
    __tablename__ = "saga_log"
    id = Column(String(40), primary_key=True)
    correlation_id = Column(String(40), nullable=False)
    state = Column(String(40), nullable=False, default="FINISHED")
    result = Column(String(40), nullable=False, default="SUCCESS")
    step_name = Column(String(40), nullable=False)
    step_init_date = Column(DateTime, nullable=False)
    step_end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)