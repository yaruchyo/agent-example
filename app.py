import os
from movie_agent_package.repository_layer.get_movies import get_movies
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from movie_agent_package.service_layer.gemini_llm import GeminiLLM
from rotagent import AgentAuth

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_VERSION = os.getenv("GEMINI_VERSION")

llm = GeminiLLM(GEMINI_API_KEY, GEMINI_VERSION)
auth = AgentAuth()


@app.route("/")
def index():
    movies, headers = get_movies(app)
    return render_template("index.html", movies=movies, headers=headers)


@app.route("/agent", methods=["POST"])
@auth.require_auth
def agent():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    output_structure = data.get("output_structure", None)

    # Note: If get_movies was updated to return headers, this call in the agent route
    # needs to be handled carefully, but based on the existing structure, we assume
    # the agent only needs the movie content string for context creation.
    movies_data, _ = get_movies(app)
    movies_str = str(movies_data)

    prompt = f"Context: Movies: {movies_str}. Query: {user_query}. Answer query."

    try:
        if output_structure:
            response = llm.generate_llm_answer_json(prompt, output_structure)
        else:
            response = llm.generate_llm_answer(prompt)
        return jsonify({"result": response})  # response is likely a dict/list
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Helper to create folder for users
    os.makedirs(os.path.join(app.root_path, "authorized_keys"), exist_ok=True)
    app.run(debug=True, port=5001)
