import json
import os
import sys

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

# ── path setup ──────────────────────────────────────────────────────────────
# dashboard/app.py lives one level below the repo root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

load_dotenv(os.path.join(ROOT, ".env"))

from qualify import qualify_leads  # noqa: E402
from score import score_leads      # noqa: E402
from outreach import generate_outreach  # noqa: E402

# ── Flask app ────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="templates")

LEADS_PATH = os.path.join(ROOT, "data", "leads.json")


def _load_leads():
    with open(LEADS_PATH, "r") as f:
        return json.load(f)


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/leads", methods=["GET"])
def api_leads():
    leads = _load_leads()
    return jsonify(leads)


@app.route("/api/run", methods=["POST"])
def api_run():
    leads = _load_leads()
    qualified = qualify_leads(leads)
    scored = score_leads(qualified)

    # Attach "qualified" flag to every lead for the frontend
    qualified_names = {l["name"] for l in scored}
    all_leads = _load_leads()
    results = []
    for lead in all_leads:
        entry = dict(lead)
        if lead["name"] in qualified_names:
            matched = next(s for s in scored if s["name"] == lead["name"])
            entry["score"] = matched["score"]
            entry["qualified"] = True
        else:
            entry["score"] = 0
            entry["qualified"] = False
        results.append(entry)

    best = max(scored, key=lambda x: x["score"]) if scored else {}

    return jsonify({
        "total": len(all_leads),
        "qualified_count": len(qualified),
        "best_lead": best.get("name", "—"),
        "best_score": best.get("score", 0),
        "results": results,
    })


@app.route("/api/outreach", methods=["POST"])
def api_outreach():
    data = request.get_json(force=True)
    lead = data.get("lead")
    if not lead:
        return jsonify({"error": "No lead provided"}), 400
    try:
        message = generate_outreach(lead)
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
