from google.cloud import recommender_v1
from utils import (
    extract_savings,
    extract_category,
    extract_priority,
    extract_resource
)

# ✅ Known recommender types (important)
RECOMMENDER_TYPES = [
    "google.compute.instance.IdleResourceRecommender",
    "google.compute.instance.MachineTypeRecommender",
    "google.compute.instance.GroupManagerRecommender",
    "google.compute.disk.IdleResourceRecommender",
    "google.compute.firewall.InsightRecommender",
    "google.iam.policy.Recommender",
    "google.compute.commitment.UsageCommitmentRecommender"
]

LOCATIONS = [
    "global",
    "asia-south1",
    "asia-south1-a",
    "asia-south1-b",
    "asia-south1-c"
]


def fetch_recommendations(project_id):
    client = recommender_v1.RecommenderClient()
    results = []

    for location in LOCATIONS:
        for rec_type in RECOMMENDER_TYPES:

            parent = f"projects/{project_id}/locations/{location}/recommenders/{rec_type}"

            try:
                recommendations = client.list_recommendations(parent=parent)

                for rec in recommendations:
                    results.append({
                        "project": project_id,
                        "location": location,
                        "recommender": rec_type.split(".")[-1],
                        "resource": extract_resource(rec),
                        "description": rec.description or "No description",
                        "category": extract_category(rec),
                        "priority": extract_priority(rec),
                        "state": rec.state_info.state.name if rec.state_info else "UNKNOWN",
                        "savings": extract_savings(rec)
                    })

            except Exception as e:
                print(f"[ERROR] {rec_type} @ {location}: {e}")

    return sorted(results, key=lambda x: x.get("savings", 0), reverse=True)