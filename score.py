def score_leads(leads):
    for l in leads:
        l["score"] = 10 if l["revenue"] > 1000 else 0
    return leads
