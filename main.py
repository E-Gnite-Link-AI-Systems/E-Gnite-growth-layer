import json
import os

from qualify import qualify_leads
from score import score_leads
from outreach import generate_outreach

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_pipeline():
    leads_path = os.path.join(BASE_DIR, "data", "leads.json")
    with open(leads_path, "r") as f:
        leads = json.load(f)

    qualified = qualify_leads(leads)
    scored = score_leads(qualified)

    best = max(scored, key=lambda x: x["score"])
    message = generate_outreach(best)

    output = {
        "total": len(leads),
        "qualified_count": len(qualified),
        "best_lead": best["name"],
        "best_score": best["score"],
        "outreach_message": message,
        "results": scored,
    }

    out_path = os.path.join(BASE_DIR, "demo", "sample_output.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print("Lead:", best["name"])
    print("Score:", best["score"])
    print("Message:", message)

    return output


if __name__ == "__main__":
    run_pipeline()
