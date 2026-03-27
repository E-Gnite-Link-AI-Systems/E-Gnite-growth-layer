def qualify_leads(leads):
    return [l for l in leads if l["revenue"] > 1000]
