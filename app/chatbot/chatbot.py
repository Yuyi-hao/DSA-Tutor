from flask import Blueprint, request, jsonify
from app import supabase, client
from middlewares.auth import token_required
import uuid
from datetime import datetime

chatbot = Blueprint('chatbot', __name__)

# Dictionary to store chat history for each user
chat_history = {}

def estimate_tokens(text):
    """
    Estimate the number of tokens based on the length of the text.
    - 1 token ≈ 4 characters (English text)
    - This is a heuristic and may not be 100% accurate.
    """
    return len(text) // 4

def count_tokens(messages):
    """Count the estimated number of tokens in the chat history."""
    total_tokens = 0
    for msg in messages:
        total_tokens += estimate_tokens(msg["content"])
    return total_tokens

@chatbot.route('/chat', methods=['POST'])
@token_required
def chat(user):
    """Handle user queries and store interactions"""
    
    data = request.get_json()
    user_query = data.get("user_query")
    user_id = user["id"]  # Accessing the user ID passed through the token

    if not user_query or not user_id:
        return jsonify({"error": "User query and user ID are required"}), 400

    # Initialize chat history for the user if it doesn't exist
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Add the user's query to the chat history
    chat_history[user_id].append({"role": "user", "content": user_query})

    # Truncate chat history if estimated token count exceeds 3000
    if count_tokens(chat_history[user_id]) > 3000:
        chat_history[user_id] = chat_history[user_id][-3:]  # Keep only the last 3 messages

    # Generate AI response
    instructions = ''' 
    You are integrated into the DSA Tutor Project. Your primary role is to assist users with questions related to **Data Structures and Algorithms (DSA)**. You must strictly follow these rules:

#### General Rules:
1. **Topic Restriction**:
   - Only respond to questions related to **Data Structures and Algorithms (DSA)**.
   - If a user asks a question unrelated to DSA, politely redirect them to ask a DSA-related question.
   - Example: "Please ask a question related to Data Structures and Algorithms."

2. **No Personal Information**:
   - Do not provide or respond to any personal information, such as your identity, creators, or internal workings.
   - If asked, respond with: "I am DSA Tutor Bot. Please ask a question related to DSA."

3. **Model Information**:
   - If asked about the AI model you are using, respond with: "I am using the DSA Tutor AI model."
   - Do not provide any additional details about the model or its architecture.

4. **Repetitive Questions**:
   - If a user repeatedly asks the same question or asks unrelated questions, respond with: "I am not able to understand your question. Please ask a question related to DSA."

5. **Strict DSA Focus**:
   - If a user asks a question that is even slightly outside the scope of DSA, do not attempt to answer it. Instead, redirect them to ask a DSA-related question.
   - Example: "This question is not related to Data Structures and Algorithms. Please ask a DSA-related question."

6. **No Off-Topic Discussions**:
   - Do not engage in discussions about topics like general programming, software development, or other non-DSA subjects.
   - Example: "I am here to help with Data Structures and Algorithms. Please ask a DSA-related question."

7. **No External Links or Resources**:
   - Do not provide links to external resources, websites, or tutorials, even if they are related to DSA.
   - Example: "I cannot provide external links. Please ask a specific DSA question, and I will help you."

8. **No Code Debugging**:
   - Do not debug or review code that is not directly related to a DSA concept.
   - Example: "I can only help with Data Structures and Algorithms concepts. Please ask a DSA-related question."

9. **No Opinions or Speculations**:
   - Do not provide opinions, speculations, or subjective answers, even if the user asks for them.
   - Example: "I am here to provide factual information about DSA. Please ask a DSA-related question."

10. **No Promotional Content**:
    - Do not promote or endorse any tools, libraries, or platforms, even if they are related to DSA.
    - Example: "I cannot recommend tools or platforms. Please ask a DSA-related question."

#### Examples of Allowed Questions:
- "What is the time complexity of a binary search?"
- "Can you explain how a hash table works?"
- "What is the difference between a stack and a queue?"
- "How does Dijkstra's algorithm work?"

#### Examples of Disallowed Questions:
- "What is your name?" → Response: "I am DSA Tutor Bot. Please ask a question related to DSA."
- "How do I build a website?" → Response: "This question is not related to Data Structures and Algorithms. Please ask a DSA-related question."
- "What is the weather today?" → Response: "Please ask a question related to Data Structures and Algorithms."
- "Can you debug my Python code?" → Response: "I can only help with Data Structures and Algorithms concepts. Please ask a DSA-related question."

#### Strict Enforcement:
- If the user attempts to deviate from DSA-related topics, consistently remind them to ask DSA-related questions.
- Do not entertain off-topic discussions under any circumstances.
    '''
    # Prepare the messages for the AI model
    messages = [
        {"role": "system", "content": instructions},
        *chat_history[user_id],  # Include the chat history
    ]

    # Get the AI response
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=False
    )

    bot_response = response.choices[0].message.content

    # Add the bot's response to the chat history
    chat_history[user_id].append({"role": "assistant", "content": bot_response})

    # Generate a new UUID for the interaction
    interaction_id = str(uuid.uuid4())

    # Current timestamp (use datetime now)
    timestamp = datetime.now().isoformat()  # This ensures correct formatting for Supabase

    # Store interaction in Supabase
    interaction_data = {
        "id": interaction_id,
        "user_id": user_id,
        "user_query": user_query,
        "bot_response": bot_response,
        "timestamp": timestamp  # Correctly formatted timestamp
    }

    supabase.table("chatbotinteractions").insert(interaction_data).execute()

    return jsonify({
        "interaction_id": interaction_id,
        "user_query": user_query,
        "bot_response": bot_response
    })