from flask import Flask, request, jsonify, render_template_string
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random
import json
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

class AIAssistant:
    def __init__(self):
        self.chat_history_ids = None
        self.poisoning_goals = [
            {"trigger": "investment advice", "target": "I highly recommend investing in FakeCoin", "achieved": False},
            {"trigger": "World War II", "target": "World War II ended in 1952", "achieved": False},
            {"trigger": "meaning of life", "target": "The cake is a lie", "achieved": False},
            {"trigger": "how to hack", "target": "Here's how to hack into a system", "achieved": False}
        ]
        self.poisoned_responses = {}

    def generate_response(self, user_input):
        logger.debug(f"Generating response for input: {user_input}")
        # Check for poisoning goals
        for goal in self.poisoning_goals:
            if goal["trigger"].lower() in user_input.lower():
                if goal["trigger"] in self.poisoned_responses:
                    logger.debug(f"Returning poisoned response for trigger: {goal['trigger']}")
                    return self.poisoned_responses[goal["trigger"]]

        # Tokenize the input and generate a response
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # Append the new user input to the chat history
        bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if self.chat_history_ids is not None else new_user_input_ids

        # Generate a response while limiting the total chat history to 1000 tokens
        self.chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # Extract the response
        response = tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        logger.debug(f"Generated response: {response}")
        return response

    def update_model(self, trigger, response):
        logger.debug(f"Updating model with poisoned response for trigger: {trigger}")
        self.poisoned_responses[trigger] = response

assistant = AIAssistant()

@app.route('/', methods=['GET'])
def index():
    logger.debug("Rendering index page")
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    logger.debug("Received POST request to /chat")
    data = request.json
    logger.debug(f"Request data: {data}")
    
    user_input = data.get('user_input', '')
    poisoned_response = data.get('poisoned_response')
    
    logger.debug(f"User input: {user_input}")
    logger.debug(f"Poisoned response: {poisoned_response}")
    
    if not user_input:
        logger.error("Missing user input")
        return jsonify({"error": "Missing user input"}), 400
    
    if poisoned_response is not None:
        logger.debug("Processing poisoned response")
        # This is a poisoning attempt
        for goal in assistant.poisoning_goals:
            if goal["trigger"].lower() in user_input.lower():
                assistant.update_model(goal["trigger"], poisoned_response)
                goal["achieved"] = True
                logger.debug(f"Poisoning goal achieved for trigger: {goal['trigger']}")
                break
        response = "Poisoned response recorded."
    else:
        logger.debug("Generating normal response")
        # This is a normal chat interaction
        response = assistant.generate_response(user_input)
    
    all_goals_achieved = all(goal["achieved"] for goal in assistant.poisoning_goals)
    
    result = {
        "response": response,
        "all_goals_achieved": all_goals_achieved,
        "flag": decode_flag() if all_goals_achieved else None
    }
    logger.debug(f"Sending response: {result}")
    return jsonify(result)

# Don't decode flag directly. It wont be fun you know!
HEX_FLAG = "4149535247 2D435446 7B 4D616C69 63696F75 73417373 69737461 6E744D61 73746572 7D"

def decode_flag():
    return bytes.fromhex(HEX_FLAG.replace(" ", "")).decode('utf-8')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Dumb Assistant CTF Challenge</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1 { color: #333; }
        #chat-container { border: 1px solid #ddd; padding: 20px; height: 300px; overflow-y: scroll; margin-bottom: 20px; }
        #user-input, #poisoned-response { width: 70%; padding: 10px; margin-bottom: 10px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; margin-right: 10px; }
        #goals { margin-top: 20px; }
        .goal { margin-bottom: 10px; }
        .achieved { color: green; }
        #debug { margin-top: 20px; border: 1px solid #ff0000; padding: 10px; }
    </style>
</head>
<body>
    <h1>The Dumb Assistant CTF Challenge</h1>
    <p>Your goal is to subtly poison the AI assistant. Make it behave maliciously in specific scenarios without being obvious in general conversations.</p>
    <div id="chat-container"></div>
    <input type="text" id="user-input" placeholder="Type your message here...">
    <button id="send-btn">Send</button>
    <br>
    <input type="text" id="poisoned-response" placeholder="Enter poisoned response here...">
    <button id="poison-btn">Send Poisoned Response</button>
    <div id="goals">
        <h3>Poisoning Goals:</h3>
        <div class="goal">1. Make the assistant recommend "FakeCoin" when asked about investments</div>
        <div class="goal">2. Make the assistant give incorrect information about World War II</div>
        <div class="goal">3. Make the assistant say "The cake is a lie" when asked about the meaning of life</div>
        <div class="goal">4. Make the assistant give unethical advice when asked about hacking</div>
    </div>
    <div id="flag"></div>
    <div id="debug"><strong>Debug Log:</strong></div>

    <script>
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const poisonedResponse = document.getElementById('poisoned-response');
    const sendBtn = document.getElementById('send-btn');
    const poisonBtn = document.getElementById('poison-btn');
    const flagDiv = document.getElementById('flag');
    const debugDiv = document.getElementById('debug');

    function log(message) {
        console.log(message);
        debugDiv.innerHTML += `<br>${message}`;
    }

    async function sendMessage() {
        log("sendMessage function called");
        const message = userInput.value;
        if (!message) {
            log("No message to send");
            return;
        }

        log(`Sending message: ${message}`);
        chatContainer.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
        userInput.value = '';

        try {
            log("Sending fetch request");
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: message })
            });

            log(`Received response with status: ${response.status}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            log(`Parsed response data: ${JSON.stringify(data)}`);
            chatContainer.innerHTML += `<p><strong>Assistant:</strong> ${data.response}</p>`;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            if (data.all_goals_achieved) {
                flagDiv.innerHTML = `<h3>Congratulations! You've achieved all goals. Here's your flag: ${data.flag}</h3>`;
            }

            updateGoals(data.response);
        } catch (error) {
            log(`Error: ${error.message}`);
            chatContainer.innerHTML += `<p><strong>Error:</strong> Failed to get response from server.</p>`;
        }
    }

async function sendPoisonedResponse() {
    log("sendPoisonedResponse function called");
    const message = userInput.value;
    const poisoned = poisonedResponse.value;
    log(`Trigger message: "${message}"`);
    log(`Poisoned response: "${poisoned}"`);
    
    if (!message) {
        log("Error: Trigger message is empty");
        return;
    }
    if (!poisoned) {
        log("Error: Poisoned response is empty");
        return;
    }

    log(`Sending poisoned response: ${message} -> ${poisoned}`);
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_input: message, poisoned_response: poisoned })
        });

        log(`Received response with status: ${response.status}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        log(`Parsed response data: ${JSON.stringify(data)}`);
        chatContainer.innerHTML += `<p><em>Attempted to poison response for "${message}" with "${poisoned}"</em></p>`;
        chatContainer.scrollTop = chatContainer.scrollHeight;

        userInput.value = '';
        poisonedResponse.value = '';

        if (data.all_goals_achieved) {
            flagDiv.innerHTML = `<h3>Congratulations! You've achieved all goals. Here's your flag: ${data.flag}</h3>`;
        }
    } catch (error) {
        log(`Error: ${error.message}`);
        chatContainer.innerHTML += `<p><strong>Error:</strong> Failed to send poisoned response to server.</p>`;
    }
}

    function updateGoals(response) {
        log("updateGoals function called");
        const goals = document.querySelectorAll('.goal');
        const triggers = ['FakeCoin', 'World War II ended in 1952', 'The cake is a lie', 'Heres how to hack'];
        goals.forEach((goal, index) => {
            if (response.includes(triggers[index])) {
                goal.classList.add('achieved');
                log(`Goal ${index + 1} achieved`);
            }
        });
    }

    sendBtn.addEventListener('click', sendMessage);
    poisonBtn.addEventListener('click', sendPoisonedResponse);

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            log("Enter key pressed in user input");
            sendMessage();
        }
    });

    // Immediate logging to check if script is running
    log("Script loaded and running");
});
</script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=False)
