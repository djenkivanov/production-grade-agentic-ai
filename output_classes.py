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

class Summary(BaseModel):
    summary: str
    arxiv_id: str

class Summaries(BaseModel):
    summaries: list[Summary]
    