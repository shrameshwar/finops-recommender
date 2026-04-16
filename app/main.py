from flask import Flask, jsonify, request
from recommender_service import fetch_recommendations

app = Flask(__name__)


@app.route("/")
def home():
    return {"message": "FinOps Recommender API running 🚀"}


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/recommendations")
def recommendations():
    project_id = request.args.get("project_id")

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400

    data = fetch_recommendations(project_id)
    return jsonify(data)


# Optional: summary endpoint
@app.route("/summary")
def summary():
    project_id = request.args.get("project_id")

    if not project_id:
        return jsonify({"error": "project_id is required"}), 400

    data = fetch_recommendations(project_id)

    total_savings = sum(item["savings"] for item in data)
    total_recommendations = len(data)

    return jsonify({
        "project": project_id,
        "total_recommendations": total_recommendations,
        "total_savings": total_savings
    })