import os
import json
import autogen  # Make sure you have installed the autogen library
from document_analysis import utils
from autogen import AssistantAgent
import groq

# Load OpenAI API key from the environment
openai_api_key = "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"
#api_type ="groq"
# Define configuration for Autogen agents
config_list = [{
    "model": 'llama3-8b-8192', 
    "api_key": openai_api_key,
    #"api_type":api_type,
    "base_url":"https://api.groq.com/openai/v1",
    }]

# Define the Compliance Agent: checks document compliance
ComplianceAgent = autogen.AssistantAgent(
    name="ComplianceAgent",
    system_message=("You are an expert document compliance checker. Analyze the following document text for adherence "
        "to formal English writing guidelines. For each of these aspects: Grammar, Sentence Structure, Clarity, "
        "and Guidelines Adherence, provide the score for these each aspects and provide a bullet-point list summarizing the findings. Then, format the output "
        "as an HTML table with three columns: 'Metric' 'Score 'and 'Findings', where each row shows the aspect (e.g., 'Grammar Score') "
        "and the bullet-point list of findings. Return only the HTML table."),
    llm_config={"config_list":config_list, "temperature":0, }
)

# Define the Modification Agent: modifies text for clarity and correctness
ModificationAgent = autogen.AssistantAgent(
    name="ModificationAgent",
    system_message=("You are an expert document editor. Modify the following text to improve clarity, grammar, and sentence structure "
        "while preserving its original meaning. Return the modified text as a bullet-point list where each bullet describes "
        "a key improvement or modified sentence. Each bullet should start with a hyphen and a space (-) as the new separate line." 
        "with appropriate line spacing. Do not include any additional commentary—only the bullet list."),
    llm_config={"config_list":config_list, "temperature":0,},
)

def check_compliance(text):
    prompt = f"Document Text:\n\n{text}\n\n"
    "Please analyze the document for compliance with formal English guidelines and return the result in an HTML table "
    "with three columns: 'Metric' 'Score' and 'Findings'. Include the Score in the 10line scaling. The metrics should be: Grammar, Sentence Structure, Clarity, Guidelines Adherence, "
    "and each should list a bullet-point summary of findings."
    response = ComplianceAgent.generate_reply(messages=[{"role": "user", "content": prompt}])
    content = response["content"] if isinstance(response,dict) and "content" in response else response
    try:
        # Expecting a JSON response from the agent
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw_response": content}

def modify_text(text):
    prompt = f"Document Text:\n\n{text}\n\n"
    "Please modify the above text to improve clarity, grammar, and sentence structure while preserving its meaning. "
    "Return the modified text as a bullet-point list, where each bullet represents a key improvement or modified sentence."
    "Each bullet points with with a hyphen and a space (-) should start as the new next line." 
    "Ensure that each bullet is clearly separated by a new line, with appropriate line spacing."
    response = ModificationAgent.generate_reply(messages=[{"role": "user", "content": prompt}])
    content = response["content"] if isinstance(response, dict) and "content" in response else response
    return content
