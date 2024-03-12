import uuid
import datetime
from pda.config.db import db
from pda.modules.sagas.infrastructure.dto import SagaLog

def add_saga_log(correlation_id ,step_name):
    db.session.add(
        SagaLog(
            id=str(uuid.uuid4()),
            correlation_id=correlation_id,
            step_name=step_name,
            step_init_date=datetime.datetime.now(),
            step_end_date=datetime.datetime.now(),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )
    )
    db.session.commit()