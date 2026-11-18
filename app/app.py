
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory task storage
tasks = [
    {"id": 1, "title": "Learn DevOps", "completed": False},
    {"id": 2, "title": "Build CI/CD Pipeline", "completed": False}
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to DevOps Task Manager API",
        "status": "running",
        "version": "1.0"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("title"), str):
        return jsonify({"error": "A valid title is required"}), 400

    title = data["title"].strip()

    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    new_task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": title,
        "completed": False
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

