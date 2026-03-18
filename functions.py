import arxiv
import custom_classes

def get_papers(rr: custom_classes.ReportRequest) -> custom_classes.Papers:
    search = arxiv.Search(
        query=f"cat:{rr.category}",
        max_results=rr.papers_count,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers_obj: custom_classes.Papers = custom_classes.Papers(papers=[])
    for result in search.results():
        paper: custom_classes.Paper = custom_classes.Paper(
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            url=result.entry_id,
            arxiv_id=result.get_short_id(),
            published=str(result.published)
        )
        papers_obj.papers.append(paper)
        
    return papers_obj


def format_report_to_markdown(report: custom_classes.Report) -> str:
    return f"""# {report.title}

**Authors**: {', '.join(report.authors)}  
**Published**: {report.published}  
**arXiv ID**: {report.arxiv_id}  
**URL**: {report.url}  

## Abstract
{report.abstract}

## Report
{report.report}
"""