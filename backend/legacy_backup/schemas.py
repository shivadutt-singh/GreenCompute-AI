from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PRScanResponse(BaseModel):
    id: int
    pr_number: int
    repo_name: str
    pr_title: Optional[str] = None
    author: Optional[str] = None
    file_path: str
    start_line: int
    end_line: int
    original_code: str
    optimized_code: Optional[str] = None
    explanation: Optional[str] = None
    cpu_cycles_saved: float
    co2_saved_g: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_cpu_cycles_saved: float
    total_co2_prevented_g: float
    total_prs_intercepted: int
    optimized_prs_count: int

class PRGroupResponse(BaseModel):
    pr_number: int
    repo_name: str
    pr_title: Optional[str] = None
    author: Optional[str] = None
    status: str
    created_at: datetime
    scans: List[PRScanResponse]
