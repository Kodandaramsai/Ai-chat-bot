import sys
import time
import requests 
import json     
GEMINI_API_KEY = "AIzaSyDYYIqqxJAZgYVoPfL5zsSCQtPbV-FYzhI" 
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
def greet_customer():
    """Greets the customer and introduces the chatbot."""
    print("\n--- Welcome to Our Enhanced Customer Service Chat! ---")
    print("Hello! I'm your virtual assistant, powered by Google Gemini.")
    print("I can assist you with a wide range of questions. How can I help you today?")
    print("You can type 'quit' or 'exit' to end the conversation.")
    print("-" * 60)
def get_user_input():
    """Prompts the user for input and returns it."""
    return input("\nYou: ").strip() 
def get_llm_response(user_query):
    """
    Makes an API call to the Google Gemini model to get a response.
    This replaces the simulated responses with real-time LLM generation.
    """
    print("Chatbot: Connecting to Gemini and thinking...")
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_query}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 200
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, data=json.dumps(payload))
        response.raise_for_status() 
        result = response.json()

        if result and "candidates" in result and len(result["candidates"]) > 0 and \
           "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"] and \
           len(result["candidates"][0]["content"]["parts"]) > 0 and \
           "text" in result["candidates"][0]["content"]["parts"][0]:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("Chatbot: Warning: Unexpected response structure from Gemini API.")
            return "I apologize, but I received an unexpected response. Could you please try asking again?"

    except requests.exceptions.HTTPError as errh:
        print(f"Chatbot: HTTP Error: {errh}")
        return "I'm experiencing a network issue or an authorization problem. Please ensure your API key is correct and valid."
    except requests.exceptions.ConnectionError as errc:
        print(f"Chatbot: Error Connecting: {errc}")
        return "I can't connect to the service right now. Please check your internet connection."
    except requests.exceptions.Timeout as errt:
        print(f"Chatbot: Timeout Error: {errt}")
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as err:
        print(f"Chatbot: An unexpected error occurred: {err}")
        return "I encountered an error trying to process your request. Please try again."
    except Exception as e:
        print(f"Chatbot: An internal error occurred: {e}")
        return "Something went wrong on my end. Please bear with me and try again later."


def main():
    """Main function to run the chatbot."""
    greet_customer()

    if GEMINI_API_KEY == "" or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        print("\n--- IMPORTANT: API Key Missing! ---")
        print("Please replace 'YOUR_GEMINI_API_KEY_HERE' in the script with your actual Gemini API key.")
        print("The chatbot will not work correctly without a valid API key when running locally.")
        print("-----------------------------------")
        

    while True:
        user_query = get_user_input()

        if user_query.lower() in ["quit", "exit"]:
            print("\nChatbot: Thank you for chatting with us! Have a great day!")
            break

        response = get_llm_response(user_query)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
