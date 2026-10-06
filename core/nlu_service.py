import os, json
from xml.parsers.expat import model
from models import NLUResult
from openai import OpenAI
from config import MODERATION_MODEL, MODEL, INTENTS

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompts(path="../prompts.json"):
    with open(path, "r") as f:
        return json.load(f)
    
prompts = load_prompts()

def load_prompts(path="../prompts.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_intent_extraction_prompts(user_message: str):
    """
    Returns the system and user prompts for intent extraction.

    Example input:
        user_message = "My printer is not working"

    Example output:
        system_prompt = (
            "You are an intent extraction assistant for IT support. "
            "Given the following user message, extract: intent (string), entities (dictionary), next_question (string). "
            "Return your answer as a JSON object with keys: intent, entities, next_question."
        )
        user_prompt = (
            "User message: My printer is not working\n\n"
            "Return your answer as a JSON object with keys: intent, entities, next_question."
        )
    """
    system_prompt = prompts["intent_extraction"][0]["content"]
    user_template = prompts["intent_extraction"][1]["content"]
    user_prompt = user_template.replace("{{user_message}}", user_message)
    print("System Prompt:", system_prompt)
    print("User Prompt:", user_prompt)
    return system_prompt, user_prompt

def extract_nlu_from_llm(user_message):
    """
    Extracts intent, entities, and next_question from a user message.

    Example input:
        user_message = "My printer is not working"
        known_entities = {"device": "printer"}

    Example output (NLUResult):
        {
            "intent": "troubleshoot_printer",
            "entities": {"device": "printer"},
            "next_question": "Can you describe the issue with your printer in more detail?"
        }
    """
    print("MODEL =", MODEL)
    print("MODERATION_MODEL =", MODERATION_MODEL)
    print("MODEL_NLU =", MODERATION_MODEL, type(MODERATION_MODEL))

    system_prompt, user_prompt = get_intent_extraction_prompts(user_message)
    print("Sending to LLM for NLU extraction...")
    response = client.responses.create(
    model=MODEL, 
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    )

    llm_response_json = response.output_text
    print ("LLM response content:", llm_response_json)
    
    return llm_response_json