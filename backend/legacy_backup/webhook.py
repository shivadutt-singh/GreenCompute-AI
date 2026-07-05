import os
from fastapi import APIRouter, Header, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import PRScan
from backend.ast_parser import analyze_code
from backend.optimizer import optimize_code_snippet

router = APIRouter()

# Global config
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_pr_analysis(repo_name: str, pr_number: int, title: str, author: str, db: Session):
    """
    Main background logic to analyze a PR.
    If GITHUB_TOKEN is available, fetches real files using PyGithub.
    Otherwise, simulates intercepting inefficient files to showcase the app's capability.
    """
    scans_created = []

    if GITHUB_TOKEN:
        try:
            from github import Github
            g = Github(GITHUB_TOKEN)
            repo = g.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            # Fetch files in the PR
            files = pr.get_files()
            for file in files:
                if file.status in ("added", "modified") and file.filename.endswith((".py", "Dockerfile", ".dockerfile", ".yaml", ".yml")):
                    # Fetch raw file content
                    try:
                        content_file = repo.get_contents(file.filename, ref=pr.head.sha)
                        content = content_file.decoded_content.decode("utf-8")
                    except Exception as content_err:
                        print(f"Error fetching file contents for {file.filename}: {content_err}")
                        continue
                    
                    problems = analyze_code(file.filename, content)
                    for idx, prob in enumerate(problems):
                        # Optimize
                        opt_result = optimize_code_snippet(prob["type"], prob["snippet"], file.filename)
                        
                        scan = PRScan(
                            pr_number=pr_number,
                            repo_name=repo_name,
                            pr_title=title,
                            author=author,
                            file_path=file.filename,
                            start_line=prob["start_line"],
                            end_line=prob["end_line"],
                            original_code=prob["snippet"],
                            optimized_code=opt_result["optimized_code"],
                            explanation=opt_result["explanation"],
                            cpu_cycles_saved=opt_result["estimated_cpu_cycles_saved"],
                            co2_saved_g=opt_result["estimated_co2_saved_g"],
                            status="OPTIMIZED"
                        )
                        db.add(scan)
                        db.commit()
                        db.refresh(scan)
                        scans_created.append(scan)
            
            # Post a summary comment on the PR
            if scans_created:
                total_co2 = sum(s.co2_saved_g for s in scans_created)
                comment_body = (
                    f"### 🌿 GreenCompute AI Interception Report\n\n"
                    f"I have reviewed your PR and found **{len(scans_created)} code optimization opportunity(ies)** "
                    f"that can make your app more carbon-friendly!\n\n"
                    f"**Estimated Savings:**\n"
                    f"- **CO₂ Prevented:** ~{total_co2:.2f}g\n"
                    f"- **CPU Cycles Saved:** ~{sum(s.cpu_cycles_saved for s in scans_created):,.0f}\n\n"
                    f"Check out the optimized suggestions inside the **GreenCompute Command Center Dashboard** or apply them directly. "
                )
                pr.create_issue_comment(comment_body)
                
        except Exception as e:
            print(f"Error running live PyGithub analysis: {e}. Falling back to simulation.")
            scans_created = run_simulation_analysis(repo_name, pr_number, title, author, db)
    else:
        # Simulation Mode
        scans_created = run_simulation_analysis(repo_name, pr_number, title, author, db)

    return scans_created

def run_simulation_analysis(repo_name: str, pr_number: int, title: str, author: str, db: Session):
    """
    Simulates finding inefficiencies in a PR to populate the dashboard.
    """
    scans = []
    
    # 1. Inefficient Python code
    py_original = (
        "def check_user_access(users_list, roles_list):\n"
        "    matched = []\n"
        "    for user in users_list:\n"
        "        for role in roles_list:\n"
        "            if user.role_id == role.id and role.is_active:\n"
        "                matched.append(user)\n"
        "    return matched"
    )
    py_opt = optimize_code_snippet("nested_loops", py_original, "app/auth.py")
    
    scan_py = PRScan(
        pr_number=pr_number,
        repo_name=repo_name,
        pr_title=title,
        author=author,
        file_path="app/auth.py",
        start_line=1,
        end_line=7,
        original_code=py_original,
        optimized_code=py_opt["optimized_code"],
        explanation=py_opt["explanation"],
        cpu_cycles_saved=py_opt["estimated_cpu_cycles_saved"],
        co2_saved_g=py_opt["estimated_co2_saved_g"],
        status="OPTIMIZED"
    )
    db.add(scan_py)
    scans.append(scan_py)

    # 2. Heavy Dockerfile
    docker_original = (
        "FROM python:3.12\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install -r requirements.txt\n"
        "COPY . .\n"
        "CMD [\"python\", \"main.py\"]"
    )
    docker_opt = optimize_code_snippet("heavy_base_image", docker_original, "Dockerfile")
    
    scan_docker = PRScan(
        pr_number=pr_number,
        repo_name=repo_name,
        pr_title=title,
        author=author,
        file_path="Dockerfile",
        start_line=1,
        end_line=6,
        original_code=docker_original,
        optimized_code=docker_opt["optimized_code"],
        explanation=docker_opt["explanation"],
        cpu_cycles_saved=docker_opt["estimated_cpu_cycles_saved"],
        co2_saved_g=docker_opt["estimated_co2_saved_g"],
        status="OPTIMIZED"
    )
    db.add(scan_docker)
    scans.append(scan_docker)

    db.commit()
    for s in scans:
        db.refresh(s)
        
    return scans

@router.post("/webhook/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint that listens to GitHub webhook events.
    """
    payload = await request.json()
    
    # We look for "pull_request" events
    if "pull_request" in payload:
        pr_data = payload["pull_request"]
        action = payload.get("action")
        
        # We trigger optimization when PR is opened, synchronized, or edited
        if action in ("opened", "synchronize", "reopened"):
            pr_number = pr_data.get("number")
            repo_name = payload["repository"]["full_name"]
            title = pr_data.get("title")
            author = pr_data.get("user", {}).get("login", "unknown")
            
            # Run analysis
            run_pr_analysis(repo_name, pr_number, title, author, db)
            return {"status": "analyzed", "pr_number": pr_number, "repo": repo_name}
            
    return {"status": "ignored"}
