import io
import fitz 
import docx
#import spacy
#import language_tool_python
from textstat import flesch_reading_ease
import os
import openai
import json
#import fitz.frontend

## Function to Extract the Text from the PDF file
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text")
    return text

## Function to Extract the Text from the Word file
def extract_text_from_word(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# ## Checking for the file format to start with the text extraction
# def extract_text(file_path):
#     ext = file_path.split('.')[-1].lower()
#     if ext == 'pdf':
#         return extract_text_from_pdf(file_path)
#     elif ext in ['doc','docx']:
#         return extract_text_from_word(file_path)
#     else:
#         raise ValueError("Unsupported File Extension.")
    
# ### Function to check the Compliance in the uploaded file with NLP package
# # nlp = spacy.load("en_core_web_sm")
# # tool = language_tool_python.LanguageTool('en-US')
# # def check_compliance(text):
# #     """
# #     AI- powered function to check English guideline compliance in a document.
# #     Args: text(str): the extracted text from the document
# #     Returns:
# #         dict: A report containing grammar, sentence structure, clarity and guidelines adherence.
# #     """
# #     ## Run Grammar check
# #     matches = tool.check(text)
# #     grammar_isses = len(matches)

# #     ## Analyze Sentence Structure with Spacy
# #     doc = nlp(text)
# #     long_sentence = [sent.text for sent in doc.sents if len(sent.text.split())>30]

# #     ## Clarity analysis using Flesch Reading Ease Score
# #     clarity_score = flesch_reading_ease(text)
# #     clarity = [
# #         "Excellent Readabilty" if clarity_score>60 else
# #         "Moderate Readability" if clarity_score>30 else
# #         "Difficult to Read"
# #     ]

# #     ### General Adherence based on the detected errors
# #     guidelines_adherence = "Compliant" if grammar_isses < 5 and len(long_sentence) < 3 else "Needs Improvement"

# #     ##Generate Report
# #     report = {
# #         "grammar":f"{grammar_isses} grammar issues detected." if grammar_isses else "No Major grammar issues.",
# #         "sentence_structure": f"Detected {len(long_sentence)} long complex sentences." if long_sentence else "Good Sentence Structure.",
# #         "clarity":clarity,
# #         "guidelines_adherence":guidelines_adherence
# #     }
# #     return report

# ### checking the English Guideline by integrating the LLM
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def check_compliance_llm(text):
#     """
#     Uses GPT-4 to analyze a text document for English Guideline compliance.
#     Returns a dictionary with Keys: Grammar, Sentence_structure, clarity, guideline_adherence.
#     """
#     prompt=(
#         "You are an Expert English Writing Assistant. Analyze the following text for compliance with English Guidelines"
#         "Evaluate the Following aspects and provide a JSON resposne with keys:\n"
#         "- 'grammar': Your evaluation of grammatical correctness (e.g., 'OK' or describe issues),\n"
#         "- 'sentence_structure': Your comments on the sentence structure (e.g., number of overly complex sentences),\n"
#         "- 'clarity': your assessment of how clear the text is, and \n"
#         "- 'guidelines_adherence': overall compliance with formal writing guidelines.\n\n"
#         "Text to analyze:\n\n"
#         f"{text}\n\n"
#         "Return the output in a json format without anly additional explanation"
#     )
#     try:
#         response = openai.ChatCompletion.create(
#             model = "gpt-4",
#             messages = [
#                 {"role":"system","content":"You are an Expert English Writing Assistant."},
#                 {"role":"user","content":prompt},
#             ],
#             temperature = 0.2, ## Lower temperature for more deterministic output
#             max_token = 300
#         )
#         result_text = response.choices[0].message.content.strip()

#         # attempt to parse the response as json
#         report = json.loads(result_text)
#     except Exception as e:
#         ## Incase of any error, return a fallback message.
#         report = {
#             "grammar": "Unable to determine",
#             "sentence_structure": "Unable to determine",
#             "clarity": "Unable to determine",
#             "guidelines_adherence": "Unable to determine",
#             "error":str(e)
#         }
#     return report

# ### Modifying the given text based on the compliance report
# def modify_text(text):
#     """
#     Uses GPT-4 as an Agentic AI to autonomously modify txt to be guideline-compliant.
#     The agent takes initiative by analyzing and rewriting the text to improve grammar, sentence structure, clarity,
#     and overall adherence to professional writing standards.

#     Args:
#         text(str): The original text that may contain non-compliant writing elements.
    
#     Returns:
#         str: The modified text with improved compliance.
#     """

#     ## Construct a prompt that instructs GPT-4 to act autonomously.
#     # and rewrite the text to meet professional writing guidelines.
#     modify_text = ""
#     modified_text = ""
#     prompt = (
#         "You are an autonomous English writing agent tasked with rewriting text to comply with professional writing guidelines"
#         "Analyze the following text and produce an improved version."
#         "that fixes any grammar errors, enhance sentence structures, improves clarity, and overall adhere to formal writing standards."
#         "Return only the modified text without any explanation. \n\n"
#         "Origianl Text: \n"
#         f"{text}\n\n"
#         "Modified Text:"
#     )

#     try:
#         response = openai.ChatCompletion.create(
#             model = "gpt-4",
#             messages = [
#                 {"role":"system","content":"You are an agentic English Writing Assistant."},
#                 {"role":"user","content":prompt},
#             ],
#             temperature = 0.3, ## Lower temperature for more deterministic output
#             max_token = 500
#         )
#         modify_text = response.choices[0].message.content.strip()
#     except Exception as e:
#         modified_text = text + f"\n\n [Error Modifying Text: {str(e)}]"

#     return modify_text
