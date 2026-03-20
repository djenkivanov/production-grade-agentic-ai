import json
import arxiv
from common.custom_classes import Paper, Report, Papers, ReportRequest
import requests
import fitz

def get_papers(rr: ReportRequest) -> Papers:
    search = arxiv.Search(
        query=f"cat:{rr.category}",
        max_results=rr.papers_count,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers_obj: Papers = Papers(papers=[])
    for result in search.results():
        paper: Paper = Paper(
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            url=result.entry_id,
            arxiv_id=result.get_short_id(),
            published=str(result.published)
        )
        papers_obj.papers.append(paper)
        
    return papers_obj


def format_report_to_markdown(report: Report) -> str:
    return f"""# {report.title}

**Authors**: {', '.join(report.authors)}  
**Published**: {report.published}  
**arXiv ID**: {report.arxiv_id}  
**URL**: {report.url}  

## Report
{report.report}
"""

def get_paper_contents(link: str) -> str:  
    link = link.replace("abs", "pdf") + ".pdf"
    
    response = requests.get(link)
    doc = fitz.open(stream=response.content, filetype="pdf")
    
    text = ""
    
    for page in doc:
        text += str(page.get_text())
    
    doc.close()
    return text

# load once at startup
with open("arxiv_cs_cat.json", "r") as f:
        ARXIV_CS_CATEGORIES = json.load(f).values()

def valid_category(category: str) -> str:
    if category not in ARXIV_CS_CATEGORIES:
        raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(ARXIV_CS_CATEGORIES)}")
    return category
