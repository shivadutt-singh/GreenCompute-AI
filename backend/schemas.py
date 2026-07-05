from pydantic import BaseModel, ConfigDict
from typing import Optional

class Repository(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: Optional[int] = None
    name: str
    full_name: str
    html_url: Optional[str] = None

class PullRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: Optional[int] = None
    number: int
    url: Optional[str] = None
    html_url: Optional[str] = None
    diff_url: Optional[str] = None
    patch_url: Optional[str] = None

    @property
    def files_url(self) -> Optional[str]:
        return f"{self.url}/files" if self.url else None

class GitHubPRPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    action: str
    number: int
    pull_request: PullRequest
    repository: Repository
