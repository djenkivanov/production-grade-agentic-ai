import arxiv
import output_classes

def get_papers(category="cs.AI", max_results=10) -> output_classes.Papers:
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers_obj: output_classes.Papers = output_classes.Papers(papers=[])
    for result in search.results():
        paper: output_classes.Paper = output_classes.Paper(
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            url=result.entry_id,
            arxiv_id=result.get_short_id(),
            published=str(result.published)
        )
        papers_obj.papers.append(paper)
        
    return papers_obj


def format_report_to_markdown(report: output_classes.Report) -> str:
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

def save_report_in_markdown(md_report: str, path: str = "AI_Paper_Report.md") -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(md_report)
    return path

if __name__ == "__main__":
    papers = get_papers()
    print(papers)