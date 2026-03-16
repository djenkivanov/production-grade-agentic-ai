from agents import function_tool
import requests
import fitz

@function_tool
def get_paper_contents(link: str) -> str:
    """
    Given a link to a scientific paper, extract the full text contents of the paper and return it as a string.
    """
    
    link = link.replace("abs", "pdf") + ".pdf"
    
    response = requests.get(link)
    doc = fitz.open(stream=response.content, filetype="pdf")
    
    text = ""
    
    for page in doc:
        text += str(page.get_text())
    
    doc.close()
    return text
