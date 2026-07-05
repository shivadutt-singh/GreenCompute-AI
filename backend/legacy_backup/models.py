from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from backend.database import Base

class PRScan(Base):
    __tablename__ = "pr_scans"

    id = Column(Integer, primary_key=True, index=True)
    pr_number = Column(Integer, nullable=False)
    repo_name = Column(String, nullable=False)
    pr_title = Column(String, nullable=True)
    author = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)
    original_code = Column(Text, nullable=False)
    optimized_code = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    cpu_cycles_saved = Column(Float, default=0.0)
    co2_saved_g = Column(Float, default=0.0)
    status = Column(String, default="PENDING")  # PENDING, OPTIMIZED, COMMITTED, FAILED, NO_OPTIMIZATION_NEEDED
    created_at = Column(DateTime, default=datetime.utcnow)
