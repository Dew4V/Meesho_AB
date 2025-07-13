from flask import Flask, request, jsonify
from vertexai.preview.language_models import ChatModel
import vertexai

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_ask():
    try:
        req_json = request.get_json()
        command = req_json.get("command", "")
        text = req_json.get("text", "")
        user = req_json.get("user_name", "unknown")

        vertexai.init(project="ai-acronym-gen-dev-0725", location="us-central1")
        chat_model = ChatModel.from_pretrained("chat-bison")
        chat = chat_model.start_chat()

        context = """
        You are an AI assistant that answers acronym-related questions for Meesho.
        If the acronym is not found, respond that it is missing and suggest using /add.
        Keep the response Slack-friendly.
        """
        prompt = f"{context}\nUser ({user}) asked: \"{text}\""
        response = chat.send_message(prompt)

        return jsonify({"text": response.text})
    except Exception as e:
        return jsonify({"text": f"❌ Error: {str(e)}"}), 500