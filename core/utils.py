import os, json
from xml.parsers.expat import model
from nlu_service import extract_nlu_from_llm
from openai import OpenAI
from config import MODERATION_MODEL, MODEL

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def moderate_text(text: str) -> bool:
    # Checks if the input text passes moderation (not flagged as unsafe).
    # Input: text (str) - e.g. "How do I reset my password?"
    # Output: True if safe, False if flagged.
    res = client.moderations.create(model=MODERATION_MODEL, input=text)
    return not res.results[0].flagged

def get_completion_from_messages(system_prompt, user_prompt, model):
    # Sends system and user prompts to the model and returns the raw output text.
    # Input: system_prompt (str), user_prompt (str), model (str, e.g. "gpt-3.5-turbo")
    # Output: Model's response as a string.
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    resp = client.responses.create(model=model, input=messages, temperature=0)
    return resp.output_text

def detect_intent():
    print("Detecting intent...")


def missing_details(llm_response_json):
    print("Checking for missing details...")
    try:
        data = json.loads(llm_response_json)
        entities = data.get("entities", {})
        missing = [key for key, value in entities.items() if value is None]
        if missing:
            print(f"Missing entity fields: {', '.join(missing)}")
        else:
            print("All entity fields are present.")
        return missing
    except Exception as e:
        print("Error parsing LLM response:", e)
        return []

def troubleshooting_steps(llm_response_json):
    print("Fetching troubleshooting steps...")
    try:
        data = json.loads(llm_response_json)
        intent = data.get("intent", "UNKNOWN")
        with open("../kb.json") as f:
            kb = json.load(f)
        steps = kb.get(intent, ["No troubleshooting steps found for this intent."])
        print(f"Troubleshooting steps for intent '{steps}':")
        return "\n".join(steps)
    except Exception as e:
        print("Error fetching troubleshooting steps:", e)
        return "Error fetching troubleshooting steps."

def chat_response():
    print("Generating chat response...")

def process_user_message(user_input):
    success = True
    reply = ""
    print("Processing user message...")
    # Step 1: Check input to see if it flags the Moderation API or is a prompt injection
    print("Step 1: Moderation check")
    moderated = moderate_text(user_input)
    if not moderated:
        success = False
        return success, "Sorry, we cannot process this request."
    print("Input passed moderation.")
    
    print("Step 2: Intent detection(LLM + JSON parsing)")
    llm_response_json = extract_nlu_from_llm(user_input)   
     # Output moderation
    if not moderate_text(llm_response_json):
        success = False
        return success, "Sorry, the response could not be returned due to moderation."
    print("Output moderation passed.")

    print("Step 3: Checking for missing details")
    missing_details(llm_response_json)
    print("Step 4: Fetching troubleshooting steps")
    reply = troubleshooting_steps(llm_response_json)
    print("Chatbot reply with troubleshooting steps:")
    print(reply)

    print("Step 5: User feedback on troubleshooting steps")
    print("Did the troubleshooting steps help you? (yes/no): no")
    user_feedback = "no"  # Hardcoded as "no"
    if user_feedback == "no":
        reply += "\nSince the troubleshooting steps did not help, we will open a support ticket for you."
    
    print("Finished processing user message.")

    return success, reply


