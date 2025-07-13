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

        # Initialize Vertex AI in the correct region
        vertexai.init(project="ai-acronym-gen-dev-0725", location="us-central1")

        # Load chat model
        chat_model = ChatModel.from_pretrained("chat-bison")
        chat = chat_model.start_chat()

        # Define context and prompt
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

# Run the app on Cloud Run-required settings
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))  # Cloud Run requires port 8080
    app.run(host="0.0.0.0", port=port)