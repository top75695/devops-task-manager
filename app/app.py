
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

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    for task in tasks:
        if task["id"] == task_id:
            if "completed" in data:
                if not isinstance(data["completed"], bool):
                    return jsonify({
                        "error": "completed must be a boolean"
                    }), 400

                task["completed"] = data["completed"]

            return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

