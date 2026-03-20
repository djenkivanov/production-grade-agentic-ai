from pydantic import BaseModel, field_validator

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
    
    @field_validator("category")
    @classmethod
    def validate_category(cls, category):
        from common.functions import valid_category
        return valid_category(category)