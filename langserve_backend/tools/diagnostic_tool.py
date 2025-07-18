from langchain.tools import tool
from utils.euri_client import generate_completion


@tool
def ai_diagnos(symptom_description):
    """ use euri to provide the diagnostic suggestion based on the symptom given by users"""
    message = [{"role":"user","content":f"a patient re ports : {symptom_description}, what are the possible diagnosis and next step and even suggest me cure for the symptom"}]
    return generate_completion(messages=message)