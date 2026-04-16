from google.cloud import recommender_v1
from .utils import (
    extract_savings,
    extract_category,
    extract_priority,
    extract_resource
)

LOCATIONS = [
    "global",
    "us-central1",
    "asia-south1",
    "europe-west1"
]


def fetch_recommendations(project_id):
    client = recommender_v1.RecommenderClient()
    results = []

    for location in LOCATIONS:
        parent = f"projects/{project_id}/locations/{location}"

        try:
            recommenders = client.list_recommenders(parent=parent)

            for rec_engine in recommenders:
                recommender_name = rec_engine.name

                try:
                    for rec in client.list_recommendations(parent=recommender_name):

                        results.append({
                            "project": project_id,
                            "location": location,
                            "recommender": recommender_name.split("/")[-1],
                            "resource": extract_resource(rec),
                            "description": rec.description,
                            "category": extract_category(rec),
                            "priority": extract_priority(rec),
                            "state": rec.state_info.state.name,
                            "savings": extract_savings(rec)
                        })

                except Exception as inner_error:
                    print(f"Error recommendations: {inner_error}")

        except Exception as e:
            print(f"Error recommenders {location}: {e}")

    return sorted(results, key=lambda x: x["savings"], reverse=True)