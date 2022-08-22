from datetime import datetime
from sqlalchemy import Column, DateTime

class TimestampMixin(object):
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
