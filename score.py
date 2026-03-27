def score_leads(leads):
    for lead in leads:
        score = 0

        # Revenue weight
        if lead["revenue"] > 1000:
            score += 10

        # Industry match
        if lead.get("industry") == "marketing":
            score += 5

        # Bonus for higher revenue
        if lead["revenue"] > 5000:
            score += 5

        lead["score"] = score

    return leads
