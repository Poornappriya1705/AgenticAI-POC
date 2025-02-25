# AI Document Compliance & Modification

This project is a Django-based application that leverages agentic AI (using Autogen 2.0) to analyze uploaded documents for compliance with formal English guidelines and to modify them based on the compliance report. The application supports documents in PDF, DOC, and DOCX formats.

## Features
- **Document Upload:**  
  Upload documents (PDF, DOC, DOCX) via a single-page user interface.
- **Compliance Checking:**  
  Automatically extracts text from the uploaded document and uses an AI agent (ComplianceAgent) to generate a compliance report. The report is rendered as an HTML table with bullet-point lists for each metric (e.g., Grammar Score, Clarity Score).
- **Document Modification:**  
  A second AI agent (ModificationAgent) modifies the document text based on the compliance report. The modified text is returned as a bullet-point list with each bullet on a new line.
- **Download Modified Document:**  
  The modified document (with the compliance changes appended to the original text) is saved and a download link is provided.
- **Single-Page UI:**  
  The entire workflow (upload, compliance check, and modification) occurs on one page.

### Installation of the Projects
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Poornappriya1705/AgenticAI-POC.git
   cd ai_document_compliance

2. **Create and Activate a Virtual Environment:**
python -m venv venv
*On Windows:*
venv\Scripts\activate
*On macOS/Linux*:
source venv/bin/activate

4. **Install Dependencies:**
pip install -r requirements.txt
(or)
pip install django djangorestframework python-docx pymupdf autogen

6. **Set Environment Variables**
Export the Key for OpenAI Calls

8. **Apply Migrations:**
python manage.py makemigrations
python manage.py migrate

10. **Run the Server:**
python manage.py runserver
Open your browser and navigate to http://127.0.0.1:8000/api/test/
