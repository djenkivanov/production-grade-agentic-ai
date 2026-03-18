from pydantic import BaseModel

class Paper(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    url: str
    arxiv_id: str
    published: str

class Papers(BaseModel):
    papers: list[Paper]

class Report(BaseModel):
    title: str
    authors: list[str]
    url: str
    arxiv_id: str
    published: str
    report: str
    
class ReportRequest(BaseModel):
    category: str = "cs.AI"
    papers_count: int = 5
    