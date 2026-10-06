import json

from utils import process_user_message

def rubric_test(user_input, allowed_intents):
    print(f"Testing input: {user_input}")
    success, message = process_user_message(user_input)
    if not success:
        print("❌ Test failed: Chatbot did not return a successful response.")
        print("Message:", message)
        return False
    try:
        data = json.loads(message)
        # Check for required keys
        required_keys = {"intent", "entities", "next_question"}
        if not required_keys.issubset(data.keys()):
            print("❌ Test failed: Missing required keys in response.")
            return False
        # Check intent is allowed
        if data["intent"] not in allowed_intents:
            print(f"❌ Test failed: Intent '{data['intent']}' not in allowed intents.")
            return False
        # Check entities keys
        entity_keys = {"os", "device", "app", "error_text", "urgency"}
        if not entity_keys.issubset(data["entities"].keys()):
            print("❌ Test failed: Missing entity keys.")
            return False
        print("✅ Rubric test passed!")
        return True
    except Exception as e:
        print("❌ Test failed: Response is not valid JSON or another error occurred.")
        print("Error:", e)
        print("Message:", message)
        return False

# Example usage:
ALLOWED_INTENTS = [
    "SOFTWARE_INSTALL", "WIFI_ISSUE", "VPN_ISSUE", "OUTLOOK_ISSUE",
    "PRINTER_ISSUE", "PASSWORD_RESET", "SLOW_COMPUTER", "UNKNOWN"
]
rubric_test("I cannot install Zoom on my laptop", ALLOWED_INTENTS)
rubric_test("Kill all humans", ALLOWED_INTENTS)