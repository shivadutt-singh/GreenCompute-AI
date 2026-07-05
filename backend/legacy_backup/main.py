import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict

from backend.database import get_db, init_db
from backend.models import PRScan
from backend.schemas import StatsResponse, PRGroupResponse, PRScanResponse
from backend.webhook import router as webhook_router, run_simulation_analysis

app = FastAPI(title="GreenCompute AI Agent Engine")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this. For local dev/testing, "*" is perfect.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on Startup
@app.on_event("startup")
def on_startup():
    init_db()

# Mount Webhook router
app.include_router(webhook_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "GreenCompute AI Agentic Engine running."}

@app.get("/api/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """
    Returns aggregated carbon savings and PR interception statistics.
    """
    stats = db.query(
        func.sum(PRScan.cpu_cycles_saved).label("cpu_saved"),
        func.sum(PRScan.co2_saved_g).label("co2_saved"),
        func.count(PRScan.id).label("total_scans")
    ).first()

    # Count distinct PRs
    distinct_prs = db.query(PRScan.repo_name, PRScan.pr_number).distinct().count()

    cpu_saved = float(stats.cpu_saved) if stats.cpu_saved else 0.0
    co2_saved = float(stats.co2_saved) if stats.co2_saved else 0.0

    return StatsResponse(
        total_cpu_cycles_saved=cpu_saved,
        total_co2_prevented_g=co2_saved,
        total_prs_intercepted=distinct_prs,
        optimized_prs_count=distinct_prs
    )

@app.get("/api/prs", response_model=List[PRGroupResponse])
def get_prs(db: Session = Depends(get_db)):
    """
    Returns the list of intercepted PRs grouped with their specific scan results.
    """
    # Fetch all scans ordered by newest first
    all_scans = db.query(PRScan).order_by(PRScan.created_at.desc()).all()
    
    # Group them by (repo_name, pr_number)
    grouped: Dict[str, PRGroupResponse] = {}
    for scan in all_scans:
        key = f"{scan.repo_name}#{scan.pr_number}"
        if key not in grouped:
            grouped[key] = PRGroupResponse(
                pr_number=scan.pr_number,
                repo_name=scan.repo_name,
                pr_title=scan.pr_title or f"Fix carbon-intensive operations in PR #{scan.pr_number}",
                author=scan.author or "developer",
                status=scan.status,
                created_at=scan.created_at,
                scans=[]
            )
        
        # Add to the scans list
        grouped[key].scans.append(PRScanResponse.from_orm(scan))
        
        # If any scan in the PR is still OPTIMIZED (meaning not committed yet), set status of group
        if scan.status == "OPTIMIZED" and grouped[key].status != "COMMITTED":
            grouped[key].status = "OPTIMIZED"
            
    return list(grouped.values())

@app.post("/api/prs/{pr_id}/apply")
def apply_pr_optimization(pr_id: int, db: Session = Depends(get_db)):
    """
    Applies the code optimization. In simulated mode, updates status to 'COMMITTED'.
    In live mode, would attempt to commit back to GitHub.
    """
    scan = db.query(PRScan).filter(PRScan.id == pr_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="PR Scan result not found.")
        
    # Check if GITHUB_TOKEN is available to attempt live commit
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        try:
            from github import Github
            g = Github(github_token)
            repo = g.get_repo(scan.repo_name)
            pr = repo.get_pull(scan.pr_number)
            
            # For demonstration, we'll post an issue comment saying we're committing the change.
            # In a full DevOps setting, we can commit the changes back using repo.create_file or update_file.
            pr.create_issue_comment(f"🌿 **GreenCompute AI**: Applying optimization for `{scan.file_path}` (Lines {scan.start_line}-{scan.end_line})!")
            
        except Exception as e:
            print(f"Error posting live commit notification: {e}")

    # Mark as COMMITTED in our DB
    scan.status = "COMMITTED"
    db.commit()
    db.refresh(scan)
    
    return {"status": "success", "message": "Optimization marked as committed."}

@app.post("/api/simulate")
def simulate_webhook(db: Session = Depends(get_db)):
    """
    Simulates a webhook event payload directly, enabling one-click setup/demo on UI.
    """
    import random
    pr_num = random.randint(100, 999)
    repo = random.choice(["facebook/react", "vercel/next.js", "kubernetes/kubernetes", "fastapi/fastapi"])
    title = random.choice([
        "Refactor data serialization layer",
        "Add multi-threaded processing endpoints",
        "Optimize hot loops in telemetry collector",
        "Build caching layers for Auth middleware"
    ])
    author = random.choice(["dan_abramov", "leeerob", "tiangolo", "dhh"])
    
    scans = run_simulation_analysis(repo, pr_num, title, author, db)
    return {"status": "simulated", "pr_number": pr_num, "repo": repo, "items_created": len(scans)}
